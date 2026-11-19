// Photo galleries: a lightbox shared by every `.shot` link (with previous/next inside
// its gallery) and draggable, button-driven `.carousel` strips.
(() => {
    // Link popovers (schools): open below when there's no room above, align right near the edge.
    document.querySelectorAll('.school').forEach(link => {
        const pop = link.querySelector('.school-pop');
        const place = () => {
            link.classList.remove('pop-below', 'pop-right');
            const linkBox = link.getBoundingClientRect();
            const popBox = pop.getBoundingClientRect();
            if (linkBox.top - popBox.height - 16 < 0) link.classList.add('pop-below');
            if (linkBox.left + popBox.width > document.documentElement.clientWidth - 16) link.classList.add('pop-right');
        };
        link.addEventListener('mouseenter', place);
        link.addEventListener('focus', place);
    });

    const shots = [...document.querySelectorAll('.shot')];
    if (!shots.length) return;

    const box = document.createElement('dialog');
    box.className = 'lightbox';
    box.setAttribute('aria-label', 'Photo viewer');
    box.innerHTML = '<button class="lb-close" aria-label="Close">×</button>' +
        '<button class="lb-nav lb-prev" aria-label="Previous photo">←</button>' +
        '<figure><img alt=""><figcaption></figcaption></figure>' +
        '<button class="lb-nav lb-next" aria-label="Next photo">→</button>';
    document.body.append(box);
    const pic = box.querySelector('img');
    const caption = box.querySelector('figcaption');
    let group = [];
    let index = 0;

    const show = (i) => {
        index = (i + group.length) % group.length;
        const shot = group[index];
        pic.src = shot.href;
        pic.alt = shot.dataset.caption;
        caption.textContent = `${shot.dataset.caption}  ·  ${index + 1} / ${group.length}`;
    };

    shots.forEach(shot => shot.addEventListener('click', (event) => {
        event.preventDefault();
        if (shot.dataset.dragged) { delete shot.dataset.dragged; return; }
        if (!box.showModal) { location.href = shot.href; return; }
        const gallery = shot.closest('.carousel, .photo-rows, .moments');
        group = gallery ? [...gallery.querySelectorAll('.shot')] : [shot];
        show(group.indexOf(shot));
        box.showModal();
    }));
    box.querySelector('.lb-prev').addEventListener('click', () => show(index - 1));
    box.querySelector('.lb-next').addEventListener('click', () => show(index + 1));
    box.querySelector('.lb-close').addEventListener('click', () => box.close());
    box.addEventListener('click', (event) => { if (event.target === box) box.close(); });
    box.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowLeft') show(index - 1);
        if (event.key === 'ArrowRight') show(index + 1);
    });

    document.querySelectorAll('.carousel').forEach(carousel => {
        const track = carousel.querySelector('.car-track');
        const prev = carousel.querySelector('.car-prev');
        const next = carousel.querySelector('.car-next');
        const bar = carousel.querySelector('.car-progress span');
        const step = () => track.clientWidth * 0.8;
        const update = () => {
            const max = track.scrollWidth - track.clientWidth;
            prev.disabled = track.scrollLeft <= 2;
            next.disabled = track.scrollLeft >= max - 2;
            bar.style.width = `${max > 0 ? (track.clientWidth + track.scrollLeft) / track.scrollWidth * 100 : 100}%`;
        };
        prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
        next.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
        track.addEventListener('scroll', update, { passive: true });
        addEventListener('resize', update);
        track.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowLeft') { event.preventDefault(); track.scrollBy({ left: -step(), behavior: 'smooth' }); }
            if (event.key === 'ArrowRight') { event.preventDefault(); track.scrollBy({ left: step(), behavior: 'smooth' }); }
        });

        // Drag with a mouse (touch devices already swipe natively).
        let startX = 0, startScroll = 0, dragging = false, moved = false;
        track.addEventListener('pointerdown', (event) => {
            if (event.pointerType !== 'mouse') return;
            dragging = true; moved = false;
            startX = event.clientX; startScroll = track.scrollLeft;
        });
        addEventListener('pointermove', (event) => {
            if (!dragging) return;
            const dx = event.clientX - startX;
            if (Math.abs(dx) > 5 && !moved) { moved = true; track.classList.add('dragging'); }
            if (moved) track.scrollLeft = startScroll - dx;
        });
        addEventListener('pointerup', (event) => {
            if (!dragging) return;
            dragging = false;
            track.classList.remove('dragging');
            if (moved) {
                const shot = event.target.closest && event.target.closest('.shot');
                if (shot) shot.dataset.dragged = '1';
            }
        });
        track.addEventListener('dragstart', (event) => event.preventDefault());
        update();
    });
})();
