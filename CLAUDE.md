# CLAUDE.md — cv-portfolio

Сайт-портфолио и резюме: Maksym Kasianov, Manual QA Engineer и разработчик приложений. Публикуется на GitHub Pages: `https://moslyharmless.github.io/cv-portfolio/` (репозиторий `MoslyHarmless/cv-portfolio`, ветка `main`). Две версии: английская `/` и украинская `/uk/`.

С владельцем общаться по-русски.

## Как устроено

Статический сайт без фреймворков и сборщиков. Весь текст сайта и резюме лежит в `content.py`, а `build.py` генерирует из него HTML, Markdown, PDF, sitemap.

**Сгенерированные файлы руками не править** — правка в `content.py` (тексты) или `build.py` (разметка), затем пересборка.

| Путь | Что это |
|---|---|
| `content.py` | Все тексты EN/UK: проекты, опыт, навыки, контакты, SEO-заголовки |
| `build.py` | Генератор страниц, резюме, sitemap, robots |
| `assets/site.css`, `assets/site.js` | Стили и скрипт (правятся руками) |
| `index.html`, `uk/index.html` | Сгенерировано |
| `cv/*.pdf` | Резюме для скачивания; сгенерировано из `cv/print/*.html` |
| `CV_Maksym_Kasianov_QA_EN.md`, `..._UK.md` | Текстовые версии резюме, сгенерировано |
| `og.html` → `og.png` | Картинка для соцсетей 1200×630 |
| `favicon.svg`, `robots.txt`, `sitemap.xml`, `.nojekyll` | Служебные файлы |

## Команды

```bash
python build.py          # HTML, Markdown, sitemap
python build.py --pdf    # плюс PDF резюме и og.png (нужны playwright и Microsoft Edge)
python -m http.server 8080
```

Выкладка — push в `main`. Сайт живёт в подпапке `/cv-portfolio/`, пути к ресурсам относительные.

## Правила

- Факты резюме (компании, даты, контакты) не выдумывать без владельца. Формулировки проектов владелец разрешил усиливать: все проекты он сделал сам.
- Тексты EN и UK меняются вместе, в обоих ключах `content.py`.
- Резюме должно оставаться ATS-дружелюбным: одна колонка, Arial, стандартные заголовки, без эмодзи и таблиц, не больше двух страниц (проверять число страниц PDF после правок).

## Скилы и агенты

Подключены из ECC (`.claude/skills`, `.claude/agents`): `seo`, `frontend-design-direction`, `i18n-sync`, `accessibility`, `browser-qa`, `make-interfaces-feel-better`; агенты `seo-specialist`, `a11y-architect`.
