"""Собирает все страницы сайта Vaibo из общего шаблона.

Запуск из корня репозитория: python3 tools/build_pages.py site
Тексты страниц правятся здесь, потом страницы пересобираются.
"""
import sys
from pathlib import Path

SITE = Path(sys.argv[1])
UPDATED = "12 октября 2026 г."


def T(s):
    return f'<span class="todo">[{s}]</span>'


OPERATOR = T("ИП Фамилия Имя Отчество / ООО «Название»")
INN = T("ИНН")
OGRN = T("ОГРН / ОГРНИП")
ADDRESS = T("адрес")
HOSTING = T("название и город хостинга в России")
MAIL = "hello@vaibofood.ru"
PMAIL = "privacy@vaibofood.ru"

NAV = [
    ("/", "Обзор"),
    ("/how.html", "Как это работает"),
    ("/parchment.html", "Пергамент"),
    ("/features.html", "Возможности"),
    ("/faq.html", "Вопросы"),
]


def head(title, desc, path, extra=""):
    full = "Vaibo" if path == "/" else f"{title} · Vaibo"
    return f"""<!doctype html>
<html lang="ru" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{full}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="https://vaibofood.ru{path}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:site_name" content="Vaibo">
  <meta property="og:title" content="{full}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://vaibofood.ru/assets/img/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preload" href="/assets/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/styles.css">
{extra}</head>
<body>
  <a class="skip" href="#main">Перейти к содержанию</a>
  <header class="nav">
    <nav class="wrap wrap--wide nav__inner" aria-label="Основное меню">
      <a class="nav__brand" href="/" aria-label="Vaibo, на главную"><img src="/assets/img/wordmark-blue.png" alt="vaibo" width="1567" height="312"></a>
      <ul class="nav__links" id="nav-links">
{nav_items(path)}
      </ul>
      <a class="btn btn--sm" href="/download.html">Скачать</a>
      <button class="nav__toggle" type="button" aria-controls="nav-links" aria-expanded="false" aria-label="Открыть меню"><span></span><span></span></button>
    </nav>
  </header>
  <main id="main">
"""


