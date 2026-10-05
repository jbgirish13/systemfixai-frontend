"""Build this static SPA for a GitHub Pages project URL."""

import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "dist-pages"
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "").strip("/")
REPO_NAME = REPOSITORY.rsplit("/", 1)[-1] if REPOSITORY else "systemfixai-frontend"
BASE = f"/{REPO_NAME}"


if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
OUTPUT.mkdir(parents=True)

html = (ROOT / "index.html").read_text(encoding="utf-8")
html = html.replace('href="/', f'href="{BASE}/')
html = html.replace('src="/', f'src="{BASE}/')
(OUTPUT / "index.html").write_text(html, encoding="utf-8")
(OUTPUT / "404.html").write_text(html, encoding="utf-8")

app = (ROOT / "app.js").read_text(encoding="utf-8")
app = app.replace("const A = '/assets/systemfixai-logo.png';", f"const BASE_PATH = '{BASE}';\nconst A = BASE_PATH + '/assets/systemfixai-logo.png';")
app = app.replace('href="/', 'href="${BASE_PATH}/')
app = app.replace(
    "const path=decodeURI(location.pathname).replace(/\\/$/,'')||'/';",
    "const rawPath=decodeURI(location.pathname);const routePath=BASE_PATH&&rawPath.startsWith(BASE_PATH)?rawPath.slice(BASE_PATH.length):rawPath;const path=routePath.replace(/\\/$/,'')||'/';",
)
(OUTPUT / "app.js").write_text(app, encoding="utf-8")
(OUTPUT / "styles.css").write_text((ROOT / "styles.css").read_text(encoding="utf-8"), encoding="utf-8")
shutil.copytree(ROOT / "assets", OUTPUT / "assets")
shutil.copy2(ROOT / "docs" / "SystemFixAI-frontend-design.pdf", OUTPUT / "SystemFixAI-frontend-design.pdf")

# Fail early if the app's root route was not made project-path aware.
if f"const BASE_PATH = '{BASE}'" not in app or 'href="${BASE_PATH}/work"' not in app:
    raise SystemExit("GitHub Pages base path was not applied correctly.")
if not re.search(r"routePath=BASE_PATH", app):
    raise SystemExit("SPA route fallback was not made base-path aware.")

print(f"Built GitHub Pages site at {OUTPUT} for {BASE}/")
