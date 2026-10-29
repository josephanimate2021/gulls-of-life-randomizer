// Language Changer (credit to soaresden & claude for the code)
(function () {
    var l = null; try { l = localStorage.getItem('sb.lang'); } catch (_) { }
    if (l !== 'fr' && l !== 'en') l = /^fr/i.test(navigator.language || '') ? 'fr' : 'en';
    window.SB_LANG = l; document.documentElement.lang = l;
    window.SBT = function (fr, en) { return l === 'en' && en != null ? en : fr; };
    document.addEventListener('DOMContentLoaded', function () {
        if (l === 'en') document.querySelectorAll('[data-en]').forEach(function (e) { e.innerHTML = e.getAttribute('data-en'); });
        if (l === 'en') document.querySelectorAll('[data-en-alt]').forEach(function (e) { e.alt = e.getAttribute('data-en-alt'); });
        var b = document.getElementById('lang');
        b.textContent = l === 'en' ? '🇫🇷 FR' : '🇬🇧 EN';
        b.onclick = function () { try { localStorage.setItem('sb.lang', l === 'en' ? 'fr' : 'en'); } catch (_) { } location.reload(); };
    });
})();