def nav_items(path):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == path else ""
        out.append(f'        <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(out)


FOOT = """  </main>
  <footer class="footer">
    <div class="wrap wrap--wide">
      <div class="footer__notes">
        <p>Vaibo помогает планировать питание и покупки. Это не медицинская услуга: приложение не ставит диагнозы и не подбирает лечебное питание. Если у вас есть заболевания, аллергия или вы ждёте ребёнка, посоветуйтесь с врачом.</p>
        <p>Цены в Vaibo берутся из каталога ВкусВилла на момент проверки. Итоговую стоимость, наличие и доставку ВкусВилл показывает при оформлении заказа. ВкусВилл является товарным знаком своего правообладателя.</p>
        <p>Экраны приложения на сайте показаны для примера, цены на них условные. iPhone и App Store являются товарными знаками Apple Inc.</p>
      </div>
      <div class="footer__cols">
        <div>
          <h4>Vaibo</h4>
          <ul>
            <li><a href="/how.html">Как это работает</a></li>
            <li><a href="/parchment.html">Пергамент</a></li>
            <li><a href="/features.html">Возможности</a></li>
            <li><a href="/faq.html">Вопросы</a></li>
          </ul>
        </div>
        <div>
          <h4>Документы</h4>
          <ul>
            <li><a href="/legal/terms.html">Пользовательское соглашение</a></li>
            <li><a href="/legal/privacy.html">Обработка персональных данных</a></li>
            <li><a href="/legal/consent.html">Согласия</a></li>
            <li><a href="/legal/offer.html">Оферта</a></li>
            <li><a href="/legal/cookies.html">Cookies</a></li>
          </ul>
        </div>
        <div>
          <h4>Связь</h4>
          <ul>
            <li><a href="/contacts.html">Контакты и реквизиты</a></li>
            <li><a href="/download.html">Скачать</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__bottom">
        <span>© <span data-year>2026</span> Vaibo</span>
        <a href="/legal/">Правовая информация</a>
      </div>
    </div>
  </footer>
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def page(path, title, desc, body, extra=""):
    rel = "index.html" if path == "/" else path.lstrip("/")
    if rel.endswith("/"):
        rel += "index.html"
    out = SITE / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(title, desc, path, extra) + body + FOOT, encoding="utf-8")
    print("wrote", rel)


# ---------------------------------------------------------------- Иконки глав
ICON = {
    "recipes": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="22" cy="21" r="11"/><circle cx="22" cy="21" r="6"/><path d="M7 8v8a3 3 0 0 0 3 3v13M7 8v5M10 8v5M13 8v8a3 3 0 0 1-3 3"/></svg>',
    "plan": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="9" width="28" height="25" rx="5"/><path d="M6 16h28M13 5v7M27 5v7M15 25l4 4 7-8"/></svg>',
    "basket": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 15h24l-2.5 17a3 3 0 0 1-3 2.5h-13a3 3 0 0 1-3-2.5z"/><path d="M14 15V12a6 6 0 0 1 12 0v3"/><path d="M16 22v6M24 22v6"/></svg>',
    "parchment": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12 20 6l15 6-15 6z"/><path d="M5 12v14l15 7 15-7V12"/><circle cx="14" cy="13" r="1.6" fill="currentColor"/><circle cx="22" cy="10.5" r="1.6" fill="currentColor"/><circle cx="25" cy="15" r="1.6" fill="currentColor"/></svg>',
}

# ---------------------------------------------------------------- Пергамент (SVG)
BOARD_SVG = """<svg viewBox="0 0 500 380" aria-hidden="true">
            <g class="zones">
              <rect class="zone" x="40" y="40" width="190" height="130" rx="18"/>
              <rect class="zone" x="270" y="40" width="190" height="130" rx="18"/>
              <rect class="zone" x="40" y="210" width="190" height="130" rx="18"/>
              <rect class="zone" x="270" y="210" width="190" height="130" rx="18"/>
              <text class="zone-label" x="54" y="62">Картофель</text>
              <text class="zone-label" x="284" y="62">Морковь</text>
              <text class="zone-label" x="54" y="232">Помидоры</text>
              <text class="zone-label" x="284" y="232">Нут</text>
            </g>
            <g class="ing"><g transform="translate(135 112)">
              <g class="whole"><ellipse cx="-30" cy="0" rx="34" ry="24" fill="#c99a5b"/><ellipse cx="30" cy="8" rx="30" ry="21" fill="#bf8f50"/><circle cx="-40" cy="-6" r="2.5" fill="#8f6533"/><circle cx="-20" cy="6" r="2" fill="#8f6533"/><circle cx="34" cy="2" r="2.2" fill="#8f6533"/></g>
              <g class="piece" fill="#f0d68f" stroke="#c99a5b" stroke-width="2"><rect x="-62" y="-22" width="22" height="20" rx="5"/><rect x="-34" y="-14" width="22" height="20" rx="5"/><rect x="-6" y="-24" width="22" height="20" rx="5"/><rect x="22" y="-10" width="22" height="20" rx="5"/><rect x="-48" y="6" width="22" height="20" rx="5"/><rect x="-18" y="10" width="22" height="20" rx="5"/><rect x="12" y="14" width="22" height="20" rx="5"/></g>
            </g></g>
            <g class="ing"><g transform="translate(365 112)">
              <g class="whole"><path d="M-70 -6 Q-10 -24 52 -4 Q-10 18 -70 -6z" fill="#ee8a2f"/><path d="M52 -4 l18 -14 M52 -4 l20 -2 M52 -4 l16 10" stroke="#3d9a4c" stroke-width="5" stroke-linecap="round"/><path d="M-60 18 Q-4 4 44 22 Q-4 38 -60 18z" fill="#f29a3f"/></g>
              <g class="piece" fill="#f39b3e" stroke="#d9741f" stroke-width="2"><circle cx="-54" cy="-10" r="12"/><circle cx="-26" cy="-14" r="12"/><circle cx="2" cy="-10" r="12"/><circle cx="30" cy="-14" r="12"/><circle cx="-40" cy="18" r="12"/><circle cx="-12" cy="16" r="12"/><circle cx="16" cy="20" r="12"/><circle cx="44" cy="16" r="12"/></g>
            </g></g>
            <g class="ing"><g transform="translate(135 282)">
              <g class="whole"><circle cx="-34" cy="0" r="26" fill="#e2412f"/><circle cx="30" cy="4" r="24" fill="#d93a29"/><path d="M-34 -24 l-6 -8 M-34 -24 l7 -8 M-34 -24 l0 -10" stroke="#3d9a4c" stroke-width="4" stroke-linecap="round"/><circle cx="-42" cy="-8" r="5" fill="#fff" opacity=".35"/></g>
              <g class="piece"><path d="M-66 -6 a18 18 0 0 1 36 0z" fill="#e2412f"/><path d="M-26 -14 a18 18 0 0 1 36 0z" fill="#d93a29"/><path d="M14 -4 a18 18 0 0 1 36 0z" fill="#e2412f"/><path d="M-50 22 a18 18 0 0 1 36 0z" fill="#d93a29"/><path d="M-6 26 a18 18 0 0 1 36 0z" fill="#e2412f"/><circle cx="-48" cy="-10" r="2" fill="#f7d36b"/><circle cx="-8" cy="-18" r="2" fill="#f7d36b"/><circle cx="32" cy="-8" r="2" fill="#f7d36b"/></g>
            </g></g>
            <g class="ing"><g transform="translate(365 282)" fill="#e7c98b" stroke="#c9a565" stroke-width="2">
              <circle cx="-50" cy="-12" r="10"/><circle cx="-28" cy="-18" r="10"/><circle cx="-6" cy="-10" r="10"/><circle cx="16" cy="-18" r="10"/><circle cx="38" cy="-10" r="10"/><circle cx="-40" cy="10" r="10"/><circle cx="-18" cy="12" r="10"/><circle cx="4" cy="12" r="10"/><circle cx="26" cy="10" r="10"/><circle cx="48" cy="14" r="10"/><circle cx="-6" cy="32" r="10"/><circle cx="18" cy="32" r="10"/>
            </g></g>
            <g class="spice" fill="#7a4b1c"><circle cx="90" cy="96" r="2"/><circle cx="150" cy="130" r="2"/><circle cx="190" cy="100" r="2"/><circle cx="320" cy="96" r="2"/><circle cx="380" cy="130" r="2"/><circle cx="420" cy="100" r="2"/><circle cx="100" cy="270" r="2"/><circle cx="170" cy="300" r="2"/><circle cx="330" cy="270" r="2"/><circle cx="410" cy="300" r="2"/><circle cx="250" cy="190" r="2"/><circle cx="120" cy="110" r="1.6" fill="#3d9a4c"/><circle cx="350" cy="110" r="1.6" fill="#3d9a4c"/><circle cx="140" cy="290" r="1.6" fill="#3d9a4c"/><circle cx="380" cy="290" r="1.6" fill="#3d9a4c"/></g>
            <g class="steam" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity=".9"><path d="M150 40 q-12 -16 0 -32 q12 -16 0 -32"/><path d="M250 30 q-12 -16 0 -32 q12 -16 0 -32"/><path d="M350 40 q-12 -16 0 -32 q12 -16 0 -32"/></g>
          </svg>"""


def board(stage="0", badge="", autoplay=False):
    attrs = f'data-stage="{stage}"'
    if autoplay:
        attrs += ' data-autoplay data-labels="Лист на столе|Раскладка|Нарезка|Специи и масло|Запекание|Подача"'
    badge_html = f'<div class="board__badge">{badge}</div>' if badge else ""
    return f"""<div class="board" {attrs}>
          <div class="board__sheet">
          {BOARD_SVG}
          </div>
          {badge_html}
        </div>"""


# ---------------------------------------------------------------- Экраны приложения
BAR = '<div class="screen__bar"><span>9:41</span><span>●●●</span></div>'

SCREEN_RECIPE = '<div class="screen"><img src="/assets/img/screen-recipe.webp" alt="Экран Vaibo: пирог с творогом и яблоками, 1–2 часа, 6 порций, рецепт ВкусВилла" width="606" height="1320" loading="lazy"></div>'

SCREEN_PLAN = f"""<div class="screen">
              {BAR}
              <div class="screen__body">
                <div class="screen__h">План</div>
                <div class="screen__note">13–19 октября · 2 едока</div>
                <div class="s-day">Понедельник</div>
                <div class="s-card s-row"><div class="s-dot"><span>🥕</span></div><div><div class="s-title">Овощи и нут на пергаменте</div><div class="s-sub">Ужин · 45 мин · духовка</div></div><span class="s-pill">AR</span></div>
                <div class="s-day">Вторник</div>
                <div class="s-card s-row"><div class="s-dot"><span>🐟</span></div><div><div class="s-title">Лосось с брокколи</div><div class="s-sub">Ужин · 30 мин</div></div><span></span></div>
                <div class="s-day">Среда</div>
                <div class="s-card s-row"><div class="s-dot"><span>🍗</span></div><div><div class="s-title">Курица с гречкой</div><div class="s-sub">Обед · 40 мин</div></div><span></span></div>
                <div class="s-day">Четверг</div>
                <div class="s-card s-row"><div class="s-dot"><span>🥗</span></div><div><div class="s-title">Чечевичный салат</div><div class="s-sub">Ужин · 25 мин</div></div><span></span></div>
                <div class="s-card s-row" style="background:#eef3ff"><div class="s-dot" style="background:#fff"><span>⏰</span></div><div><div class="s-title">Начать готовить в 18:30</div><div class="s-sub">Напоминание на понедельник</div></div><span></span></div>
              </div>
            </div>"""

SCREEN_BASKET = f"""<div class="screen">
              {BAR}
              <div class="screen__body">
                <div class="screen__h">Покупки</div>
                <div class="screen__note">На 7 дней · 2 едока</div>
                <div class="s-card s-budget">
                  <div class="s-budget__top"><span class="s-sub">Бюджет на неделю</span><span class="s-sub">из 5 000 ₽</span></div>
                  <div class="s-num">4 120 ₽</div>
                  <div class="s-track"><div class="s-fill" style="--w:82%"></div></div>
                  <div class="s-sub">Цены ВкусВилла, проверены сегодня в 9:12</div>
                </div>
                <div class="s-card s-row s-row--check3"><span class="s-check"></span><div><div class="s-title">Нут, 400 г</div><div class="s-sub">2 упаковки</div></div><span class="s-val">258 ₽</span></div>
                <div class="s-card s-row s-row--check3"><span class="s-check"></span><div><div class="s-title">Брокколи, 400 г</div><div class="s-sub">1 упаковка</div></div><span class="s-val">189 ₽</span></div>
                <div class="s-card s-row s-row--check3"><span class="s-check"></span><div><div class="s-title">Картофель</div><div class="s-sub">1,2 кг</div></div><span class="s-val">96 ₽</span></div>
                <div class="s-card s-row s-row--check3"><span class="s-check on"></span><div><div class="s-title">Гречка</div><div class="s-sub">300 г</div></div><span class="s-pill">Есть дома</span></div>
                <div class="s-cta"><span>Открыть корзину ВкусВилла</span><span>›</span></div>
              </div>
            </div>"""

SCREEN_AR = f"""<div class="screen screen--ar">
              {BAR}
              {board("1", autoplay=True)}
              <div class="ar-hud"><b>Раскладка</b><span>Овощи и нут на пергаменте</span><div class="ar-progress"><i class="on"></i><i class="on"></i><i></i><i></i><i></i><i></i></div></div>
            </div>"""

SCREEN_SIGNIN = f"""<div class="screen">
              {BAR}
              <div class="screen__body" style="padding-top:3em;gap:0.9em">
                <img src="/assets/img/wordmark-blue.png" alt="" width="1567" height="312" style="width:56%;margin:0 auto 0.4em">
                <div class="screen__note" style="text-align:center">Вкусно, полезно и по карману</div>
                <div class="s-card s-row s-row--check"><span class="s-check on"></span><div class="s-sub" style="color:var(--ink)">Согласен на обработку персональных данных</div></div>
                <div class="s-card s-row s-row--check"><span class="s-check on"></span><div class="s-sub" style="color:var(--ink)">Сохранять мой пищевой профиль</div></div>
                <div class="s-card s-row s-row--check"><span class="s-check"></span><div class="s-sub" style="color:var(--ink)">Определять город по геопозиции</div></div>
                <div class="s-cta s-cta--black s-cta--center" style="margin-top:0.5em">Войти с Apple</div>
              </div>
            </div>"""

SCREEN_PROFILE = f"""<div class="screen">
              {BAR}
              <div class="screen__body">
                <div class="screen__h">Что не едите?</div>
                <div class="screen__note">Можно выбрать несколько</div>
                <div class="s-chips"><span class="s-chip">Грибы</span><span class="s-chip on">Кинза</span><span class="s-chip">Свинина</span><span class="s-chip on">Острое</span><span class="s-chip">Печень</span><span class="s-chip">Оливки</span></div>
                <div class="screen__h screen__h--sm">Аллергены</div>
                <div class="s-chips"><span class="s-chip">Глютен</span><span class="s-chip on">Молоко</span><span class="s-chip">Орехи</span><span class="s-chip">Яйца</span><span class="s-chip">Рыба</span></div>
                <div class="screen__h screen__h--sm">Что есть на кухне</div>
                <div class="s-chips"><span class="s-chip on">Духовка</span><span class="s-chip on">Плита</span><span class="s-chip">Мультиварка</span><span class="s-chip">Блендер</span></div>
                <div class="s-cta s-cta--center" style="margin-top:0.4em">Дальше</div>
              </div>
            </div>"""

SCREEN_BUDGET = f"""<div class="screen">
              {BAR}
              <div class="screen__body">
                <div class="screen__h">Бюджет</div>
                <div class="screen__note">Сколько готовы тратить на продукты</div>
                <div class="s-chips"><span class="s-chip">День</span><span class="s-chip on">Неделя</span><span class="s-chip">Месяц</span></div>
                <div class="s-card s-center"><div class="s-num s-num--xl">5 000 ₽</div><div class="s-sub">в неделю на 2 человек</div></div>
                <div class="screen__h screen__h--sm">Город</div>
                <div class="s-card s-row"><div class="s-dot"><span>📍</span></div><div><div class="s-title">Москва</div><div class="s-sub">Определили по геопозиции</div></div><span class="s-sub">Изменить</span></div>
                <div class="screen__h screen__h--sm">Время на готовку</div>
                <div class="s-chips"><span class="s-chip">до 20 мин</span><span class="s-chip on">до 45 мин</span><span class="s-chip">не важно</span></div>
                <div class="s-cta s-cta--center" style="margin-top:0.3em">Готово</div>
              </div>
            </div>"""

SCREEN_WEEK = SCREEN_PLAN.replace('<div class="screen__h">План</div>', '<div class="screen__h">Собрать неделю</div>').replace(
    '<div class="s-card s-row" style="background:#eef3ff"><div class="s-dot" style="background:#fff"><span>⏰</span></div><div><div class="s-title">Начать готовить в 18:30</div><div class="s-sub">Напоминание на понедельник</div></div><span></span></div>',
    '<div class="s-cta s-cta--center">Сохранить план</div>')

SCREEN_COOK = f"""<div class="screen">
              {BAR}
              <div class="screen__body">
                <div class="screen__note">Шаг 3 из 6</div>
                <div class="screen__h" style="font-size:1.5em">Нарежьте картофель кубиками 2 см, морковь кружками</div>
                <div class="s-card s-center"><div class="s-sub">Таймер</div><div class="s-num s-num--xl">12:00</div><div class="s-sub">Сообщим, даже если закроете приложение</div></div>
                <div class="s-chips"><span class="s-chip on">🔊 Озвучить шаг</span><span class="s-chip">Пергамент в AR</span></div>
                <div class="s-card s-row s-row--check3"><span class="s-check on"></span><div><div class="s-title">Картофель, 600 г</div></div><span></span></div>
                <div class="s-card s-row s-row--check3"><span class="s-check on"></span><div><div class="s-title">Морковь, 2 шт.</div></div><span></span></div>
                <div class="s-card s-row s-row--check3"><span class="s-check"></span><div><div class="s-title">Нут, 1 банка</div></div><span></span></div>
                <div class="s-cta s-cta--center">Следующий шаг</div>
              </div>
            </div>"""


def phone(screens):
    return f"""<div class="phone">
            <div class="phone__screen">
            {screens}
            </div>
          </div>"""


# ---------------------------------------------------------------- Главная
CHAPTERS = [
    ("recipes", "Рецепты.", "Блюда с фото, пошаговыми инструкциями и КБЖУ. Vaibo убирает то, что вы не едите, и учитывает аллергены, технику на кухне и время, которое вы готовы потратить.", "/features.html#recipes", "Все про рецепты", SCREEN_RECIPE),
    ("plan", "План на неделю.", "Одно касание, и у вас меню на 3–14 дней без повторов. Vaibo напомнит, когда пора ставить ужин, и перенесёт готовку в календарь iPhone.", "/how.html", "Как собирается план", SCREEN_PLAN),
    ("basket", "Покупки во ВкусВилле.", "Продукты из всех рецептов собираются в один список и пересчитываются на всех, кто ест. Отметьте, что уже есть дома, и Vaibo посчитает сумму по ценам ВкусВилла и откроет готовую корзину.", "/features.html#basket", "Про покупки и бюджет", SCREEN_BASKET),
    ("parchment", "Пергамент в AR.", "Наведите камеру на стол, и на нём появится лист с разметкой: куда положить продукты, как нарезать и когда отправлять в духовку. Ингредиенты в 3D можно покрутить и рассмотреть.", "/parchment.html", "Посмотреть пергамент", SCREEN_AR),
]

chapters_html = []
for key, bold, text, href, link, screen in CHAPTERS:
    chapters_html.append(f"""      <article class="chapter chapter--{key}">
        <div class="wrap wrap--wide chapter__inner">
          <div class="chapter__text">
            <div class="chapter__icon">{ICON[key]}</div>
            <p><b>{bold}</b> {text}</p>
            <a class="more" href="{href}">{link}</a>
          </div>
          <div class="chapter__media">
          {phone(screen)}
          </div>
        </div>
      </article>""")

stage_screens = "\n            ".join(c[5] for c in CHAPTERS)

INDEX = f"""
    <section class="hero">
      <div class="wrap intro">
        <img class="hero__wordmark" src="/assets/img/wordmark-blue.png" alt="vaibo" width="1567" height="312">
        <h1 class="display hero__title">Полезная еда, которая укладывается в бюджет</h1>
        <p class="lead hero__sub">Vaibo подбирает рецепты под ваш вкус, собирает меню на неделю и считает, сколько продукты будут стоить во ВкусВилле. А когда пора готовить, раскладывает рецепт прямо на вашем столе.</p>
        <div class="hero__cta">
          <a class="btn" href="/download.html">Скачать для iPhone</a>
          <a class="more" href="/how.html">Как это работает</a>
        </div>
      </div>
      <img class="hero__device" src="/assets/img/app-recipe.webp" alt="iPhone с открытым Vaibo: рецепт пирога с творогом и яблоками" width="668" height="1374" fetchpriority="high">
    </section>

    <section class="section">
      <div class="wrap center">
        <p class="statement">Каждый вечер одни и те же вопросы: что приготовить, что купить и хватит ли денег до зарплаты. Vaibo отвечает на них за пару минут, а вы спокойно готовите.</p>
      </div>
    </section>

    <section class="chapters" aria-label="Что умеет Vaibo">
      <div class="chapters__stage" aria-hidden="true">
        <div class="wrap wrap--wide">
          <div class="stage-slot">
          {phone(stage_screens)}
          </div>
        </div>
      </div>
{chr(10).join(chapters_html)}
    </section>

    <section class="section">
      <div class="wrap wrap--wide">
        <div class="center reveal">
          <h2 class="title">Деньги считаются сами</h2>
          <p class="lead" style="margin-top:16px">Укажите бюджет на день, неделю или месяц. Vaibo сверит с ним стоимость плана и подскажет, где можно сэкономить.</p>
        </div>
        <div class="tiles">
          <article class="tile tile--third reveal"><h3>Меню на 3–14 дней</h3><p>Короткий план, чтобы попробовать, или две недели, чтобы не думать о еде до зарплаты.</p><div class="tile__num">3–14</div></article>
          <article class="tile tile--third reveal" style="--delay:.08s"><h3>На всю семью</h3><p>Скажите, сколько человек едят, и количество продуктов пересчитается само.</p><div class="tile__num">×2</div></article>
          <article class="tile tile--third reveal" style="--delay:.16s"><h3>Что есть дома</h3><p>Отметьте гречку в шкафу и морковь в холодильнике. В корзину они не попадут.</p><div class="tile__num">−1</div></article>
          <article class="tile tile--blue reveal"><h3>Цены без сюрпризов</h3><p>Рядом с суммой видно, когда Vaibo проверил цены. Если у товара нет цены или фасовки, приложение честно напишет об этом и не станет угадывать итог.</p></article>
          <article class="tile reveal" style="--delay:.08s"><h3>Готовка по шагам</h3><p>Таймеры напомнят, даже если вы закрыли приложение. А шаг можно послушать, пока руки в муке.</p><a class="more" href="/features.html#cooking">Подробнее</a></article>
        </div>
      </div>
    </section>

    <section class="section section--soft">
      <div class="wrap wrap--wide">
        <div class="center reveal">
          <h2 class="title">Ваши данные остаются у вас</h2>
          <p class="lead" style="margin-top:16px">Мы просим только то, без чего не получится подобрать еду.</p>
        </div>
        <div class="facts">
          <div class="fact reveal"><b>Геопозиция только для города</b><p>Координаты нужны, чтобы определить город. Они не уходят с iPhone, а город можно выбрать и вручную.</p></div>
          <div class="fact reveal" style="--delay:.08s"><b>Камера ничего не записывает</b><p>Пергамент работает на самом iPhone. Видео не сохраняется и никуда не отправляется.</p></div>
          <div class="fact reveal" style="--delay:.16s"><b>Аккаунт удаляется в приложении</b><p>Перед удалением можно скачать все свои данные одним файлом.</p></div>
        </div>
        <p class="center reveal" style="margin-top:36px"><a class="more" href="/legal/privacy.html">Как мы обращаемся с данными</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap center">
        <h2 class="title reveal">Попробуйте Vaibo на iPhone</h2>
        <p class="lead reveal" style="margin-top:16px">Скоро в App Store.</p>
        <p class="reveal" style="margin-top:28px"><a class="btn" href="/download.html">Узнать о запуске</a></p>
      </div>
    </section>
"""
page("/", "Vaibo", "Vaibo подбирает полезные рецепты под ваш вкус и бюджет, собирает меню на неделю и корзину во ВкусВилле, а в AR показывает рецепт прямо на столе.", INDEX)

# ---------------------------------------------------------------- Как это работает
HOW_STEPS = [
    ("Шаг 1", "Войдите через Apple", "Без паролей и форм. Почту можно скрыть, Vaibo она не нужна. На этом же экране вы отдельно решаете, что разрешить: сохранять пищевой профиль, определять город по геопозиции.", SCREEN_SIGNIN),
    ("Шаг 2", "Расскажите, как вы едите", "Цель, любимые продукты, то, что вы терпеть не можете, аллергены и техника на кухне. Это пара минут, а потом рецепты подбираются без лишнего.", SCREEN_PROFILE),
    ("Шаг 3", "Назовите бюджет", "На день, неделю или месяц. Ещё город и сколько времени вы готовы стоять у плиты. Всё это можно поменять в профиле в любой момент.", SCREEN_BUDGET),
    ("Шаг 4", "Соберите неделю", "Нажмите «Собрать неделю», и Vaibo предложит меню на 3–14 дней. Блюда чередуются, а занятые дни остаются как были, если вы сами не попросите их заменить.", SCREEN_WEEK),
    ("Шаг 5", "Купите продукты", "Все ингредиенты собираются в один список. Отметьте, что уже есть дома, проверьте сумму по ценам ВкусВилла и откройте корзину. Заказ и оплату вы подтверждаете уже во ВкусВилле.", SCREEN_BASKET),
    ("Шаг 6", "Готовьте по шагам", "Каждый шаг с таймером и озвучкой. Если хочется наглядности, откройте пергамент в AR и раскладывайте продукты прямо по разметке на столе.", SCREEN_COOK),
]
steps_html = "\n".join(f"""          <article class="step">
            <div class="step__n">{n}</div>
            <h2 class="subtitle">{h}</h2>
            <p>{p}</p>
          </article>""" for n, h, p, _ in HOW_STEPS)
how_screens = "\n            ".join(s for *_, s in HOW_STEPS)
HOW = f"""
    <section class="page-head" style="border:0;padding-bottom:0">
      <div class="wrap center intro">
        <span class="eyebrow">Как это работает</span>
        <h1 class="display">От первого входа до ужина</h1>
        <p class="lead" style="margin-top:20px">Шесть шагов. Первые три вы проходите один раз, остальные каждую неделю.</p>
      </div>
    </section>

    <section class="story" data-story>
      <div class="wrap wrap--wide story__grid">
        <div class="story__stage">
          {phone(how_screens)}
        </div>
        <div class="story__list">
{steps_html}
        </div>
      </div>
    </section>

    <section class="section section--soft">
      <div class="wrap wrap--wide">
        <h2 class="title center reveal">Что ещё посмотреть</h2>
        <div class="cards">
          <a class="card reveal" href="/parchment.html"><h3>Пергамент в AR</h3><p>Как рецепт раскладывается прямо на вашем столе.</p><span class="more">Смотреть</span></a>
          <a class="card reveal" style="--delay:.08s" href="/features.html"><h3>Все возможности</h3><p>Рецепты, план, покупки, бюджет и готовка подробно.</p><span class="more">Открыть</span></a>
          <a class="card reveal" style="--delay:.16s" href="/faq.html"><h3>Вопросы</h3><p>Про цены, аллергии, данные и то, чего Vaibo пока не умеет.</p><span class="more">Читать</span></a>
        </div>
      </div>
    </section>
"""
page("/how.html", "Как это работает", "Как пользоваться Vaibo: вход через Apple, пищевой профиль, бюджет, план на неделю, покупки во ВкусВилле и готовка по шагам.", HOW)

# ---------------------------------------------------------------- Пергамент
AR_STEPS = [
    ("Лист на столе", "Положите лист", "Наведите камеру на стол или противень. Vaibo найдёт ровную поверхность и положит на неё пергамент с разметкой. Лист можно подвинуть, повернуть и подогнать по размеру."),
    ("Раскладка", "Разложите продукты", "На листе отмечено, где лежит каждый ингредиент. Продукты показаны в 3D: нажмите на помидор, чтобы покрутить его и рассмотреть со всех сторон."),
    ("Нарезка", "Нарежьте", "Целые овощи на листе превращаются в кусочки нужного вида. Сразу видно, что резать кубиком, а что кружками."),
    ("Специи и масло", "Добавьте специи", "Подсказка покажет, что посыпать и что перемешать. Кнопка «Показать движение» поднимет и повернёт модели, чтобы было понятно, что делать руками."),
    ("Запекание", "Отправьте в духовку", "Лист на экране прогревается, а рядом запускается таймер. Когда время выйдет, iPhone напомнит, даже если вы ушли в другую комнату."),
    ("Подача", "Подавайте", "Последняя подсказка про подачу. Прогресс сохраняется, поэтому можно отвлечься и потом вернуться ровно к тому же шагу."),
]
ar_steps_html = "\n".join(f"""          <article class="step" data-badge="{b}">
            <div class="step__n">Стадия {i + 1} из 6</div>
            <h2 class="subtitle">{h}</h2>
            <p>{p}</p>
          </article>""" for i, (b, h, p) in enumerate(AR_STEPS))
PARCH = f"""
    <section class="page-head parchment-bg" style="border:0">
      <div class="wrap center intro">
        <span class="eyebrow" style="color:#a0671f">Пергамент</span>
        <h1 class="display">Рецепт, разложенный прямо на столе</h1>
        <p class="lead" style="margin-top:20px">Помните пергаменты для запекания, где нарисовано, куда класть продукты? Мы сделали такой же в iPhone. Только он подстраивается под рецепт и показывает каждый шаг.</p>
      </div>
    </section>

    <section class="story story--ar" data-story>
      <div class="wrap wrap--wide story__grid">
        <div class="story__stage">
          {board("0", badge="Лист на столе")}
        </div>
        <div class="story__list">
{ar_steps_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap wrap--wide">
        <div class="center reveal">
          <h2 class="title">Что важно знать</h2>
        </div>
        <div class="facts">
          <div class="fact reveal"><b>Нужен iPhone с AR</b><p>Пергамент работает на iPhone с поддержкой ARKit. На остальных рецепт открывается в обычном пошаговом режиме.</p></div>
          <div class="fact reveal" style="--delay:.08s"><b>Камера только смотрит</b><p>Изображение обрабатывается на самом iPhone. Ничего не записывается и не отправляется.</p></div>
          <div class="fact reveal" style="--delay:.16s"><b>Не перегревает телефон</b><p>Если iPhone сильно нагрелся, Vaibo показывает меньше моделей и прямо говорит об этом.</p></div>
        </div>
        <p class="center reveal muted" style="margin:40px auto 0;max-width:60ch;color:var(--ink-2)">Пока Vaibo не распознаёт продукты и не понимает, готово ли блюдо. AR помогает с порядком действий, а текст шага остаётся главным. Следите за плитой и ножом, а не за экраном.</p>
      </div>
    </section>
"""
page("/parchment.html", "Пергамент", "Пергамент в AR: Vaibo раскладывает рецепт прямо на вашем столе, показывает ингредиенты в 3D и ведёт по шагам от нарезки до подачи.", PARCH)

# ---------------------------------------------------------------- Возможности
FEATURES = f"""
    <section class="page-head" style="border:0;padding-bottom:0">
      <div class="wrap center intro">
        <span class="eyebrow">Возможности</span>
        <h1 class="display">Всё, что есть в Vaibo сейчас</h1>
        <p class="lead" style="margin-top:20px">И немного о том, что мы делаем дальше.</p>
      </div>
    </section>

    <section class="section--tight" id="recipes">
      <div class="wrap wrap--wide">
        <h2 class="title reveal">Рецепты</h2>
        <div class="tiles" style="margin-top:32px">
          <article class="tile reveal"><h3>Каталог с фото и шагами</h3><p>Рецепты из каталога ВкусВилла с фотографиями, пошаговой инструкцией и КБЖУ на 100 грамм. Поиск работает по названию и продуктам.</p></article>
          <article class="tile reveal" style="--delay:.08s"><h3>Авторские блюда Vaibo</h3><p>Наши рецепты с точными граммовками и разметкой для пергамента в AR. Их становится больше с каждым обновлением.</p></article>
          <article class="tile tile--blue reveal"><h3>Только то, что вы едите</h3><p>Продукты, которые вы исключили, в подборку не попадают. Учитываются техника на кухне и время на готовку.</p></article>
          <article class="tile reveal" style="--delay:.08s"><h3>Аллергены</h3><p>Если вы отметили аллерген, Vaibo скрывает рецепты, где он есть, и те, где про аллергены ничего не известно. Этикетку на упаковке всё равно проверяйте.</p></article>
        </div>
      </div>
    </section>

    <section class="section--tight" id="plan">
      <div class="wrap wrap--wide">
        <h2 class="title reveal">План и напоминания</h2>
        <div class="tiles" style="margin-top:32px">
          <article class="tile tile--third reveal"><h3>Собрать неделю</h3><p>Меню на 3–14 дней одним нажатием, без повторов подряд.</p><div class="tile__num">3–14</div></article>
          <article class="tile tile--third reveal" style="--delay:.08s"><h3>Перенести</h3><p>Планы поменялись? Блюдо переезжает на другой день вместе с напоминанием.</p></article>
          <article class="tile tile--third reveal" style="--delay:.16s"><h3>Календарь iPhone</h3><p>По кнопке «В календарь» готовка появляется в вашем календаре. Повторный экспорт не плодит дубли.</p></article>
        </div>
      </div>
    </section>

    <section class="section--tight" id="basket">
      <div class="wrap wrap--wide">
        <h2 class="title reveal">Покупки и бюджет</h2>
        <div class="tiles" style="margin-top:32px">
          <article class="tile reveal"><h3>Один список на неделю</h3><p>Одинаковые продукты из разных рецептов складываются, количество пересчитывается на всех едоков.</p></article>
          <article class="tile reveal" style="--delay:.08s"><h3>Кладовая</h3><p>Отметьте, что уже лежит дома. Эти продукты не попадут ни в сумму, ни в корзину.</p></article>
          <article class="tile tile--blue reveal"><h3>Сумма по ценам ВкусВилла</h3><p>Vaibo ищет каждый продукт в каталоге ВкусВилла и считает, сколько нужно упаковок. Полный итог появляется, только если известна цена и фасовка каждой позиции.</p></article>
          <article class="tile reveal" style="--delay:.08s"><h3>Корзина по ссылке</h3><p>Найденные товары открываются готовой корзиной во ВкусВилле, до 20 позиций за раз. Заказ и оплату вы подтверждаете там.</p></article>
        </div>
      </div>
    </section>

    <section class="section--tight" id="cooking">
      <div class="wrap wrap--wide">
        <h2 class="title reveal">Готовка</h2>
        <div class="tiles" style="margin-top:32px">
          <article class="tile tile--third reveal"><h3>Таймеры</h3><p>Отсчёт не сбрасывается при закрытии экрана, а уведомление придёт вовремя.</p></article>
          <article class="tile tile--third reveal" style="--delay:.08s"><h3>Озвучка шагов</h3><p>iPhone читает шаг вслух русским голосом. Текст никуда не отправляется.</p></article>
          <article class="tile tile--third reveal" style="--delay:.16s"><h3>Пергамент в AR</h3><p>Рецепт раскладывается на столе, а ингредиенты можно покрутить в 3D.</p><a class="more" href="/parchment.html">Смотреть</a></article>
        </div>
      </div>
    </section>

    <section class="section section--soft">
      <div class="wrap">
        <h2 class="title center reveal">Что мы делаем дальше</h2>
        <div class="facts">
          <div class="fact reveal"><b>Другие магазины</b><p>Хотим сравнивать корзину в нескольких магазинах по вашему адресу. Подключим, когда получим официальный доступ к их ценам.</p></div>
          <div class="fact reveal" style="--delay:.08s"><b>Цены по адресу</b><p>Сейчас цена каталожная. Наличие, скидки в конкретном магазине и доставку пока показывает только ВкусВилл.</p></div>
          <div class="fact reveal" style="--delay:.16s"><b>Android</b><p>Сначала доводим до ума версию для iPhone, потом возьмёмся за Android.</p></div>
        </div>
      </div>
    </section>
"""
page("/features.html", "Возможности", "Рецепты с КБЖУ, план на 3–14 дней, общий список покупок, кладовая, сумма по ценам ВкусВилла, таймеры, озвучка и пергамент в AR.", FEATURES)

# ---------------------------------------------------------------- Вопросы
QA = [
    ("О приложении", [
        ("Для кого Vaibo?", ["Для тех, кто хочет есть дома нормальную еду, не тратить вечер на выбор рецептов и понимать, во сколько обойдутся продукты на неделю."]),
        ("Есть версия для Android?", ["Пока нет. Сначала доводим версию для iPhone, Android будет следующим."]),
        ("Это диета?", ["Нет. Vaibo помогает питаться разнообразно и укладываться в бюджет. Худеть, держать вес или набирать, решаете вы, а меню подстраивается под цель."]),
        ("Будут рестораны или соцсеть?", ["Нет, Vaibo про домашнюю еду. Мы сознательно не делаем ленту отзывов и поиск кафе."]),
    ]),
    ("Цены и покупки", [
        ("Почему корзина только во ВкусВилле?", ["У ВкусВилла есть официальный открытый сервис для приложений: через него можно честно искать товары и собирать корзину. Другие магазины подключим, когда договоримся об официальном доступе. Копировать цены с чужих сайтов мы не будем."]),
        ("Цена в Vaibo совпадёт с ценой в магазине?", ["Не всегда. Мы показываем цену из каталога ВкусВилла и время, когда её проверили. Наличие, скидки по адресу и доставку ВкусВилл покажет при оформлении."]),
        ("Vaibo сам закажет продукты?", ["Нет. Vaibo собирает корзину и открывает её во ВкусВилле. Заказ и оплату вы подтверждаете сами."]),
    ]),
    ("Здоровье", [
        ("У меня аллергия. Можно доверять фильтру?", ["Фильтр скрывает рецепты с выбранным аллергеном и те, где данных об аллергенах нет. Но состав на упаковке и предупреждения о следах аллергенов всё равно проверяйте сами.", "Vaibo не медицинский сервис и не заменяет врача."]),
        ("Откуда КБЖУ?", ["Для рецептов из каталога это данные на 100 грамм от источника рецепта. Цифры ориентировочные: реальные продукты и способ готовки их немного меняют."]),
    ]),
    ("Данные и безопасность", [
        ("Что видит камера в AR?", ["Камера нужна, чтобы найти стол. Изображение обрабатывается на iPhone и не сохраняется."]),
        ("Зачем геопозиция?", ["Только чтобы определить город. Координаты не отправляются на сервер, а город можно выбрать вручную."]),
        ("Как удалить аккаунт?", ["В приложении, в разделе профиля. Перед удалением можно выгрузить свои данные. Если вы входили через Apple, Vaibo попросит подтвердить вход ещё раз, чтобы отозвать доступ."]),
    ]),
]
qa_html = []
for group, items in QA:
    inner = "\n".join(
        f'          <div class="qa__item"><h3>{q}</h3>' + "".join(f"<p>{a}</p>" for a in ans) + "</div>" for q, ans in items
    )
    qa_html.append(f'        <div class="qa-group reveal"><h2>{group}</h2>\n{inner}\n        </div>')
FAQ = f"""
    <section class="page-head" style="border:0">
      <div class="wrap center intro">
        <span class="eyebrow">Вопросы</span>
        <h1 class="display">Что нас спрашивают</h1>
        <p class="lead" style="margin-top:20px">Не нашли ответ? Напишите на {MAIL}, отвечаем в рабочие дни.</p>
      </div>
    </section>
    <section class="section--tight" style="padding-top:0">
      <div class="wrap qa">
{chr(10).join(qa_html)}
      </div>
    </section>
"""
page("/faq.html", "Вопросы", "Ответы на частые вопросы о Vaibo: цены и корзина ВкусВилла, аллергены, AR, геопозиция и удаление аккаунта.", FAQ)

# ---------------------------------------------------------------- Скачать
APPLE_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9-1.7 0-3.3 1-4.2 2.6-1.8 3.1-.5 7.7 1.3 10.2.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8s2 .8 3.4.8c1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.7-1-2.7-4.1zM13.9 5c.7-.9 1.2-2 1-3.2-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.1 1.2.1 2.3-.6 3.1-1.5z"/></svg>'
DOWNLOAD = f"""
    <section class="section" style="padding-bottom:40px">
      <div class="wrap center intro">
        <img src="/assets/img/icon-blue-640.webp" alt="Иконка Vaibo" width="640" height="640" style="width:132px;margin:0 auto 30px;border-radius:30px">
        <h1 class="display">Vaibo для iPhone</h1>
        <p class="lead" style="margin-top:20px">Приложение готовится к выходу в App Store. Когда оно появится, кнопка ниже откроет страницу Vaibo в магазине.</p>
        <p style="margin-top:34px">
          <!-- TODO: заменить href на ссылку из App Store Connect после публикации -->
          <a class="store" href="#">{APPLE_SVG}<span><small>Скоро в</small>App Store</span></a>
        </p>
      </div>
    </section>
    <section class="section--tight">
      <div class="wrap wrap--wide">
        <div class="facts">
          <div class="fact reveal"><b>Только iPhone</b><p>Версия для Android появится позже.</p></div>
          <div class="fact reveal" style="--delay:.08s"><b>Вход через Apple</b><p>Без паролей. Почту можно скрыть, приложению она не нужна.</p></div>
          <div class="fact reveal" style="--delay:.16s"><b>Пергамент на iPhone с AR</b><p>Остальные функции работают на любом iPhone с актуальной iOS.</p></div>
        </div>
        <p class="center reveal" style="margin-top:40px;color:var(--ink-2)">Устанавливая Vaibo, вы принимаете <a href="/legal/terms.html">пользовательское соглашение</a>.</p>
      </div>
    </section>
"""
page("/download.html", "Скачать", "Vaibo для iPhone скоро в App Store.", DOWNLOAD)

# ---------------------------------------------------------------- Документы


def p(*xs):
    return "\n".join(f"        <p>{x}</p>" for x in xs)


def ul(*xs):
    return "        <ul>\n" + "\n".join(f"          <li>{x}</li>" for x in xs) + "\n        </ul>"


REQ = f"""        <div class="table-wrap"><table>
          <tr><th>Наименование</th><td>{OPERATOR}</td></tr>
          <tr><th>ИНН</th><td>{INN}</td></tr>
          <tr><th>ОГРН / ОГРНИП</th><td>{OGRN}</td></tr>
          <tr><th>Адрес</th><td>{ADDRESS}</td></tr>
          <tr><th>Почта</th><td>{MAIL}</td></tr>
        </table></div>"""


def legal_doc(path, title, desc, intro, summary, sections):
    toc = "\n".join(f'          <li><a href="#s{i}">{h}</a></li>' for i, (h, _) in enumerate(sections, 1))
    secs = "\n".join(f'        <h2 id="s{i}">{i}. {h}</h2>\n{html}' for i, (h, html) in enumerate(sections, 1))
    summ = "".join(f"<p>{x}</p>" for x in summary)
    body = f"""    <section class="page-head">
      <div class="wrap wrap--wide">
        <a class="more" href="/legal/" style="font-size:14px">Все документы</a>
        <h1 class="title" style="margin-top:14px">{title}</h1>
        <p class="lead">{intro} Редакция от {UPDATED}</p>
      </div>
    </section>
    <div class="wrap wrap--wide legal">
      <nav class="legal__toc" aria-label="Содержание">
        <h2>Содержание</h2>
        <ol>
{toc}
        </ol>
      </nav>
      <article class="legal__body">
        <div class="summary"><p><b>Коротко</b></p>{summ}<p class="summary__note">Это пересказ простыми словами. Юридическую силу имеет текст ниже.</p></div>
{secs}
      </article>
    </div>
"""
    page(path, title, desc, body)


legal_doc(
    "/legal/privacy.html", "Политика обработки персональных данных",
    "Какие данные обрабатывает Vaibo, зачем, где они хранятся и как их удалить.",
    "Принята в соответствии с Федеральным законом от 27.07.2006 № 152-ФЗ «О персональных данных».",
    [
        "Мы храним только то, что нужно для подбора еды: аккаунт Apple, пищевой профиль и бюджет.",
        "Геопозиция, камера, голос и календарь работают на вашем iPhone. Эти данные к нам не приходят.",
        "Данные хранятся в России. Их можно выгрузить или удалить прямо в приложении.",
    ],
    [
        ("Кто оператор", p(
            f"Оператор персональных данных: {OPERATOR}, ИНН {INN}, ОГРН/ОГРНИП {OGRN}, адрес: {ADDRESS}.",
            f"Сведения об операторе внесены в реестр операторов персональных данных Роскомнадзора, регистрационный номер {T('номер в реестре')}.",
            f"По любым вопросам о данных пишите на {PMAIL}.",
        )),
        ("Что мы получаем и храним", "        <h3>Аккаунт</h3>\n" + ul(
            "идентификатор Apple ID и адрес почты, который передаёт Apple (это может быть скрытый адрес);",
            "имя, если вы разрешили Apple его передать;",
            "фото профиля, если вы сами его загрузили;",
            "даты и версии согласий, которые вы дали.",
        ) + "\n        <h3>Пищевой профиль</h3>\n" + ul(
            "цель (снизить, удержать или набрать вес), число едоков, город;",
            "любимые и исключённые продукты, выбранные аллергены, техника на кухне, время на готовку;",
            "бюджет и его период: день, неделя или месяц.",
        ) + p(
            "Пищевой профиль сохраняется на сервере только с вашего отдельного согласия. Без него профиль хранится только на iPhone.",
            "Мы не спрашиваем о диагнозах и заболеваниях. Аллерген в Vaibo означает продукт, который нужно убрать из рецептов, и не связывается с медицинскими сведениями.",
        ) + "\n        <h3>Технические данные</h3>\n" + ul(
            "версия приложения и iOS, сведения о сбоях;",
            "IP-адрес при обращении к серверу.",
        )),
        ("Что остаётся на iPhone", ul(
            "<b>Геопозиция.</b> Координаты используются на устройстве, чтобы выбрать ближайший город. На сервер они не отправляются.",
            "<b>Камера.</b> Изображение для пергамента в AR обрабатывается на iPhone средствами Apple ARKit. Видео и фото не сохраняются и не передаются.",
            "<b>Озвучка шагов.</b> Текст читает встроенный синтезатор речи iPhone.",
            "<b>Календарь.</b> Vaibo создаёт события готовки только после нажатия «В календарь» и проверяет календарь лишь на свои события, чтобы не делать дубликатов.",
            "<b>Уведомления.</b> Напоминания и таймеры создаются локально на iPhone.",
            "<b>План, кладовая и корзина.</b> Хранятся на iPhone.",
        )),
        ("Зачем", ul(
            "создать аккаунт и войти через Apple;",
            "подобрать рецепты и составить план питания;",
            "собрать список покупок и проверить цены;",
            "отвечать на обращения;",
            "исправлять ошибки и делать приложение стабильнее.",
        ) + p("Мы не продаём данные и не используем их для рекламы.")),
        ("Основания", p(
            "Ваше согласие (п. 1 ч. 1 ст. 6 152-ФЗ) и исполнение пользовательского соглашения, стороной которого вы являетесь (п. 5 ч. 1 ст. 6 152-ФЗ).",
            'Согласия оформлены <a href="/legal/consent.html">отдельными документами</a>. Каждое можно дать или отозвать независимо от других.',
        )),
        ("Кому передаются данные", ul(
            f"<b>Хостинг.</b> Сервер, где хранятся аккаунт и профиль: {HOSTING}.",
            "<b>Apple.</b> Вход через Apple ID проходит у Apple. При удалении аккаунта мы просим Apple отозвать доступ Vaibo.",
            "<b>ВкусВилл.</b> Для поиска товаров и сборки корзины во ВкусВилл уходят названия продуктов. Ваше имя, почта и профиль не передаются. Заказ вы оформляете уже во ВкусВилле по его правилам.",
            "<b>Государственные органы</b>, если этого прямо требует закон.",
        ) + p(f"Трансграничная передача персональных данных {T('не осуществляется / осуществляется в … после уведомления Роскомнадзора')}.")),
        ("Где и сколько храним", p(
            "Запись, систематизация, накопление, хранение, уточнение и извлечение персональных данных граждан России ведутся в базах данных на территории Российской Федерации.",
            "Данные хранятся, пока у вас есть аккаунт. После удаления аккаунта они удаляются с сервера в течение 30 дней, кроме сведений, которые закон требует хранить дольше.",
        )),
        ("Защита", ul(
            "шифрование соединения между приложением и сервером;",
            "доступ к записям в базе только у их владельца, на уровне правил самой базы;",
            "секретные ключи хранятся только на сервере, не в приложении;",
            "оценка вреда и модель угроз по требованиям 152-ФЗ и постановления Правительства РФ № 1119.",
        ) + p("Если случится утечка, мы сообщим в Роскомнадзор в течение 24 часов и предупредим пользователей, которых она затронула.")),
        ("Ваши права", ul(
            "узнать, какие данные о вас есть и как они используются;",
            "выгрузить свои данные в приложении;",
            "исправить или удалить данные, отозвать согласие;",
            "удалить аккаунт в приложении;",
            "пожаловаться в Роскомнадзор или в суд.",
        ) + p(f"Запросы можно отправить на {PMAIL}. Ответим в течение 10 рабочих дней. Срок можно продлить ещё на 5 рабочих дней, если мы объясним причину.")),
        ("Дети", p("Vaibo рассчитан на взрослых. Если вам меньше 18 лет, пользуйтесь приложением с согласия родителей или законных представителей.")),
        ("Изменения", p("Если поменяется закон или то, как работает Vaibo, мы обновим политику. Действующая редакция всегда на этой странице, а о важных изменениях расскажем в приложении.")),
    ],
)

legal_doc(
    "/legal/consent.html", "Согласия на обработку данных",
    "Тексты согласий, которые пользователь даёт в приложении Vaibo.",
    "Каждое согласие вы даёте отдельно, отмечая его в приложении. Ни одно не отмечено заранее.",
    [
        "Первое согласие нужно, чтобы работал аккаунт. Без него войти не получится.",
        "Второе разрешает хранить пищевой профиль на сервере. Без него профиль останется только на iPhone.",
        "Любое согласие можно отозвать в настройках приложения или письмом.",
    ],
    [
        ("Согласие на обработку персональных данных для аккаунта", p(
            f"Я свободно, своей волей и в своём интересе даю согласие {OPERATOR}, ИНН {INN}, адрес: {ADDRESS} (Оператор), на обработку моих персональных данных: идентификатора Apple ID, адреса электронной почты, имени (если передано), фото профиля (если загружено), сведений о данных мною согласиях, технических данных устройства и IP-адреса.",
            "Цель: регистрация и работа учётной записи в приложении Vaibo, исполнение пользовательского соглашения, ответы на обращения.",
            "Действия: сбор, запись, систематизация, накопление, хранение, уточнение, извлечение, использование, передача хостинг-провайдеру Оператора, блокирование, удаление, уничтожение, с использованием средств автоматизации.",
            "Срок: до удаления учётной записи или отзыва согласия.",
        )),
        ("Согласие на хранение пищевого профиля", p(
            "Я даю Оператору согласие на обработку сведений о моих пищевых предпочтениях: цели по весу, числе едоков, городе, любимых и исключённых продуктах, выбранных аллергенах, кухонной технике, времени на готовку и бюджете.",
            "Цель: подбор рецептов и плана питания, синхронизация профиля между устройствами.",
            "Действия и срок: те же, что в согласии для аккаунта.",
            "Я понимаю, что Vaibo не является медицинским сервисом, а аллерген в профиле означает продукт, который нужно исключить из рецептов.",
        )),
        ("Как отозвать", p(
            f"Отозвать любое согласие можно в настройках приложения или письмом на {PMAIL}. Оператор прекратит обработку и удалит данные в течение 30 дней, если закон не разрешает продолжить обработку без согласия.",
            "Отзыв согласия на пищевой профиль не удаляет аккаунт: профиль останется только на вашем iPhone.",
        )),
        ("Подтверждение", p('Отмечая согласие, я подтверждаю, что прочитал <a href="/legal/privacy.html">Политику обработки персональных данных</a> и что мне исполнилось 18 лет либо согласие даёт мой законный представитель.')),
    ],
)

legal_doc(
    "/legal/terms.html", "Пользовательское соглашение",
    "Правила пользования приложением Vaibo и сайтом vaibofood.ru.",
    "Правила пользования приложением Vaibo и сайтом vaibofood.ru.",
    [
        "Vaibo помогает выбирать рецепты, планировать питание и покупки. Это не медицинский сервис.",
        "Цены в приложении справочные. Окончательную стоимость показывает магазин при заказе.",
        "Во время готовки следите за плитой и ножом, а не за экраном.",
    ],
    [
        ("Стороны", p(
            f"Соглашение заключается между {OPERATOR} (далее «мы») и вами как пользователем приложения Vaibo и сайта vaibofood.ru.",
            "Устанавливая приложение или входя в аккаунт, вы принимаете эти правила. Если не согласны, не пользуйтесь сервисом.",
        )),
        ("Что делает Vaibo", ul(
            "подбирает рецепты по вашему профилю;",
            "составляет план питания и напоминает о готовке;",
            "собирает список покупок и показывает цены из каталога ВкусВилла;",
            "открывает корзину во ВкусВилле;",
            "показывает шаги рецепта, в том числе в дополненной реальности.",
        )),
        ("Цены и магазины", p(
            "Цены берутся из каталога ВкусВилла на момент проверки и могут отличаться от цены в конкретном магазине. Мы не продаём продукты. Заказ, оплату, доставку и возврат вы оформляете у магазина по его правилам.",
        )),
        ("Здоровье и безопасность", p(
            "Vaibo не оказывает медицинских услуг, не ставит диагнозы и не подбирает лечебное питание. КБЖУ ориентировочные. Фильтр аллергенов скрывает рецепты по известным данным, но не гарантирует отсутствие аллергена: проверяйте состав на упаковке.",
            "Подсказки в AR показывают порядок действий и не распознают продукты или готовность блюда. Соблюдайте технику безопасности на кухне и доводите мясо, птицу, рыбу и яйца до готовности.",
        )),
        ("Аккаунт", p(
            "Вход выполняется через Apple ID. Вы отвечаете за доступ к своему устройству. Удалить аккаунт и выгрузить данные можно в приложении.",
        )),
        ("Чего делать нельзя", ul(
            "взламывать приложение, обходить ограничения и автоматически собирать данные из него;",
            "копировать и распространять рецепты и материалы Vaibo без разрешения;",
            "использовать сервис для действий, нарушающих закон.",
        )),
        ("Права на материалы", p("Приложение, дизайн, авторские рецепты, 3D-модели и товарный знак Vaibo принадлежат нам. Рецепты и фото из каталога ВкусВилла принадлежат их правообладателям и показываются с их сервиса.")),
        ("Как подбираются рецепты", p("Подборка строится по правилам, которые вы задаёте сами: цель, исключённые продукты, аллергены, техника, время и бюджет. Мы объясняем, почему предложено блюдо, и не используем для подбора данные, которых вы не указывали.")),
        ("Ответственность", p("Мы стараемся, чтобы Vaibo работал без сбоев, но не гарантируем, что внешние сервисы (Apple, ВкусВилл) всегда доступны. Это соглашение не ограничивает ваши права потребителя по закону.")),
        ("Изменения и связь", p(f"Мы можем обновлять соглашение. Новая редакция действует с момента публикации, о важных изменениях сообщим в приложении. Вопросы присылайте на {MAIL}.") + "\n" + REQ),
    ],
)

legal_doc(
    "/legal/offer.html", "Оферта",
    "Условия платных функций Vaibo.",
    "Условия платных функций Vaibo, если они появятся в приложении.",
    [
        "Сейчас Vaibo можно пользоваться без оплаты. Когда появятся платные функции, условия будут здесь.",
        "Покупки внутри приложения проходят через App Store, отменить подписку можно в настройках Apple ID.",
    ],
    [
        ("Статус", p(f"На дату этой редакции платных функций в Vaibo {T('нет / перечислить тарифы')}. Этот документ описывает, как они будут работать.")),
        ("Как оплачивать", p("Оплата проходит через App Store по правилам Apple. Цена и состав тарифа показываются до оплаты. Подписка продлевается автоматически, если не отключить её в настройках Apple ID минимум за 24 часа до конца периода.")),
        ("Возврат", p("Возврат за покупки в App Store оформляется через Apple. Если что-то не работало по нашей вине, напишите нам, разберёмся и поможем с возвратом.")),
        ("Продукты", p("Продукты продаёт магазин, а не Vaibo. Оплата подписки Vaibo не включает стоимость продуктов и доставки.")),
        ("Реквизиты", REQ),
    ],
)

legal_doc(
    "/legal/cookies.html", "Cookies",
    "Использует ли сайт vaibofood.ru cookies.",
    "Использует ли сайт vaibofood.ru cookies и счётчики.",
    ["Сейчас сайт не ставит cookies и не подключает счётчики. Шрифты и картинки загружаются с нашего же сервера."],
    [
        ("Что сейчас", p("Сайт vaibofood.ru не использует cookies, счётчики посещений и сторонние скрипты.")),
        ("Если это изменится", p("Если мы подключим статистику, например Яндекс Метрику, сайт сначала спросит разрешения, а здесь появится список cookies и сроков их хранения.")),
        ("Контакты", p(f"Вопросы присылайте на {PMAIL}.")),
    ],
)

cards = [
    ("/legal/terms.html", "Пользовательское соглашение", "Что делает Vaibo, правила и ответственность."),
    ("/legal/privacy.html", "Обработка персональных данных", "Что мы храним, где и как это удалить."),
    ("/legal/consent.html", "Согласия", "Тексты согласий, которые вы даёте в приложении."),
    ("/legal/offer.html", "Оферта", "Условия платных функций."),
    ("/legal/cookies.html", "Cookies", "Сайт сейчас не использует cookies."),
    ("/contacts.html", "Контакты и реквизиты", "Кто мы и как с нами связаться."),
]
cards_html = "\n".join(f'      <a class="card reveal" href="{h}"><h3>{t}</h3><p>{d}</p><span class="more">Открыть</span></a>' for h, t, d in cards)
page("/legal/", "Правовая информация", "Документы Vaibo: соглашение, политика обработки персональных данных, согласия, оферта.", f"""    <section class="page-head" style="border:0;padding-bottom:0">
      <div class="wrap wrap--wide">
        <h1 class="title">Правовая информация</h1>
        <p class="lead">В начале каждого документа есть короткий пересказ простыми словами.</p>
      </div>
    </section>
    <div class="wrap wrap--wide doc-list">
{cards_html}
    </div>
""")

page("/contacts.html", "Контакты", "Как связаться с командой Vaibo. Реквизиты.", f"""    <section class="page-head" style="border:0;padding-bottom:0">
      <div class="wrap wrap--wide">
        <h1 class="title">Напишите нам</h1>
        <p class="lead">Вопрос про приложение, идея или предложение о партнёрстве. Отвечаем в рабочие дни, обычно в течение суток.</p>
      </div>
    </section>
    <div class="wrap wrap--wide">
      <div class="contacts">
        <div class="contact reveal"><h2>Поддержка</h2><strong>{MAIL}</strong><p>Всё про приложение.</p></div>
        <div class="contact reveal" style="--delay:.08s"><h2>Персональные данные</h2><strong>{PMAIL}</strong><p>Выгрузка, удаление, отзыв согласия.</p></div>
        <div class="contact reveal" style="--delay:.16s"><h2>Партнёрам</h2><strong>partners@vaibofood.ru</strong><p>Магазины, производители, пресса.</p></div>
      </div>
      <div class="legal__body" style="padding-bottom:110px">
        <h2>Реквизиты</h2>
        <div class="table-wrap"><table>
          <tr><th>Наименование</th><td>{OPERATOR}</td></tr>
          <tr><th>ИНН</th><td>{INN}</td></tr>
          <tr><th>ОГРН / ОГРНИП</th><td>{OGRN}</td></tr>
          <tr><th>Адрес</th><td>{ADDRESS}</td></tr>
          <tr><th>Телефон</th><td>{T('+7 …')}</td></tr>
          <tr><th>Реестр операторов ПДн</th><td>{T('номер Роскомнадзора')}</td></tr>
        </table></div>
      </div>
    </div>
""")

page("/404.html", "Страница не найдена", "Такой страницы нет.", """    <section class="notfound">
      <div class="wrap">
        <img src="/assets/img/wordmark-blue.png" alt="vaibo" width="1567" height="312" style="width:180px;margin:0 auto 28px">
        <h1 class="title">Здесь пусто, как в холодильнике в воскресенье</h1>
        <p class="lead" style="margin:18px auto 30px">Такой страницы нет, зато рецепты на неделю есть.</p>
        <a class="btn" href="/">На главную</a>
      </div>
    </section>
""", extra='  <meta name="robots" content="noindex">\n')
