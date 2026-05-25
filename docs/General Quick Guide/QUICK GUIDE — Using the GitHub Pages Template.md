# QUICK GUIDE — Using the GitHub Pages Template for Research Reports

This quick guide explains how to take the generic GitHub Pages template in this repository and turn it into a polished website for presenting a paper or project. The template uses **Jekyll** and the **Just the Docs** theme, but you don't need to know much about either to get started.

---

## 1. Get Started

- Copy the content of the [`gitpage_template` folder]({{ '/gitpage_template.zip' | relative_url }}) into a new GitHub repository.
- Make sure the repository contains a `_config.yml` file and some Markdown pages (`index.md`, `method.md`, `experiments.md`, etc.).
- Enable **GitHub Pages** on your repository (`Settings → Pages`) and choose the `main` branch and root (`/`) as the source.

!!! tip
    If you want to preview the site locally, install Ruby and Jekyll and run:
    ```bash
    bundle exec jekyll serve
    ```
    Then open `http://127.0.0.1:4000/<your-repo-name>/` in a browser.

## 2. File Structure and Configuration

The key files and folders in the template are:

| Path | Purpose |
| --- | --- |
| `_config.yml` | Site‑wide settings: title, description, URL, menus, logos and footer. |
| `index.md` | Home page (abstract, overview, links). |
| `method.md` | Outline of your methodology or approach. |
| `experiments.md` | Results from simulations or experiments. |
| `results.md` | (Optional) Discussion of key findings. |
| `references.md` | Citation information and related links. |
| `assets/` | Images (`assets/img`) and videos (`assets/video`). |

Edit `_config.yml` to personalise the site:

- Change `title` and `description` to match your project.
- Replace `<tuo-username>` and `<nome-del-tuo-progetto>` in `url`, `baseurl` and `gh_edit_repository` with your GitHub username and repository name.
- Update `aux_links` to include links to your lab, department or collaborators.
- Replace the logo or favicon by changing the paths in `logo` and `favicon_ico` and placing your own files in `assets/img/`.

!!! warning
    YAML is picky about indentation. Make sure there are no tabs or extra spaces when editing `_config.yml`.

## 3. Creating and Organising Pages

Each page is a Markdown file (`.md`) with a front matter section at the top. The front matter tells Jekyll how to render the page and where to place it in the navigation.

Example template:

```markdown
---
layout: default
title: "My New Section"
nav_order: 4
---

# My New Section

Content goes here.
```

- **`layout: default`** – use the standard page layout.
- **`title`** – the text that appears in the sidebar and at the top of the page.
- **`nav_order`** – lower numbers appear earlier in the navigation. Pages with the same `nav_order` are sorted alphabetically.

To add a new page:

1. Create a new `.md` file in the project root (e.g. `analysis.md`).
2. Add front matter as shown above and write your content.
3. Commit and push to GitHub. The page will appear in the sidebar once the site rebuilds.

## 4. Adding Images and Videos

### Images

Place images in `assets/img/` and embed them using Markdown:

```markdown
![A chart showing results]({{ '/assets/img/analysis_chart.png' | relative_url }})
```

### Videos

Place MP4 files in `assets/video/` (you can create subfolders) and embed them with HTML:

```html
<video autoplay muted loop playsinline preload="metadata">
  <source src="{{ '/assets/video/simulations/demo.mp4' | relative_url }}" type="video/mp4">
</video>
```

You can also use `<iframe>` to embed videos from YouTube or Vimeo.

## 5. Publishing to GitHub Pages

Once your content is ready, publishing is straightforward:

1. Commit and push all changes to GitHub.
2. In your repository’s **Settings → Pages**, ensure the correct branch and folder are selected.
3. Wait a moment; GitHub will build the site and provide a URL like:
   ```text
   https://<your-user>.github.io/<repository-name>/
   ```

To update the site later, just push new commits. GitHub Pages will rebuild automatically.

## 6. Advanced Customisation

If you want to change colours, fonts or layout details:

- Modify the colour scheme in `assets/css/color_schemes/custom.css` and `_sass/color_schemes/prismalab.scss`.
- Add custom stylesheets or JavaScript files under `assets/css/` or `assets/js/` and reference them in `_config.yml` using `extra_css` or `extra_js`.
- Explore the [Just the Docs documentation](https://just-the-docs.github.io/just-the-docs/) for more options such as callouts, badges, and search settings.

## 7. Frequently Asked Questions

- **Can I use this template outside of PRISMA Lab?** Yes. It’s generic; only the PRISMA Lab logo and footer are preconfigured. Replace or remove them as needed.
- **What if I need another language?** Translate the Markdown files directly. Nothing in the code restricts the language.
- **Do I have to run Jekyll locally?** No. GitHub Pages will build the site for you. Running locally is optional for previewing changes.

## 8. Summary

The basic workflow is:

1. Personalise `_config.yml` with your project details.
2. Edit the Markdown pages to add your abstract, methods, results, and references.
3. Add new pages and set `nav_order` to organise the sidebar.
4. Upload images and videos to the `assets/` folders and embed them in your pages.
5. Commit and push to GitHub to publish or update the site.

For more complex customisation (multi‑language, search filters, versioning), consult the official Jekyll and Just the Docs documentation.