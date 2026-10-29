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

// le film d'ouverture en boucle
(function () {
    const fig = document.getElementById('film'), dots = document.getElementById('filmDots');
    const imgs = [...fig.querySelectorAll('.screen img')];
    let k = 0, timer = null;
    const show = (j) => {
        k = (j + imgs.length) % imgs.length;
        imgs.forEach((im, n) => { im.style.opacity = n === k ? 1 : 0; });
        dots.querySelectorAll('button').forEach((b, n) => b.classList.toggle('on', n === k));
    };
    imgs.forEach((_, n) => {
        const b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', SBT('Image ', 'Frame ') + (n + 1));
        b.onclick = () => { show(n); clearInterval(timer); timer = null; };
        dots.append(b);
    });
    show(0);
    if (!reduce) timer = setInterval(() => show(k + 1), 1800);
})();

// journal : compte des cœurs
(function () {
    const all = document.querySelectorAll('#quest li'), todo = document.querySelectorAll('#quest li.todo').length;
    document.getElementById('tally').textContent = SBT(`♥ ${all.length - todo} / ${all.length} cœurs`, `♥ ${all.length - todo} / ${all.length} hearts`);
})();

// La musique de l'écran titre, en version douce pour la page (docs/titre.ogg, tools/make_page_music_douce.py). Les navigateurs refusent le
// son avant un geste du visiteur : l'écran « PRESS START » le lui demande, comme une console.
// Couper la musique est retenu (préférence de ce navigateur seulement) : on n'affiche alors plus l'écran.
(function () {
    const audio = document.getElementById('bgm'), btn = document.getElementById('music'), label = document.getElementById('musicLabel');
    const gate = document.getElementById('gate');
    const closeGate = () => {
        document.body.classList.remove('gated');
        gate.classList.add('gone');
        setTimeout(() => { gate.hidden = true; }, 700);
        removeEventListener('keydown', onKey, true);
    };
    const onKey = (e) => { if (e.key !== 'Tab' && e.target.id !== 'silent') { e.preventDefault(); begin(); } };
    if (!audio.canPlayType('audio/ogg; codecs="vorbis"')) { gate.hidden = true; return; }
    let muted = false;
    try { muted = localStorage.getItem('gulls.music') === 'off'; } catch (_) { }
    const VOL = 0.55;
    audio.volume = 0;
    // la musique entre en douceur (2 s) à chaque lecture
    audio.addEventListener('play', () => {
        const t0 = performance.now();
        (function up() { const k = Math.min(1, (performance.now() - t0) / 2000); audio.volume = VOL * k * k; if (k < 1 && !audio.paused) requestAnimationFrame(up); })();
    });
    btn.hidden = false;
    const render = () => {
        const on = !audio.paused;
        btn.classList.toggle('on', on);
        label.textContent = on ? SBT('Couper la musique', 'Mute the music') : SBT('♪ Musique', '♪ Music');
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    };
    const remember = (v) => { try { localStorage.setItem('gulls.music', v); } catch (_) { } };
    const begin = () => { audio.play().then(render, render); closeGate(); };
    btn.addEventListener('click', () => {
        if (audio.paused) { remember('on'); audio.play().then(render, render); }
        else { audio.pause(); remember('off'); render(); }
    });
    audio.addEventListener('play', render); audio.addEventListener('pause', render);
    render();
    if (muted) { gate.hidden = true; return; }
    document.body.classList.add('gated');
    gate.addEventListener('click', (e) => { if (e.target.id === 'silent') { closeGate(); } else { begin(); } });
    addEventListener('keydown', onKey, true);
    document.getElementById('pressStart').focus({ preventScroll: true });
})();

// agrandir les captures et la carte
const zoom = document.getElementById('zoom');
document.querySelectorAll('.shots img, .map img, img.shot, .gbc.hero img').forEach((im) => im.addEventListener('click', () => {
    zoom.querySelector('img').src = im.src; zoom.querySelector('img').alt = im.alt; zoom.showModal();
}));
zoom.addEventListener('click', () => zoom.close());