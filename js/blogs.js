(() => {
    const archive = document.querySelector('.blog-archive');
    const filters = archive.querySelector('.blog-filters');
    const categories = [...filters.querySelectorAll('[data-category]')];
    const tags = [...filters.querySelectorAll('[data-tag]')];
    const rows = [...archive.querySelectorAll('.blog-row')].map(element => ({
        element,
        category: element.dataset.category,
        tags: JSON.parse(element.dataset.tags),
    }));
    let category = '';
    let tag = '';

    function render() {
        let count = 0;
        for (const row of rows) {
            const matches = (!category || row.category === category) && (!tag || row.tags.includes(tag));
            row.element.hidden = !matches;
            if (matches) count++;
        }
        categories.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === category)));
        tags.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.tag === tag)));
        archive.querySelector('.blog-count').textContent = `${count} ${count === 1 ? 'post' : 'posts'}`;
        archive.querySelector('.blog-empty').hidden = count !== 0;
    }

    function readLocation() {
        const params = new URLSearchParams(location.search);
        category = categories.some(button => button.dataset.category === params.get('category')) ? params.get('category') : '';
        tag = tags.some(button => button.dataset.tag === params.get('tag')) ? params.get('tag') : '';
        render();
    }

    function updateLocation() {
        const url = new URL(location.href);
        category ? url.searchParams.set('category', category) : url.searchParams.delete('category');
        tag ? url.searchParams.set('tag', tag) : url.searchParams.delete('tag');
        if (url.href !== location.href) history.pushState(null, '', url);
        render();
    }

    categories.forEach(button => button.addEventListener('click', () => {
        category = button.dataset.category;
        updateLocation();
    }));
    tags.forEach(button => button.addEventListener('click', () => {
        tag = button.dataset.tag;
        updateLocation();
    }));
    archive.querySelector('.blog-empty button').addEventListener('click', () => {
        category = tag = '';
        updateLocation();
    });
    window.addEventListener('popstate', readLocation);
    readLocation();
    filters.hidden = false;
})();
