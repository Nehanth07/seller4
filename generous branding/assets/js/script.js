/* ============================================================
   Generous — recreation interactions (original implementation)
   ============================================================ */
(function () {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Loader ---------- */
  const loader = document.getElementById('loader');
  const loaderCount = document.getElementById('loaderCount');

  function runLoader() {
    if (!loader) return finishLoad();
    let v = 0;
    const step = () => {
      v += Math.random() * 18 + 6;
      if (v >= 100) v = 100;
      if (loaderCount) loaderCount.textContent = Math.floor(v);
      if (v < 100) {
        setTimeout(step, 90);
      } else {
        setTimeout(finishLoad, 350);
      }
    };
    step();
  }

  function finishLoad() {
    document.body.classList.remove('is-loading');
    if (loader) loader.classList.add('is-done');
  }

  /* ---------- Custom cursor ---------- */
  const cursor = document.querySelector('.cursor');
  const dot = document.querySelector('.cursor__dot');
  const ring = document.querySelector('.cursor__ring');

  if (cursor && window.matchMedia('(hover:hover) and (pointer:fine)').matches) {
    let mx = window.innerWidth / 2, my = window.innerHeight / 2;
    let rx = mx, ry = my;

    window.addEventListener('mousemove', (e) => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate(${mx}px, ${my}px)`;
    });

    const loop = () => {
      rx += (mx - rx) * 0.18;
      ry += (my - ry) * 0.18;
      ring.style.transform = `translate(${rx}px, ${ry}px)`;
      requestAnimationFrame(loop);
    };
    loop();

    const hoverSel = 'a, button, .work-card, .sb-page, .a-toggle';
    document.querySelectorAll(hoverSel).forEach((el) => {
      el.addEventListener('mouseenter', () => cursor.classList.add('is-hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-hover'));
    });
    document.addEventListener('mouseleave', () => cursor.classList.add('is-hidden'));
    document.addEventListener('mouseenter', () => cursor.classList.remove('is-hidden'));
  }

  /* ---------- Header morph on scroll ---------- */
  const head = document.getElementById('siteHead');
  const hero = document.getElementById('hero');

  function onScroll() {
    const threshold = hero ? hero.offsetHeight * 0.6 : 400;
    document.body.classList.toggle('is-nav-small', window.scrollY > threshold);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav toggle ---------- */
  const toggle = document.getElementById('navToggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const open = document.body.classList.toggle('is-menu-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    document.querySelectorAll('.site-head__menu a').forEach((a) => {
      a.addEventListener('click', () => {
        document.body.classList.remove('is-menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Hero slider ---------- */
  const slides = Array.from(document.querySelectorAll('.sb-slide'));
  const pagination = document.getElementById('heroPagination');
  const DURATION = 5200;
  let current = 0;
  let timer = null;
  let startTime = 0;
  let rafId = null;

  if (slides.length && pagination) {
    slides.forEach((_, i) => {
      const b = document.createElement('button');
      b.className = 'sb-page' + (i === 0 ? ' is-active' : '');
      b.setAttribute('aria-label', 'Aller au projet ' + (i + 1));
      b.innerHTML = '<span class="sb-page__progress"></span>';
      b.addEventListener('click', () => goTo(i));
      pagination.appendChild(b);
    });

    const pages = Array.from(pagination.children);

    function setProgress(p) {
      const prog = pages[current] && pages[current].querySelector('.sb-page__progress');
      if (prog) prog.style.setProperty('--p', p);
    }

    function tick(now) {
      if (!startTime) startTime = now;
      const elapsed = now - startTime;
      setProgress(Math.min(100, (elapsed / DURATION) * 100));
      if (elapsed >= DURATION) {
        next();
      } else {
        rafId = requestAnimationFrame(tick);
      }
    }

    function restartTimer() {
      cancelAnimationFrame(rafId);
      startTime = 0;
      if (!reduceMotion) rafId = requestAnimationFrame(tick);
    }

    function goTo(i) {
      if (i === current) return;
      slides[current].classList.remove('is-active');
      pages[current].classList.remove('is-active');
      setProgress(0);
      current = i;
      slides[current].classList.add('is-active');
      pages[current].classList.add('is-active');
      restartTimer();
    }

    function next() { goTo((current + 1) % slides.length); }

    restartTimer();

    // pause when tab hidden
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) cancelAnimationFrame(rafId);
      else restartTimer();
    });
  }

  /* ---------- Word-by-word statement reveal ---------- */
  const words = document.querySelectorAll('.s-statement__text .word');
  if (words.length) {
    const statement = document.querySelector('.s-statement');
    const litOnScroll = () => {
      const rect = statement.getBoundingClientRect();
      const start = window.innerHeight * 0.85;
      const end = window.innerHeight * 0.25;
      const total = start - end;
      const progressed = Math.min(1, Math.max(0, (start - rect.top) / total));
      const count = Math.floor(progressed * words.length);
      words.forEach((w, i) => w.classList.toggle('is-lit', i < count));
    };
    window.addEventListener('scroll', litOnScroll, { passive: true });
    litOnScroll();
  }

  /* ---------- Scroll reveals ---------- */
  const revealEls = document.querySelectorAll('.work-card, .s-approach__col, .s-approach__title, .s-statement__text');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('reveal', 'is-in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach((el) => { el.classList.add('reveal'); io.observe(el); });
  }

  /* ---------- Cookie banner ---------- */
  const cookie = document.getElementById('cookie');
  if (cookie) {
    const stored = (function () { try { return localStorage.getItem('gb_cookie'); } catch (e) { return null; } })();
    if (!stored) setTimeout(() => cookie.classList.add('is-visible'), 1600);
    cookie.querySelectorAll('[data-cookie]').forEach((btn) => {
      btn.addEventListener('click', () => {
        try { localStorage.setItem('gb_cookie', btn.dataset.cookie); } catch (e) {}
        cookie.classList.remove('is-visible');
      });
    });
  }

  /* ---------- Init ---------- */
  window.addEventListener('load', runLoader);
  if (document.readyState === 'complete') runLoader();
})();
