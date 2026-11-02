#!/usr/bin/env python3
"""Divineestates 3D web UI server (stdlib only). Reuses script_engine.py + video_engine.py unchanged.
Run:  python Divineestates_server.py   ->  http://localhost:8000     (original Streamlit app.py still works)"""
import base64, io, json, re, sys, tempfile, threading, uuid, webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from PIL import Image
from script_engine import generate_script
from video_engine import render_video

ROOT = Path(__file__).parent
OUT, DEMO, SAMPLE = ROOT / "outputs", ROOT / "assets" / "demo", ROOT / "sample_output"
OUT.mkdir(exist_ok=True)
JOBS: dict[str, dict] = {}

def run_job(jid, b):
    job = JOBS[jid]; out = None
    try:
        d = b["details"]
        imgs = [Image.open(io.BytesIO(base64.b64decode(i["data"].split(",", 1)[1]))).convert("RGB") for i in b["images"]]
        job.update(stage="Preparing captions and script", frac=0.02)
        with tempfile.TemporaryDirectory(prefix="ef_") as tmp:
            tmp = Path(tmp); voice = music = None; warnings = []
            if b.get("music_data"):
                music = tmp / ("music" + (Path(b.get("music_name", "")).suffix[:6] or ".mp3"))
                music.write_bytes(base64.b64decode(b["music_data"].split(",", 1)[1]))
            if b.get("voice") and str(b.get("voiceover", "")).strip():
                try:
                    from gtts import gTTS
                    voice = tmp / "narration.mp3"; gTTS(text=b["voiceover"], lang="en", tld="co.in").save(str(voice))
                except Exception:
                    voice = None; warnings.append("Online narration was unavailable; the video was exported without narration.")
            slug = re.sub(r"[^a-z0-9]+", "_", (d.get("property_name") or "property_video").lower()).strip("_")[:48] or "property_video"
            out = OUT / f"{slug}_{datetime.now():%Y%m%d_%H%M%S}.mp4"
            def cb(f): job.update(stage="Finalizing MP4" if f >= .96 else "Rendering scenes and encoding MP4", frac=max(.03, min(1, f)))
            res = render_video(images=imgs, details=d, output_path=out, aspect_ratio=d["aspect_ratio"],
                               scene_seconds=float(b.get("scene_seconds", 3.7)), transition_seconds=0.4,
                               music_path=str(music) if music else None, voiceover_path=str(voice) if voice else None, progress_callback=cb)
        info = {"name": d.get("property_name") or "Property video", "location": d.get("location", ""),
                "created_at": datetime.now().strftime("%d %b %Y, %H:%M"), "meta": res, "style": d.get("visual_style", "")}
        out.with_suffix(".json").write_text(json.dumps(info, default=str), encoding="utf-8")
        job.update(done=True, frac=1.0, stage="MP4 ready", video=f"/media/{out.name}", info=info, warnings=warnings)
    except Exception as e:
        if out: out.unlink(missing_ok=True)
        job.update(done=True, error=(str(e).splitlines() or ["Video export failed."])[0][:260])

def videos():
    rows = []
    for mp4 in sorted(OUT.glob("*.mp4"), key=lambda f: f.stat().st_mtime, reverse=True):
        j = mp4.with_suffix(".json")
        try: info = json.loads(j.read_text("utf-8")) if j.exists() else {}
        except Exception: info = {}
        info.setdefault("name", mp4.stem.rsplit("_", 2)[0].replace("_", " ").title()); info.setdefault("location", "")
        info.setdefault("created_at", datetime.fromtimestamp(mp4.stat().st_mtime).strftime("%d %b %Y, %H:%M"))
        info.setdefault("meta", {"file_size_mb": round(mp4.stat().st_size / 1048576, 2)})
        rows.append({**info, "file": mp4.name, "video": f"/media/{mp4.name}"})
    return rows

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, code, data, ct="application/json", extra=None):
        data = data if isinstance(data, bytes) else json.dumps(data, default=str).encode()
        self.send_response(code); self.send_header("Content-Type", ct); self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(data)
    def file(self, f, ct):
        if not f.is_file(): return self.send(404, {"error": "not found"})
        data = f.read_bytes(); rng = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
        if rng:   # byte ranges so <video> can seek
            a = int(rng[1] or 0); z = int(rng[2]) if rng[2] else len(data) - 1
            return self.send(206, data[a:z + 1], ct, {"Content-Range": f"bytes {a}-{z}/{len(data)}", "Accept-Ranges": "bytes"})
        self.send(200, data, ct, {"Accept-Ranges": "bytes"})
    def do_GET(self):
        p = self.path.split("?")[0]
        if p in ("/", "/index.html"): return self.file(ROOT / "web/index.html", "text/html; charset=utf-8")
        if m := re.fullmatch(r"/api/status/([\w-]+)", p): return self.send(200, JOBS.get(m[1], {"done": True, "error": "Unknown job"}))
        if p == "/api/videos": return self.send(200, videos())
        if p == "/api/sample":
            s = json.loads((ROOT / "sample_property.json").read_text("utf-8"))
            return self.send(200, {"data": s, "files": [f.name for f in sorted(DEMO.glob("*.jpg"))[:8]]})
        if m := re.fullmatch(r"/media/([\w\-]+\.mp4)", p): return self.file(OUT / m[1], "video/mp4")
        if m := re.fullmatch(r"/demo/([\w\-]+\.jpg)", p): return self.file(DEMO / m[1], "image/jpeg")
        if p == "/sample/video": return self.file(SAMPLE / "The_Meridian_Residences_demo.mp4", "video/mp4")
        self.send(404, {"error": "not found"})
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        if n > 120_000_000: return self.send(413, {"error": "Upload too large (max 120 MB in total)."})
        try: b = json.loads(self.rfile.read(n))
        except Exception: return self.send(400, {"error": "Invalid request"})
        if self.path == "/api/script": return self.send(200, {"voiceover": generate_script(b)["voiceover"]})
        if self.path == "/api/videos/delete":
            name = str(b.get("file", ""))
            if re.fullmatch(r"[\w\-]+\.mp4", name):
                (OUT / name).unlink(missing_ok=True); (OUT / name).with_suffix(".json").unlink(missing_ok=True)
            return self.send(200, {"ok": True})
        if self.path == "/api/generate":
            jid = uuid.uuid4().hex[:10]; JOBS[jid] = {"stage": "Preparing property photos", "frac": 0.0, "done": False}
            threading.Thread(target=run_job, args=(jid, b), daemon=True).start(); return self.send(200, {"id": jid})
        self.send(404, {"error": "not found"})

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"Divineestates Studio running at http://localhost:{port}  (Ctrl+C to stop)")
    threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nStopped.")
