#!/usr/bin/env python3
"""
OS Multithreaded Proxy Server - Interactive GUI & Visualization Server
Inspired by 'Designed to Scale' (designedtoscale.app)

Usage:
    python proxy_gui_server.py [PORT]
    (Default port: 5000)
"""
import http.server
import json
import os
from pathlib import Path
import socket
import sys
import threading
import time
import urllib.parse
import webbrowser

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"
DEFAULT_PORT = 5000
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8080


class ProxyGUIRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/status":
            self.handle_api_status()
        elif parsed.path == "/api/proxy-test":
            self.handle_api_proxy_test(parsed.query)
        else:
            # Fallback to serving static files from frontend/
            super().do_GET()

    def handle_api_status(self):
        """Check if the C proxy server binary is running on port 8080."""
        is_proxy_running = False
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect((PROXY_HOST, PROXY_PORT))
                is_proxy_running = True
        except (socket.error, OSError):
            is_proxy_running = False

        payload = {
            "status": "online",
            "c_proxy_running": is_proxy_running,
            "proxy_host": PROXY_HOST,
            "proxy_port": PROXY_PORT,
            "max_workers": 32,
            "architecture": "POSIX Pthreads + Semaphores (sem_t)",
            "timestamp": time.time(),
        }
        self.send_json_response(200, payload)

    def handle_api_proxy_test(self, query_string):
        """Send a real or simulated request through the C proxy."""
        params = urllib.parse.parse_qs(query_string)
        target_url = params.get("url", ["http://example.com"])[0]
        concurrency = int(params.get("concurrency", ["1"])[0])

        start_time = time.time()
        results = []

        def test_worker(worker_id):
            worker_start = time.time()
            try:
                # Attempt real connection to C proxy
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(3.0)
                    s.connect((PROXY_HOST, PROXY_PORT))
                    req = f"GET {target_url} HTTP/1.0\r\nHost: {urllib.parse.urlparse(target_url).netloc}\r\n\r\n"
                    s.sendall(req.encode())
                    resp = s.recv(4096)
                    elapsed = int((time.time() - worker_start) * 1000)
                    first_line = resp.split(b"\r\n")[0].decode(errors="replace") if resp else "Empty response"
                    return {
                        "worker_id": worker_id,
                        "status": 200 if b"200" in resp else 503 if b"503" in resp else 400,
                        "response_header": first_line,
                        "bytes_relayed": len(resp),
                        "latency_ms": elapsed,
                        "is_real_backend": True
                    }
            except Exception as e:
                # Fallback to realistic simulation if C server is not currently running
                elapsed = int((time.time() - worker_start) * 1000) + 45
                is_overload = worker_id > 32
                return {
                    "worker_id": worker_id,
                    "status": 503 if is_overload else 200,
                    "response_header": "HTTP/1.0 503 Service Unavailable" if is_overload else "HTTP/1.0 200 OK",
                    "bytes_relayed": 0 if is_overload else 577,
                    "latency_ms": elapsed,
                    "is_real_backend": False,
                    "note": "Deflected by sem_trywait (overload)" if is_overload else "Simulated C worker output"
                }

        threads = []
        collected = []
        for i in range(1, concurrency + 1):
            def run(wid=i):
                collected.append(test_worker(wid))
            t = threading.Thread(target=run)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total_elapsed = int((time.time() - start_time) * 1000)
        self.send_json_response(200, {
            "target_url": target_url,
            "concurrency": concurrency,
            "total_latency_ms": total_elapsed,
            "results": collected
        })

    def send_json_response(self, status_code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Clean terminal output
        sys.stderr.write(f"[GUI Server] {args[0]} {args[1]} - {args[2]}\n")


def run_server(port=DEFAULT_PORT):
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, ProxyGUIRequestHandler)
    url = f"http://localhost:{port}"

    print("=" * 65)
    print("  DESIGNED TO SCALE: OS PROXY INTERACTIVE FRONTEND")
    print("=" * 65)
    print(f"  * Frontend Web App : {url}")
    print(f"  * C Proxy Target   : {PROXY_HOST}:{PROXY_PORT}")
    print(f"  * Press Ctrl+C in this terminal to stop the server")
    print("=" * 65)

    def open_browser():
        time.sleep(0.8)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[GUI Server] Shutting down cleanly.")
        httpd.server_close()


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else DEFAULT_PORT
    run_server(p)
