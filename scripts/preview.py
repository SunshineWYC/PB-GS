"""Serve only public site files at http://127.0.0.1:8000/ (Python 3.9+)."""
import argparse
import socket
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--port', type=int, default=8000)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1] / 'site'

class PublicFileHandler(SimpleHTTPRequestHandler):
    # Windows registry MIME associations can otherwise turn image links into downloads.
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.css': 'text/css',
        '.js': 'text/javascript',
    }


class PreviewServer(ThreadingHTTPServer):
    allow_reuse_address = False

    def server_bind(self):
        # SO_REUSEADDR on Windows can bind over another project without an error.
        if sys.platform == 'win32' and hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


handler = partial(PublicFileHandler, directory=str(root))
try:
    server = PreviewServer(('127.0.0.1', args.port), handler)
except OSError as error:
    parser.exit(1, 'Cannot start preview: {}. Try --port 8001.\n'.format(error))
print('Preview: http://127.0.0.1:{}/  (serving site/ only; Ctrl+C to stop)'.format(server.server_port), flush=True)
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: server.server_close()
