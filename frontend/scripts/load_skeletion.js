const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Creates text for the Get Started button and a dialog above that.
(function () {
    const el = document.getElementById('helloText'), box = document.getElementById('hello');
    const txt = SBT('Cliquez sur le bouton ci-dessous pour commencer !',
        'Hit the button below to get started!');
    const plain = txt.replace(/<[^>]+>/g, '');
    if (reduce) { el.innerHTML = txt; box.classList.add('done'); return; }
    let i = 0;
    (function tick() {
        i++;
        // on retrouve la position dans le HTML pour garder le nom en rouge
        let n = 0, out = '';
        for (const part of txt.split(/(<[^>]+>)/)) {
            if (part.startsWith('<')) { out += part; continue; }
            const take = Math.max(0, Math.min(part.length, i - n)); out += part.slice(0, take); n += part.length;
        }
        el.innerHTML = out;
        if (i < plain.length) setTimeout(tick, 45); else box.classList.add('done');
    })();
})();

// agrandir les captures et la carte
const zoom = document.getElementById('zoom');
document.querySelectorAll('.shots img, .map img, img.shot, .gbc.hero img').forEach((im) => im.addEventListener('click', () => {
    zoom.querySelector('img').src = im.src; zoom.querySelector('img').alt = im.alt; zoom.showModal();
}));
zoom.addEventListener('click', () => zoom.close());