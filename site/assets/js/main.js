(() => {
  document.documentElement.classList.remove("no-js");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const desktop = window.matchMedia("(min-width: 835px)");
  const clamp = (v, a, b) => Math.min(Math.max(v, a), b);

  /* ---------- Меню на телефоне ---------- */
  const nav = document.querySelector(".nav");
  const toggle = nav && nav.querySelector(".nav__toggle");
  if (toggle) {
    const setOpen = (open) => {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    };
    toggle.addEventListener("click", () => setOpen(!nav.classList.contains("is-open")));
    document.addEventListener("keydown", (e) => e.key === "Escape" && setOpen(false));
    desktop.addEventListener("change", () => setOpen(false));
  }

  /* ---------- Появление блоков ---------- */
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Абзац, который проявляется по словам ---------- */
  const statement = document.querySelector(".statement");
  let words = [];
  if (statement) {
    const text = statement.textContent.trim().replace(/\s+/g, " ");
    statement.setAttribute("aria-label", text);
    statement.innerHTML = text.split(" ").map((w) => `<span class="w" aria-hidden="true">${w}</span>`).join(" ");
    words = [...statement.querySelectorAll(".w")];
    if (reduced) words.forEach((w) => w.classList.add("on"));
  }

  /* ---------- Главы: телефон на месте, экран меняется шторкой ---------- */
  const chapters = document.querySelector(".chapters");
  const stageScreen = chapters && chapters.querySelector(".chapters__stage .phone__screen");
  const chapterEls = chapters ? [...chapters.querySelectorAll(".chapter")] : [];
  const stageScreens = stageScreen ? [...stageScreen.querySelectorAll(".screen")] : [];
  const setStaged = () => {
    if (chapters && stageScreen) chapters.classList.toggle("is-staged", desktop.matches);
  };
  setStaged();
  desktop.addEventListener("change", () => { setStaged(); frame(); });

  /* ---------- Кадр прокрутки ---------- */
  const heroDevice = document.querySelector(".hero__device");
  let ticking = false;
  function frame() {
    ticking = false;
    const vh = window.innerHeight;

    if (heroDevice && !reduced) {
      const r = heroDevice.getBoundingClientRect();
      const p = clamp(1 - r.top / vh, 0, 1);
      heroDevice.style.transform = `translateY(${(1 - p) * 40}px) scale(${0.92 + p * 0.1})`;
    }

    if (words.length && !reduced) {
      const r = statement.getBoundingClientRect();
      const p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1);
      const lit = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle("on", i < lit));
    }

    if (chapters && chapters.classList.contains("is-staged")) {
      const s = stageScreen.getBoundingClientRect();
      chapterEls.forEach((ch, i) => {
        const c = ch.getBoundingClientRect();
        const top = clamp(c.top - s.top, 0, s.height);
        const bottom = clamp(s.bottom - c.bottom, 0, s.height);
        if (stageScreens[i]) stageScreens[i].style.clipPath = `inset(${top}px 0 ${bottom}px 0)`;
      });
    }
  }
  const request = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  window.addEventListener("scroll", request, { passive: true });
  window.addEventListener("resize", request);
  frame();

  /* ---------- Пошаговые истории: шаг справа меняет экран слева ---------- */
  document.querySelectorAll("[data-story]").forEach((story) => {
    const steps = [...story.querySelectorAll(".step")];
    const screens = [...story.querySelectorAll(".story__stage .screen")];
    const board = story.querySelector(".story__stage .board");
    const badge = board && board.querySelector(".board__badge");
    const activate = (i) => {
      steps.forEach((s, k) => s.classList.toggle("is-on", k === i));
      screens.forEach((s, k) => s.classList.toggle("is-on", k === i));
      if (board) {
        board.dataset.stage = String(i);
        if (badge && steps[i]) badge.textContent = steps[i].dataset.badge || "";
      }
    };
    if (!("IntersectionObserver" in window)) { activate(0); return; }
    let io;
    const observe = () => {
      if (io) io.disconnect();
      io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) activate(steps.indexOf(e.target)); });
      }, { rootMargin: desktop.matches ? "-45% 0px -45% 0px" : "-70% 0px -20% 0px" });
      steps.forEach((s) => io.observe(s));
    };
    observe();
    desktop.addEventListener("change", observe);
    activate(0);
  });

  /* ---------- Пергамент в телефоне: стадии идут по кругу, пока экран виден ---------- */
  document.querySelectorAll("[data-autoplay]").forEach((board) => {
    if (reduced || !("IntersectionObserver" in window)) { board.dataset.stage = "2"; return; }
    const labels = (board.dataset.labels || "").split("|");
    const hud = board.closest(".screen") && board.closest(".screen").querySelector(".ar-hud");
    const dots = hud ? [...hud.querySelectorAll(".ar-progress i")] : [];
    const title = hud && hud.querySelector("b");
    let stage = 0;
    let timer = null;
    const show = () => {
      board.dataset.stage = String(stage);
      dots.forEach((d, k) => d.classList.toggle("on", k <= stage));
      if (title && labels[stage]) title.textContent = labels[stage];
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting && !timer) {
          show();
          timer = setInterval(() => { stage = (stage + 1) % 6; show(); }, 1700);
        } else if (!e.isIntersecting && timer) {
          clearInterval(timer);
          timer = null;
        }
      });
    }, { threshold: 0.2 });
    io.observe(board);
  });

  /* ---------- Оглавление документов ---------- */
  const tocLinks = document.querySelectorAll(".legal__toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    const map = new Map();
    tocLinks.forEach((a) => {
      const t = document.getElementById(a.getAttribute("href").slice(1));
      if (t) map.set(t, a);
    });
    const tio = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          tocLinks.forEach((a) => a.classList.remove("is-current"));
          map.get(e.target).classList.add("is-current");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    map.forEach((_, el) => tio.observe(el));
  }

  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
