// Homepage card ↔ project hero morph. The clicked card's box, its screenshot and the
// header take the same view-transition names as the project hero, its screenshot and
// header — only for the navigation between those two pages, so the rest cross-fade.
(() => {
  const isHome = url => /\/(index\.html)?$/.test(new URL(url).pathname);
  const onHome = isHome(location.href);

  const inView = el => {
    const r = el.getBoundingClientRect();
    return r.bottom > 0 && r.top < innerHeight;
  };

  // The box paired with `url`: on the homepage the card linking to it, on a project page its hero
  const boxFor = url => {
    if (!url) return null;
    const box = onHome
      ? [...document.querySelectorAll('[data-hero]')].find(b => b.closest('a').pathname === new URL(url).pathname)
      : isHome(url) && document.querySelector('[data-hero]');
    return box && inView(box) ? box : null;
  };

  const name = (box, on) => {
    const parts = [[box, 'hero'], [box.querySelector('[data-hero-img]'), 'hero-img'], [document.querySelector('header'), 'site-header']];
    for (const [el, n] of parts) if (el) el.style.viewTransitionName = on && inView(el) ? n : '';
  };

  addEventListener('pageswap', e => {
    const box = e.viewTransition && boxFor(e.activation?.entry.url);
    if (box) name(box, true);
  });

  addEventListener('pagereveal', e => {
    // Coming back from the bfcache: drop names left over from leaving this page
    document.querySelectorAll('[data-hero]').forEach(b => name(b, false));
    const box = e.viewTransition && boxFor(window.navigation?.activation?.from?.url);
    if (!box) return;
    name(box, true);
    if (!onHome) document.documentElement.classList.add('from-card');
    e.viewTransition.finished.then(() => name(box, false));
  });

  // The × on a project page steps back when the homepage is the previous page, so the
  // homepage reopens where it was and the hero shrinks back into its card
  addEventListener('click', e => {
    if (!e.target.closest('[data-close]') || e.metaKey || e.ctrlKey || e.shiftKey) return;
    const prev = window.navigation?.entries()[navigation.currentEntry.index - 1];
    if (prev && isHome(prev.url)) {
      e.preventDefault();
      history.back();
    }
  });
})();
