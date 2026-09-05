# srinisvas.github.io

Personal portfolio and research site. Built with Jekyll and deployed via GitHub Pages.

## Structure

- `index.html` introduces selected engineering work and research.
- `engineering.html` contains three case studies, career history, and technical expertise.
- `research.html` separates published/accepted papers from ongoing work.
- `about.html` contains background, education, credentials, recognition, and contact details.
- `resume.html` is a printable résumé with a generated plain-text download.
- `experience.html` and `certifications.html` preserve old links with redirects.

## Updating content

Edit `_data/projects.yml`, `_data/career.yml`, `_data/publications.yml`, and
`_data/credentials.yml`. Shared includes keep the homepage, detail pages, and
résumé consistent. Contact details and the production URL live in `_config.yml`.

Publication statuses are explicit. Add verified author lists and paper or PDF
URLs when available. Missing resources are omitted, never rendered as empty links.
The TRACE preprint uses a shorter title than the conference title retained here.
Credentials are grouped as certifications or courses without assuming current
validity or inventing verification URLs.

## Validation and deployment

The pull request workflow builds with the same Jekyll action as production,
checks generated internal links and assets, and uploads the built site for review.
It has no deployment permissions. The existing Pages workflow still deploys only
from `main` (or its explicit manual trigger).

For an environment with Jekyll installed:

```sh
jekyll build
python3 scripts/check_site.py _site
node --check assets/site.js
```

Check a project-site base path as well when changing URL handling:

```sh
jekyll build --baseurl /preview
python3 scripts/check_site.py _site --baseurl /preview
```

The layout supports keyboard navigation, a skip link, a mobile menu with an
expanded state and Escape handling, reduced motion, and print styles. Navigation
remains visible when JavaScript is unavailable. The print action opens the browser
dialog, where visitors can save the résumé as PDF.
