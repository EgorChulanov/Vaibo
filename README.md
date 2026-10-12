# Vaibo

Сайт приложения Vaibo: **vaibofood.ru**. Статичный, без сборщиков и зависимостей.

## Страницы

| Файл | Что на странице |
|---|---|
| `site/index.html` | Обзор: главный экран, цветные главы как на странице Apple TV |
| `site/how.html` | Как это работает: шесть шагов с экраном приложения |
| `site/parchment.html` | Пергамент в AR, стадии готовки на анимированном листе |
| `site/features.html` | Возможности и что в планах |
| `site/faq.html` | Вопросы |
| `site/download.html` | Скачать (пока «Скоро в App Store») |
| `site/contacts.html`, `site/legal/` | Контакты, реквизиты и документы |

## Как менять тексты

Шапка, подвал и тексты всех страниц собраны в одном файле `tools/build_pages.py`. Поправьте текст там и пересоберите:

```bash
python3 tools/build_pages.py site
```

Стили в `site/assets/css/styles.css`, анимации в `site/assets/js/main.js`.

## Посмотреть локально

```bash
cd site && python3 -m http.server 8000
# http://localhost:8000
```

## Шрифт

Onest, лицензия SIL Open Font License (бесплатно, в том числе для коммерции). Файлы лежат в `site/assets/fonts` вместе с текстом лицензии, сайт не ходит за шрифтом в Google.

## Что заполнить перед запуском

На сайте всё незаполненное подсвечено жёлтым:

```bash
grep -rn 'class="todo"' site
```

- реквизиты, номер в реестре Роскомнадзора, хостинг в России;
- ссылка на App Store в `download.html` (сейчас `href="#"`);
- почтовые ящики `hello@`, `privacy@`, `partners@vaibofood.ru`.

## Публикация

Подробно в [docs/launch-guide.md](docs/launch-guide.md): домен, DNS, юридический чек-лист, реестры, App Store.
