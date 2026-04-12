#!/usr/bin/env python3
"""Lightweight time-tracker web server – serves UI and manages times.csv."""

import csv
import hashlib
import http.server
import json
import subprocess
import threading
import uuid
from pathlib import Path

PORT = 8742
BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "times.csv"
HTML_FILE = BASE_DIR / "time_tracker.html"
FIELDS = ["id", "start", "end", "duration", "working_on", "what_did"]


def _generated_id(row, index):
    payload = json.dumps(
        {
            "start": row.get("start", ""),
            "end": row.get("end", ""),
            "duration": row.get("duration", ""),
            "working_on": row.get("working_on", ""),
            "what_did": row.get("what_did", "") or row.get("deliverables", ""),
            "index": index,
        },
        sort_keys=True,
    )
    return f"legacy-{hashlib.sha1(payload.encode()).hexdigest()[:16]}"


def normalize_row(row, index):
    row = {
        (k or "").strip().rstrip("."): (v or "").strip()
        for k, v in row.items()
    }
    legacy_note = row.get("deliverables", "")
    return {
        "id": row.get("id", "") or _generated_id(row, index),
        "start": row.get("start", ""),
        "end": row.get("end", ""),
        "duration": row.get("duration", ""),
        "working_on": row.get("working_on", ""),
        "what_did": row.get("what_did", "") or legacy_note,
    }


def read_rows(*, persist_missing_ids=False):
    if not CSV_FILE.exists():
        return []

    missing_ids = False
    with open(CSV_FILE, newline="") as f:
        rows = []
        for i, r in enumerate(csv.DictReader(f)):
            if not (r.get("id", "") or "").strip():
                missing_ids = True
            rows.append(normalize_row(r, i))

    if persist_missing_ids and missing_ids:
        write_rows(rows)

    return rows


def write_rows(rows):
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows([{k: row.get(k, "") for k in FIELDS} for row in rows])


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        {"/" : self._html, "/api/entries": self._entries}.get(
            self.path, lambda: self.send_error(404))()

    def do_POST(self):
        if self.path == "/api/entry":
            self._add_entry()
        elif self.path == "/api/update-entry":
            self._update_entry()
        elif self.path == "/api/alarm":
            self._play_alarm()
        else:
            self.send_error(404)

    # ── routes ─────────────────────────────────────────────
    def _html(self):
        self._respond(200, "text/html", HTML_FILE.read_bytes())

    def _entries(self):
        self._respond(
            200, "application/json", json.dumps(read_rows(persist_missing_ids=True)).encode()
        )

    def _add_entry(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        rows = read_rows(persist_missing_ids=True)
        row = {k: data.get(k, "") for k in FIELDS}
        row["id"] = row["id"] or uuid.uuid4().hex
        rows.insert(0, row)
        write_rows(rows)
        self._respond(200, "application/json", b'{"ok":true}')

    def _update_entry(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        row_id = (data.get("id") or "").strip()
        if not row_id:
            self.send_error(400, "Missing id")
            return

        rows = read_rows(persist_missing_ids=True)
        for i, row in enumerate(rows):
            if row.get("id") != row_id:
                continue

            updated = {k: data.get(k, row.get(k, "")) for k in FIELDS}
            updated["id"] = row_id
            rows[i] = updated
            write_rows(rows)
            self._respond(200, "application/json", b'{"ok":true}')
            return

        self.send_error(404, "Entry not found")

    def _play_alarm(self):
        """Play system alert sound 3 times via afplay."""
        def _ring():
            sound = "/System/Library/Sounds/Glass.aiff"
            for _ in range(3):
                subprocess.run(["afplay", sound])
        threading.Thread(target=_ring, daemon=True).start()
        self._respond(200, "application/json", b'{"ok":true}')

    # ── helpers ────────────────────────────────────────────
    def _respond(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass  # silence request logs


def main():
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="") as f:
            csv.writer(f).writerow(FIELDS)
    else:
        read_rows(persist_missing_ids=True)

    class ReusableHTTPServer(http.server.HTTPServer):
        allow_reuse_address = True

    srv = ReusableHTTPServer(("", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"⏱️  Time Tracker → {url}  (Ctrl-C to stop)")

    threading.Timer(0.5, lambda: subprocess.Popen(
        ["open", "-a", "Google Chrome", url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )).start()

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Stopped.")
        srv.shutdown()


if __name__ == "__main__":
    main()
