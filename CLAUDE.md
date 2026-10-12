# CLAUDE.md — cv-portfolio

Сайт-портфолио и резюме: Maksym Kasianov, Manual QA Engineer и разработчик приложений. Публикуется на GitHub Pages: `https://moslyharmless.github.io/cv-portfolio/` (репозиторий `MoslyHarmless/cv-portfolio`, ветка `main`).

С владельцем общаться по-русски.

## Важно: здесь лежит собранный сайт, а не исходники

`index.html` подключает файлы с хешами в именах (`assets/index-DgNdEhsC.js`, `assets/index-BsM75ylq.css`, `assets/hero3d-*.js`, `assets/three-*.js`). Это результат сборки Vite с Three.js. Исходников (`src/`, `package.json`) в репозитории нет.

Следствия:
- JS и CSS в `assets/` минифицированы — править их руками нельзя.
- Изменить вёрстку, тексты секций или 3D-сцену можно только в исходном проекте с последующей пересборкой. Если владелец просит такую правку, сначала спроси, где исходники.
- Руками можно править то, что лежит вне бандла: мета-теги и JSON-LD в `index.html`, `robots.txt`, `sitemap.xml`, файлы резюме, `og.svg`/`og.png`, `favicon.svg`.

## Где что лежит

| Путь | Что это |
|---|---|
| `index.html` | Оболочка страницы: SEO-мета, Open Graph, подключение бандла |
| `assets/` | Собранные JS и CSS (не править) |
| `cv/CV_Maksym_Kasianov_QA_EN.pdf`, `cv/CV_Maksym_Kasianov_QA_UA.pdf` | Резюме для скачивания с сайта |
| `CV_Maksym_Kasianov_QA_EN.md`, `CV_Maksym_Kasianov_QA_UK.md` | Текстовые исходники резюме |
| `og.svg`, `og.png`, `favicon.svg` | Картинка для соцсетей и иконка |
| `robots.txt`, `sitemap.xml`, `.nojekyll` | Служебные файлы GitHub Pages |
| `14.08.2026 Project Review.md` | Старый обзор; часть замечаний уже неактуальна (OG-теги добавлены) |

## Команды

```bash
python -m http.server 8080    # http://localhost:8080
```

Выкладка — push в `main`. Сайт живёт в подпапке `/cv-portfolio/`, поэтому пути к ресурсам должны оставаться относительными.

## Правила

- Факты резюме (опыт, даты, навыки, контакты) не выдумывать и не «улучшать» без владельца.
- Правка резюме: менять `.md` в обеих языковых версиях и напомнить владельцу, что PDF в `cv/` нужно пересобрать — сам он не обновится.
- После смены `og.svg` пересоздать `og.png` (1200×630).

## Скилы

Проектных скилов нет: в репозитории нечего собирать и тестировать.

Установленные, которые здесь уместны:
- `searchfit-seo:seo-check`, `searchfit-seo:schema-markup` — мета-теги и JSON-LD (Person) в `index.html`.
- `anthropic-skills:pdf` — пересборка PDF резюме из `.md`.
- `design:design-critique`, `design:accessibility-review` — оценка страницы по скриншоту.
