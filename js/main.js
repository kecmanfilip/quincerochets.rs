/* ═══════════════════════════════════════════════════════════
   Quincè crochèts — Main JS
   ═══════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── NAV ─────────────────────────────────────────────────── */
  function initNav() {
    const toggle = document.getElementById('navToggle');
    const mobile = document.getElementById('navMobile');
    if (!toggle || !mobile) return;

    toggle.addEventListener('click', function () {
      const open = mobile.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });

    // Close mobile nav on link click
    mobile.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        mobile.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!toggle.contains(e.target) && !mobile.contains(e.target)) {
        mobile.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    // Active nav state
    var path = window.location.pathname;
    document.querySelectorAll('.nav-link, .nav-mobile-link').forEach(function (link) {
      var href = link.getAttribute('href');
      if (href === '/' && path === '/') {
        link.classList.add('active');
      } else if (href !== '/' && href && path.startsWith(href)) {
        link.classList.add('active');
      }
    });
  }

  /* ── FAQ ─────────────────────────────────────────────────── */
  function initFaq() {
    document.querySelectorAll('.faq-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('.faq-item');
        var isOpen = item.classList.contains('open');

        // Close all
        document.querySelectorAll('.faq-item.open').forEach(function (el) {
          el.classList.remove('open');
          el.querySelector('.faq-btn').setAttribute('aria-expanded', 'false');
        });

        // Open clicked if it wasn't open
        if (!isOpen) {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  /* ── CONTACT FORM ────────────────────────────────────────── */
  function initContactForm() {
    var form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      // Netlify handles POST; on local / non-Netlify, fallback to Instagram
      if (window.location.hostname === 'localhost' ||
          window.location.hostname === '127.0.0.1' ||
          window.location.protocol === 'file:') {
        e.preventDefault();
        var ime = (document.getElementById('ime') || {}).value || '';
        window.open('https://www.instagram.com/quince.crochets', '_blank', 'noopener,noreferrer');
        if (ime) {
          alert('Hvala, ' + ime.split(' ')[0] + '! Otvorili smo Instagram — pošalji nam DM sa detaljima. Odgovaramo brzo!');
        }
        form.reset();
      }
      // On Netlify, let the form submit naturally (data-netlify="true")
    });
  }

  /* ── COLOR SELECTION (product pages) ────────────────────── */
  function initColorSelection() {
    document.querySelectorAll('.color-option').forEach(function (opt) {
      opt.addEventListener('click', function () {
        var parent = opt.closest('.color-options');
        parent.querySelectorAll('.color-option').forEach(function (o) {
          o.querySelector('.color-circle').style.boxShadow = '';
        });
        opt.querySelector('.color-circle').style.boxShadow = '0 0 0 2px #9b1c2e, 0 0 0 4px #d4941a';
        var modelInput = document.getElementById('model');
        if (modelInput && opt.dataset.color) {
          // Pre-fill color info in form if navigating to contact
        }
      });
    });
  }

  /* ── INIT ────────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    initNav();
    initFaq();
    initContactForm();
    initColorSelection();
  });

})();
