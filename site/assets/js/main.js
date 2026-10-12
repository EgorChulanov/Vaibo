(() => {
  const root = document.documentElement;
  root.classList.remove("no-js");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Навигация ---------- */
  const nav = document.querySelector(".nav");
  if (nav) {
    const toggle = nav.querySelector(".nav__toggle");
    const onScroll = () => nav.classList.toggle("is-stuck", window.scrollY > 4);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    if (toggle) {
      const setOpen = (open) => {
        nav.classList.toggle("is-open", open);
        toggle.setAttribute("aria-expanded", String(open));
        document.body.style.overflow = open ? "hidden" : "";
      };
      toggle.addEventListener("click", () => setOpen(!nav.classList.contains("is-open")));
      nav.querySelectorAll(".nav__links a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
      document.addEventListener("keydown", (e) => e.key === "Escape" && setOpen(false));
    }
  }

  /* ---------- Появление при скролле ---------- */
  const revealEls = document.querySelectorAll(".reveal, .reveal-scale, .basket");
  if ("IntersectionObserver" in window && !reduced) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.18, rootMargin: "0px 0px -8% 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Счётчики ---------- */
  const counters = document.querySelectorAll("[data-count]");
  const runCounter = (el) => {
    const target = Number(el.dataset.count);
    const prefix = el.dataset.prefix || "";
    if (reduced) { el.textContent = prefix + target; return; }
    const duration = 1400;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ("IntersectionObserver" in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { runCounter(entry.target); cio.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach((el) => cio.observe(el));
  }

  /* ---------- Hero: иконка уплывает и уменьшается при скролле ---------- */
  const heroIcon = document.querySelector(".hero__icon");
  const heroContent = document.querySelector(".hero__content");

  /* ---------- Манифест: слова «загораются» по мере скролла ---------- */
  const manifesto = document.querySelector(".manifesto__text");
  let words = [];
  if (manifesto) {
    const text = manifesto.textContent.trim().replace(/\s+/g, " ");
    manifesto.setAttribute("aria-label", text);
    manifesto.innerHTML = text
      .split(" ")
      .map((w) => `<span class="w" aria-hidden="true">${w}</span>`)
      .join(" ");
    words = [...manifesto.querySelectorAll(".w")];
  }

  let ticking = false;
  const onFrame = () => {
    ticking = false;
    const vh = window.innerHeight;

    if (heroIcon && heroContent && !reduced) {
      const p = Math.min(Math.max(window.scrollY / (vh * 0.9), 0), 1);
      heroIcon.style.transform = `translateY(${p * -40}px) scale(${1 - p * 0.25}) rotate(${p * -6}deg)`;
      heroContent.style.opacity = String(1 - p * 1.1);
    }

    if (words.length) {
      const r = manifesto.getBoundingClientRect();
      // 0 — когда блок появился внизу экрана, 1 — когда дошёл до верхней трети
      const p = Math.min(Math.max((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0), 1);
      const lit = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle("on", i < lit));
    }
  };
  const requestFrame = () => {
    if (!ticking) { ticking = true; requestAnimationFrame(onFrame); }
  };
  window.addEventListener("scroll", requestFrame, { passive: true });
  window.addEventListener("resize", requestFrame);
  if (reduced) words.forEach((w) => w.classList.add("on"));
  onFrame();

  /* ---------- Как это работает: шаги переключают экран телефона ---------- */
  const steps = document.querySelectorAll(".step");
  const screens = document.querySelectorAll(".screen");
  const timer = document.querySelector("[data-timer]");
  let timerRun = 0;
  const startTimer = () => {
    if (!timer) return;
    const id = ++timerRun;
    const total = 30;
    const start = performance.now();
    const tick = (now) => {
      if (id !== timerRun) return;
      const p = Math.min((now - start) / 2400, 1);
      const left = Math.round(total * (1 - (1 - Math.pow(1 - p, 3))));
      timer.textContent = `0:${String(left).padStart(2, "0")}`;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const activate = (index) => {
    steps.forEach((s, i) => s.classList.toggle("is-active", i === index));
    screens.forEach((s, i) => s.classList.toggle("is-active", i === index));
    if (screens[index] && screens[index].querySelector("[data-timer]")) startTimer();
  };
  if (steps.length && "IntersectionObserver" in window) {
    const sio = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) activate([...steps].indexOf(entry.target));
      });
    }, {
      // На телефоне верх экрана занят макетом, поэтому шаг «активен» в нижней части
      rootMargin: window.matchMedia("(max-width: 834px)").matches ? "-72% 0px -18% 0px" : "-45% 0px -45% 0px",
    });
    steps.forEach((s) => sio.observe(s));
    activate(0);
  }

  /* ---------- Галерея ---------- */
  document.querySelectorAll(".gallery").forEach((g) => {
    const track = g.querySelector(".gallery__track");
    const prev = g.querySelector("[data-dir='-1']");
    const next = g.querySelector("[data-dir='1']");
    if (!track || !prev || !next) return;
    const update = () => {
      prev.disabled = track.scrollLeft < 8;
      next.disabled = track.scrollLeft + track.clientWidth > track.scrollWidth - 8;
    };
    [prev, next].forEach((btn) =>
      btn.addEventListener("click", () => {
        const card = track.querySelector(".diet");
        const step = card ? card.getBoundingClientRect().width + 20 : 320;
        track.scrollBy({ left: step * Number(btn.dataset.dir) * 2, behavior: reduced ? "auto" : "smooth" });
      })
    );
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  /* ---------- Cookies ---------- */
  const cookie = document.querySelector(".cookie");
  if (cookie) {
    let seen = false;
    try { seen = localStorage.getItem("vaibo-cookie-ok") === "1"; } catch (e) { /* приватный режим */ }
    if (!seen) setTimeout(() => cookie.classList.add("is-shown"), 1200);
    cookie.querySelector("button").addEventListener("click", () => {
      cookie.classList.remove("is-shown");
      try { localStorage.setItem("vaibo-cookie-ok", "1"); } catch (e) { /* ничего страшного */ }
    });
  }

  /* ---------- Оглавление юридических страниц ---------- */
  const tocLinks = document.querySelectorAll(".legal__toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    const map = new Map();
    tocLinks.forEach((a) => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target) map.set(target, a);
    });
    const tio = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          tocLinks.forEach((a) => a.classList.remove("is-current"));
          map.get(entry.target).classList.add("is-current");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    map.forEach((_, el) => tio.observe(el));
  }

  /* ---------- Год в подвале ---------- */
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
