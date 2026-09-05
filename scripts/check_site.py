"""Validate generated static pages without external requests or dependencies."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.references = []
        self.h1 = 0
        self.main = 0
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        self.h1 += tag == "h1"
        self.main += tag == "main"
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])
        for key in ("aria-controls", "aria-labelledby"):
            self.references.extend(attrs.get(key, "").split())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--baseurl", default="")
    args = parser.parse_args()
    root = args.directory.resolve()
    baseurl = args.baseurl.rstrip("/")
    pages = {}
    errors = []
    for path in root.rglob("*.html"):
        text = path.read_text()
        pages[path] = Page(text)
        if "{{" in text or "{%" in text:
            errors.append(f"Unrendered Liquid in {path.name}")
    expected = ("index.html", "engineering.html", "research.html", "about.html", "resume.html", "experience.html", "certifications.html")
    for name in expected:
        if root / name not in pages:
            errors.append(f"Missing page: {name}")
    for path, page in pages.items():
        if page.h1 != 1 or page.main != 1:
            errors.append(f"Expected one h1 and main in {path.name}")
        errors.extend(f"Duplicate ID in {path.name}: {value}" for value in page.duplicates)
        errors.extend(f"Missing ARIA target in {path.name}: {value}" for value in page.references if value not in page.ids)
        current = baseurl + "/" + path.relative_to(root).as_posix()
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            if not link or link == "#":
                errors.append(f"Empty link in {path.name}")
                continue
            resolved = urlsplit(urljoin(current, link))
            url_path = unquote(resolved.path)
            if baseurl and not url_path.startswith(baseurl + "/"):
                errors.append(f"Link escapes baseurl in {path.name}: {link}")
                continue
            target = root / url_path[len(baseurl):].lstrip("/")
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"Broken link in {path.name}: {link}")
            elif resolved.fragment and target in pages and unquote(resolved.fragment) not in pages[target].ids:
                errors.append(f"Missing anchor in {path.name}: {link}")
    resume = root / "assets/srinivasan-subramanian-resume.txt"
    if not resume.exists() or "{{" in resume.read_text() or "{%" in resume.read_text():
        errors.append("Text résumé missing or contains unrendered Liquid")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(pages)} pages, internal links, anchors, assets, ARIA targets, and résumé.")


if __name__ == "__main__":
    main()
