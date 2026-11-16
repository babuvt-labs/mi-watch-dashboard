#!/usr/bin/env python3
"""Serve the Mi Watch dashboard and latest JSON export using Python stdlib only."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse, json, os

HERE = Path(__file__).resolve().parent

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, data_file: Path, **kwargs):
        self.data_file = data_file
        super().__init__(*args, directory=str(HERE), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/api/data":
            try:
                payload = json.loads(self.data_file.read_text(encoding="utf-8"))
                body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                self.end_headers()
                self.wfile.write(body)
            except Exception as exc:
                body = json.dumps({"error": str(exc), "path": str(self.data_file)}).encode()
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            return
        return super().do_GET()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default=str(Path.home() / "MiWatchData/mi-fitness-data-bridge/exports/mi_fitness_export.json"),
                   help="Path to mi_fitness_export.json")
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    data_file = Path(args.data).expanduser().resolve()
    if not data_file.exists():
        raise SystemExit(f"JSON export not found: {data_file}\\nRun mi-fitness-bridge export first.")
    factory = lambda *a, **kw: Handler(*a, data_file=data_file, **kw)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), factory)
    print(f"Dashboard: http://127.0.0.1:{args.port}")
    print(f"Reading latest JSON from: {data_file}")
    print("Keep this Terminal window open. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nStopping dashboard.")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
