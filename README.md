# Vaibo

Сайт сервиса Vaibo: **vaibofood.ru**. Статичный, без сборки и зависимостей: HTML, CSS и немного JavaScript.

## Структура

```
site/                  ← всё, что публикуется на vaibofood.ru
  index.html           главная (структура в духе apple.com/apple-tv-4k)
  contacts.html        контакты и реквизиты
  legal/               оферта, соглашение, политика ПДн, согласие, cookies
  404.html
  assets/css|js|img    стили, анимации, иконки
  CNAME                домен для GitHub Pages
docs/launch-guide.md   домен, хостинг, юридический чек-лист, реестры и льготы
.github/workflows/     автодеплой сайта на GitHub Pages
```

## Посмотреть локально

```bash
cd site
python3 -m http.server 8000
# открыть http://localhost:8000
```

## Что заполнить перед запуском

Все места, которые нужно заменить, на сайте подсвечены жёлтым (`class="todo"`). Найти их:

```bash
grep -rn 'class="todo"' site
grep -rn 'href="#"' site/index.html   # ссылки на App Store, RuStore, Google Play
```

- реквизиты: ИП или ООО, ИНН, ОГРН, адрес, телефон, расчётный счёт;
- номер в реестре операторов персональных данных Роскомнадзора;
- хостинг в РФ, где хранятся данные пользователей приложения;
- название магазина-партнёра для корзины;
- ссылки на приложение в сторах;
- список 13 стилей питания в `site/index.html` (сверить с приложением);
- почтовые ящики `hello@`, `privacy@`, `partners@vaibofood.ru` (создать на домене).

## Публикация

Подробно в [docs/launch-guide.md](docs/launch-guide.md). Коротко:

1. GitHub → Settings → Pages → Source: **GitHub Actions**.
2. Влить ветку в `main`, сайт задеплоится сам.
3. В reg.ru пройти идентификацию через Госуслуги и прописать DNS-записи для GitHub Pages.
