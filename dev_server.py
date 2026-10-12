"""Serve a local preview, rebuild on source changes, and refresh the browser."""

import argparse
import io
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
WATCHED = ("content", "site_templates", "static", "site_builder.py", "image_manifest.json")
VERSION_PATH = "/__dev/version"


def snapshot():
    files = {}
    for name in WATCHED:
        source = ROOT / name
        for path in source.rglob("*") if source.is_dir() else [source]:
            if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
                continue
            try:
                if path.is_file():
                    stat = path.stat()
                    files[str(path)] = (stat.st_mtime_ns, stat.st_size)
            except FileNotFoundError:
                pass  # An editor may replace a file while we are scanning.
    return files


class Preview:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.output = None
        self.version = ""
        self.lock = threading.Lock()

    def rebuild(self):
        version = uuid.uuid4().hex
        output = self.directory / version
        result = subprocess.run(
            [sys.executable, str(ROOT / "site_builder.py"), "--output", str(output)],
            cwd=ROOT,
        )
        if result.returncode:
            shutil.rmtree(output, ignore_errors=True)
            print("Build failed. Keeping the last working preview; fix the source and save again.", flush=True)
            return False
        with self.lock:
            previous = self.output
            self.output, self.version = output, version
            if previous:
                shutil.rmtree(previous)
        return True

    def watch(self, stop, previous):
        pending = previous
        while not stop.wait(0.35):
            current = snapshot()
            # Wait for one stable scan so a multi-file save produces one build.
            if current != previous and current == pending:
                print("Source changed. Rebuilding…", flush=True)
                self.rebuild()
                previous = current
            pending = current


def handler_for(preview):
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            with preview.lock:
                self.directory = str(preview.output)
                super().do_GET()

        def do_HEAD(self):
            with preview.lock:
                self.directory = str(preview.output)
                super().do_HEAD()

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def send_bytes(self, body, content_type):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return io.BytesIO(body)

        def send_head(self):
            route = urlsplit(self.path).path
            if route == VERSION_PATH:
                return self.send_bytes(json.dumps(preview.version).encode(), "application/json")
            path = Path(self.translate_path(self.path))
            if path.is_dir() and route.endswith("/"):
                path /= "index.html"
            if path.is_file() and path.suffix == ".html":
                script = """<script>
(() => {
  const version = VERSION;
  let checking = false;
  setInterval(async () => {
    if (checking) return;
    checking = true;
    try {
      const response = await fetch('/__dev/version', {cache: 'no-store'});
      if (response.ok && await response.json() !== version) location.reload();
    } catch (_) {} finally { checking = false; }
  }, 600);
})();
</script>""".replace("VERSION", json.dumps(preview.version))
                body = path.read_text(encoding="utf-8").replace("</body>", script + "</body>")
                return self.send_bytes(body.encode(), "text/html; charset=utf-8")
            return super().send_head()

        def log_message(self, format, *args):
            if urlsplit(self.path).path != VERSION_PATH:
                super().log_message(format, *args)

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="site-preview-") as directory:
        preview = Preview(directory)
        previous = snapshot()
        if not preview.rebuild():
            return 1
        with ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(preview)) as server:
            stop = threading.Event()
            watcher = threading.Thread(target=preview.watch, args=(stop, previous), daemon=True)
            watcher.start()
            print(f"Live preview: http://127.0.0.1:{server.server_port}/work/ (Ctrl+C to stop)", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                stop.set()
                watcher.join()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
