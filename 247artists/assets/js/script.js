/* ============================================================
   24/7 Artists — recreation interactions (original implementation)
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Preloader ---------- */
  const preloader = document.getElementById('preloader');
  const fill = document.getElementById('preloaderFill');

  function runPreloader() {
    let v = 0;
    const step = () => {
      v += Math.random() * 20 + 8;
      if (v >= 100) v = 100;
      if (fill) fill.style.width = v + '%';
      if (v < 100) setTimeout(step, 80);
      else setTimeout(() => {
        document.body.classList.remove('is-loading');
        if (preloader) preloader.classList.add('is-done');
      }, 300);
    };
    step();
  }

  /* ---------- Header scroll state ---------- */
  const head = document.getElementById('siteHead');
  const onScroll = () => head && head.classList.toggle('is-scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav ---------- */
  const toggle = document.getElementById('navToggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const open = document.body.classList.toggle('is-menu-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.querySelectorAll('.mobile-nav a').forEach((a) =>
      a.addEventListener('click', () => document.body.classList.remove('is-menu-open')));
  }

  /* ---------- Technology stepper ---------- */
  const techItems = Array.from(document.querySelectorAll('.tech-item'));
  const techCards = Array.from(document.querySelectorAll('.tech-card'));
  let techIndex = 0, techTimer = null;

  function setTech(i) {
    techIndex = i;
    techItems.forEach((el, k) => el.classList.toggle('is-active', k === i));
    techCards.forEach((el, k) => el.classList.toggle('is-active', k === i));
  }
  function autoTech() {
    techTimer = setInterval(() => setTech((techIndex + 1) % techItems.length), 3500);
  }
  if (techItems.length) {
    techItems.forEach((el, i) => el.addEventListener('click', () => {
      setTech(i);
      clearInterval(techTimer); autoTech();
    }));
    autoTech();
  }

  /* ---------- Network live clock ---------- */
  const ch = document.getElementById('clockH');
  const cm = document.getElementById('clockM');
  const cs = document.getElementById('clockS');
  function tickClock() {
    const d = new Date();
    const p = (n) => String(n).padStart(2, '0');
    if (ch) ch.textContent = p(d.getHours());
    if (cm) cm.textContent = p(d.getMinutes());
    if (cs) cs.textContent = p(d.getSeconds());
  }
  if (ch) { tickClock(); setInterval(tickClock, 1000); }

  /* ---------- Testimonials ---------- */
  const slides = Array.from(document.querySelectorAll('.testimonial'));
  const dotsWrap = document.getElementById('testimonialDots');
  let tIndex = 0, tTimer = null;

  if (slides.length && dotsWrap) {
    slides.forEach((_, i) => {
      const b = document.createElement('button');
      if (i === 0) b.classList.add('is-active');
      b.setAttribute('aria-label', 'Testimonial ' + (i + 1));
      b.addEventListener('click', () => { setTestimonial(i); resetT(); });
      dotsWrap.appendChild(b);
    });
    const dots = Array.from(dotsWrap.children);
    function setTestimonial(i) {
      tIndex = i;
      slides.forEach((el, k) => el.classList.toggle('is-active', k === i));
      dots.forEach((el, k) => el.classList.toggle('is-active', k === i));
    }
    function resetT() { clearInterval(tTimer); tTimer = setInterval(() => setTestimonial((tIndex + 1) % slides.length), 5000); }
    window.__setTestimonial = setTestimonial;
    resetT();
  }

  /* ---------- FAQ view more ---------- */
  const faqMore = document.getElementById('faqMore');
  if (faqMore) {
    faqMore.addEventListener('click', () => {
      const hidden = document.querySelectorAll('.faq-item.is-hidden');
      hidden.forEach((el) => el.classList.remove('is-hidden'));
      faqMore.style.display = 'none';
    });
  }
  // close other open FAQs (accordion behavior)
  document.querySelectorAll('.faq-item').forEach((item) => {
    item.addEventListener('toggle', () => {
      if (item.open) {
        document.querySelectorAll('.faq-item[open]').forEach((o) => { if (o !== item) o.open = false; });
      }
    });
  });

  /* ---------- Cookie banner ---------- */
  const cookie = document.getElementById('cookie');
  if (cookie) {
    const stored = (() => { try { return localStorage.getItem('a247_cookie'); } catch (e) { return null; } })();
    if (!stored) setTimeout(() => cookie.classList.add('is-visible'), 1400);
    cookie.querySelectorAll('[data-cookie]').forEach((b) =>
      b.addEventListener('click', () => {
        try { localStorage.setItem('a247_cookie', b.dataset.cookie); } catch (e) {}
        cookie.classList.remove('is-visible');
      }));
  }

  /* ---------- Scroll reveals ---------- */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.about-tile, .net-card, .price-card, .s-education__intro, .s-education__courses, .s-tech__head, .course-list li')
      .forEach((el) => { el.classList.add('reveal'); io.observe(el); });
  }

  /* ---------- Init ---------- */
  window.addEventListener('load', runPreloader);
  if (document.readyState === 'complete') runPreloader();
})();
