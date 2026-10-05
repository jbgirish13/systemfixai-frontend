# SystemFixAI frontend

A self-contained, responsive frontend concept based on `systemfixai-frontend-prompt.md` and the supplied circuit brain logo.

The hero motion map routes email, WhatsApp, Instagram/Facebook DMs, web leads, AI voice, and support through a central automation core to CRM, bookings, customer support, finance, and inventory. The services section groups the offers into customer conversations, sales and bookings, AI content, and business operations. Motion is simplified on mobile and disabled for reduced-motion preferences.

## Preview

Run the local preview server from this folder (it supports direct links and refreshes on every frontend route):

```powershell
python serve.py
```

Then open `http://localhost:4173`. The app includes the homepage, work filters, case study pages, about, contact, privacy, terms, and a designed not-found screen.

The forms are frontend demonstrations. They validate input and show a success message, but need a backend connection to deliver submissions. Replace sample case study figures, client names, calendar details, contact information, and legal copy before publishing.

## PDF

The homepage has print styles for a clean browser **Print → Save as PDF** export. A companion five-page design preview is included at `docs/SystemFixAI-frontend-design.pdf`.

## GitHub Pages

The included Actions workflow deploys this static frontend from the `main` branch. The build handles the repository subpath, deep links, and the PDF download. After pushing, select **Settings → Pages → GitHub Actions** in the repository if Pages has not been enabled yet.

## Files

- `index.html` — app shell and metadata
- `app.js` — page content, routes, and interactions
- `serve.py` — local preview server with route fallback
- `build_pages.py` — static Pages build with repository path support
- `.github/workflows/pages.yml` — deploys the site with GitHub Actions
- `styles.css` — responsive design system and print styles
- `assets/systemfixai-logo.png` — whitespace-trimmed copy of the supplied brand logo
