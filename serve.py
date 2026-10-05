"""Small local preview server with SPA route fallback."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class FrontendHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _serve(self, method):
        requested = Path(self.translate_path(self.path))
        if not requested.exists() and not Path(self.path.split("?", 1)[0]).suffix:
            original = self.path
            self.path = "/index.html"
            try:
                getattr(super(), method)()
            finally:
                self.path = original
            return
        getattr(super(), method)()

    def do_GET(self):
        self._serve("do_GET")

    def do_HEAD(self):
        self._serve("do_HEAD")


if __name__ == "__main__":
    print("SystemFixAI preview: http://localhost:4173")
    ThreadingHTTPServer(("127.0.0.1", 4173), FrontendHandler).serve_forever()
