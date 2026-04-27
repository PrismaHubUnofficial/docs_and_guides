# How to Update the Website (MkDocs + GitHub Pages)

This guide explains how to maintain and extend the PrismaHub documentation website using MkDocs and GitHub Pages.

It assumes you already completed the first setup:

- repository with a `docs/` folder
- working `mkdocs.yml`
- `mkdocs-material` installed
- initial deploy already done

---

## 1. Prerequisites

Before making changes, verify:

- Python 3.8+ is installed
- `pip` is available
- MkDocs Material is installed

```bash
pip install mkdocs-material
```

Expected project structure (example):

```text
.
├── docs/
│   ├── index.md
│   ├── General Quick Guide/
│   ├── pdfs/
│   └── robots/
├── mkdocs.yml
└── site/   # generated during build (should be ignored by git)
```

If needed, deploy once with:

```bash
mkdocs gh-deploy --force
```

`--force` overwrites the remote `gh-pages` branch history.

## 2. Core Configuration (`mkdocs.yml`)

`mkdocs.yml` controls navigation, theme, plugins, and site metadata.

```yaml
site_name: PrismaHub - Documentation & Guides
site_description: Internal knowledge base for robot operation and media guides
site_author: Simone
site_url: https://<your-github-username>.github.io/<repository-name>/

# Repository links
repo_name: <your-username>/<repo-name>
repo_url: https://github.com/<your-username>/<repo-name>
edit_uri: edit/main/docs/

theme:
  name: material
  language: en
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: black
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: Roboto
    code: Fira Code
  favicon: assets/images/favicon.png
  logo: assets/images/logo.svg

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html

plugins:
  - search
  - mkdocs-pdf-embed-plugin
  - glightbox

nav:
  - Home: index.md
  - General Quick Guides:
      - Creating Subtitles: "General Quick Guide/QUICK GUIDE — Creating Subtitles.md"
      - Voiceover for a Video: "General Quick Guide/QUICK GUIDE — Voiceover for a Video.md"
  - Robots:
      - ANYmal: robots/anymal/anymal_manual_operation.md
      - baby_k: robots/baby_k/baby_k_manual_operation.md
      - H1: robots/h1/h1_manual_operation.md
      - Rover: robots/rover/rover_manual_operation.md
  - Resources:
      - LaTeX Symbols PDF: pdfs/latex_symbols_guide.pdf
```

Important notes:

- Filenames with spaces are allowed, but hyphens or underscores are usually easier to maintain.
- If `nav` is defined, MkDocs uses it as the source of truth.
- Keep `site/` in `.gitignore`.

## 3. Add a New Section or Page

### 3.1 Create the Markdown file

Example for a new robot guide (`Spot`):

```bash
mkdir -p docs/robots/Spot
touch docs/robots/Spot/Spot_manual_operation.md
```

### 3.2 Write the content

```markdown
# Spot - Manual Operation

## Safety Precautions

!!! warning
    Keep at least 2 meters of distance during initial testing.

## Powering On

1. ...
```

### 3.3 Add images or PDFs

- Put images in `docs/robots/figures/` or in the same section folder.
- Use relative paths when linking.

```markdown
![Spot robot](figures/spot.jpg)
```

- Put PDFs in `docs/pdfs/` and link them normally.

### 3.4 Update navigation

Add the page to `nav` in `mkdocs.yml`.

```yaml
nav:
  - Robots:
      - ANYmal: robots/anymal/anymal_manual_operation.md
      - baby_k: robots/baby_k/baby_k_manual_operation.md
      - H1: robots/h1/h1_manual_operation.md
      - Rover: robots/rover/rover_manual_operation.md
      - Spot: robots/Spot/Spot_manual_operation.md
```

### 3.5 Test locally

```bash
mkdocs serve
```

Open `http://127.0.0.1:8000` and verify rendering, links, and navigation.

### 3.6 Deploy

```bash
mkdocs gh-deploy
```

This rebuilds `site/` and publishes to the `gh-pages` branch.

## 4. Customize the Look and Behavior

### 4.1 Custom CSS and JavaScript

Create files like:

- `docs/stylesheets/extra.css`
- `docs/javascripts/extra.js`

Then include them in `mkdocs.yml`:

```yaml
extra_css:
  - stylesheets/extra.css

extra_javascript:
  - javascripts/extra.js
```

### 4.2 Theme colors

Update the `palette` section in `mkdocs.yml`.

### 4.3 Footer and social links

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/<your-username>
    - icon: fontawesome/brands/linkedin
      link: https://linkedin.com/in/<your-profile>
  generator: false
```

### 4.4 Custom domain

- Create `docs/CNAME` with your domain (example: `docs.prismahub.com`).
- Configure the same domain in GitHub Pages settings.

## 5. Asset Management

- Images: keep them in `docs/robots/figures/` or `docs/assets/images/`.
- PDFs: keep them in `docs/pdfs/`.
- Other files (`.zip`, `.docx`, etc.): place them anywhere inside `docs/`.

Example PDF button:

```markdown
[Download PDF](pdfs/latex_symbols_guide.pdf){: .md-button }
```

## 6. Common Commands

| Command | Description |
| --- | --- |
| `mkdocs serve` | Start local dev server with live reload. |
| `mkdocs build` | Build static site into `site/`. |
| `mkdocs gh-deploy` | Build and publish to `gh-pages`. |
| `mkdocs gh-deploy --force` | Force overwrite `gh-pages` history. |
| `mkdocs --version` | Show MkDocs version. |

## 7. Troubleshooting

### 7.1 Navigation entries are missing

- Check that the page is listed in `nav`.
- Run `mkdocs serve` and watch terminal output for missing files.

### 7.2 Images or PDFs do not load

- Check relative path correctness.
- Check filename case sensitivity.
- Ensure files are inside `docs/`.

### 7.3 Deploy fails with `GH006: Protected branch update failed`

- If branch protections block `gh-pages`, update protections or use a suitable token-based workflow.
- Manual fallback:

```bash
mkdocs build
cd site
git init
git add .
git commit -m "Deploy site"
git push --force https://github.com/<username>/<repo>.git master:gh-pages
```

### 7.4 Markdown extensions not recognized

- Confirm extensions are listed in `markdown_extensions`.
- Install missing packages:

```bash
pip install pymdown-extensions
```

## 8. Summary

Regular workflow:

1. Add or update Markdown pages in `docs/`.
2. Update `nav` in `mkdocs.yml`.
3. Run `mkdocs serve` for local checks.
4. Deploy with `mkdocs gh-deploy`.

For advanced features (i18n, versioning, blog), refer to MkDocs and Material for MkDocs official documentation.