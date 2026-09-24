# Robotics & Documentation Hub

This repository contains the Prisma Lab documentation hub: technical manuals, operational guides, quick guides, and reference material for robotics and laboratory activities.

## Contents

The documentation is organised with MkDocs and currently covers:

- aerial platforms and drones;
- legged and wheeled robots;
- manipulators and haptic devices;
- discontinued projects in the Museum archive;
- laboratory equipment and infrastructure;
- general guides and reference resources.

The source documentation is stored in `docs/` and the site structure is defined in `mkdocs.yml`. Generated web content is stored in `site/` and published through the `gh-pages` branch.

## Local Development

Install MkDocs Material, then preview the documentation locally:

```bash
pip install mkdocs-material
mkdocs serve
```

The local site is available at `http://127.0.0.1:8000/`.

## Publishing

After updating the Markdown files or `mkdocs.yml`, build and publish the site with:

```bash
mkdocs gh-deploy
```

The public website is available at:

https://prismahubunofficial.github.io/docs_and_guides/

The documentation is intended primarily for internal Prisma Lab use.
