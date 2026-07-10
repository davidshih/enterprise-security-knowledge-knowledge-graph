import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from scripts.build_site import KNOWLEDGE_FILES, build


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"] or "")
        if tag == "a" and attributes.get("href"):
            self.hrefs.append(attributes["href"] or "")


class SiteTests(unittest.TestCase):
    def test_build_contains_versioned_knowledge_files_and_valid_local_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build(output)
            parser = LinkParser()
            parser.feed((output / "index.html").read_text(encoding="utf-8"))

            self.assertEqual(len(parser.ids), len(set(parser.ids)))
            self.assertTrue((output / "styles.css").is_file())
            self.assertTrue((output / "app.js").is_file())
            self.assertTrue((output / "knowledge" / "manifest.json").is_file())

            for destination in KNOWLEDGE_FILES.values():
                self.assertTrue((output / "knowledge" / destination).is_file())

            for href in parser.hrefs:
                if href.startswith("./"):
                    self.assertTrue((output / href.removeprefix("./")).is_file(), href)

    def test_navigation_targets_existing_sections(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        parser = LinkParser()
        parser.feed((project_root / "website" / "index.html").read_text(encoding="utf-8"))
        page_ids = set(parser.ids)

        for href in parser.hrefs:
            if href.startswith("#"):
                self.assertIn(href.removeprefix("#"), page_ids)

    def test_ui_contract_includes_accessible_responsive_foundations(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        html = (project_root / "website" / "index.html").read_text(encoding="utf-8")
        css = (project_root / "website" / "styles.css").read_text(encoding="utf-8")

        self.assertIn('<html lang="zh-Hant">', html)
        self.assertIn('class="skip-link"', html)
        self.assertIn('aria-controls="site-menu"', html)
        self.assertIn('id="site-search"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn(':focus-visible', css)
        self.assertIn('min-height: 44px', css)
        self.assertIn('@media (max-width: 760px)', css)
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertIn('overflow-x: hidden', css)

    def test_light_theme_does_not_include_legacy_dark_graph_surfaces(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        html = (project_root / "website" / "index.html").read_text(encoding="utf-8")
        css = (project_root / "website" / "styles.css").read_text(encoding="utf-8")

        self.assertNotIn('class="feature-card metric-card dark-card"', html)
        self.assertNotIn('class="section-intro light-copy"', html)
        self.assertNotIn('--dark:', css)
        self.assertNotIn('--dark-surface:', css)
        self.assertIn('.blue-card { background: #eaf4ff;', css)
        self.assertIn('.evidence-section { background: var(--surface);', css)
        self.assertIn('.quickstart {', css)
        self.assertIn('background: var(--surface); color: var(--foreground);', css)


if __name__ == "__main__":
    unittest.main()
