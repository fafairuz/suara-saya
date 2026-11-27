"""Langkah 1: ujian A/B ejaan sebutan. Setiap ayat dijana tiga kali dengan benih sama:
  A = teks asal, B = istilah -> lajur `sebutan` tanpa sengkang (cantum), C = sengkang jadi jarak.
Istilah dibaca dari video-template/istilah-saya.csv. Semua tempatan, luar talian.
  .venv/bin/python ujian/ab_sebutan.py"""
import os, sys
os.environ['HF_HUB_OFFLINE'] = '1'; os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
import csv, json, re, subprocess, time
from pathlib import Path
import numpy as np, soundfile as sf, torch

VT = Path('/Volumes/opt/claude/video-template')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from suara.model import muat as load, device   # noqa: E402  (model kini di suara-saya/models)

OUT = Path(__file__).resolve().parent / 'ab'
WHISPER = os.path.expanduser('~/.local/share/whisper/models/ggml-large-v3-turbo.bin')
AYAT = [
    "Kita host LLM sendiri on-prem.",
    "Untuk demo ni, jangan masukkan data PII sebenar dalam log.",
    "Cuma cryptographic proof yang dihantar ke MBI trust layer.",
    "Untuk demo deepfake ni, kita guna rakaman simulasi.",
    "Sistem ni boleh dipercayai, telus dan berintegriti.",
    "Bila fail sampai, sistem kira hash dan simpan dalam blockchain.",
]


def istilah():
    rows = [r for r in csv.DictReader(open(VT / 'istilah-saya.csv')) if r['jenis'] != 'BM' and r['sebutan'].strip()]
    pats = []
    for r in rows:
        for w in {r['istilah'], r['bentuk_tulisan']}:
            if not w.strip(): continue
            flag = 0 if r['jenis'] == 'AKRONIM' else re.I
            pats.append((len(w), re.compile(r'(?<![\w-])' + re.escape(w) + r'(?![\w-])', flag), r['sebutan']))
    return sorted(pats, key=lambda p: -p[0])


def tukar(teks, pats, sambung):
    out, ganti = teks, []
    for _, p, s in pats:
        s2 = s.replace('-', sambung)
        if p.search(out): ganti.append(f'{p.pattern}->{s2}')
        out = p.sub(s2, out)
    return out


def whisper(wav):
    w16 = str(wav) + '.16k.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-ar', '16000', '-ac', '1', w16], check=True)
    r = subprocess.run(['whisper-cli', '-m', WHISPER, '-l', 'ms', '-nt', '-np', '-f', w16], capture_output=True, text=True)
    os.remove(w16)
    return ' '.join(r.stdout.split())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pats = istilah()
    m = load(device()); m.prepare_conditionals(str(Path(__file__).resolve().parent.parent / 'persona' / 'fairuz' / 'rujukan' / 'santai.flac'), exaggeration=0.5)
    gap = np.zeros(int(0.9 * m.sr), np.float32); semua = []; lap = []
    for i, a in enumerate(AYAT, 1):
        varian = {'A': a, 'B': tukar(a, pats, ''), 'C': tukar(a, pats, ' ')}
        parts = []
        for k, t in varian.items():
            torch.manual_seed(7); t0 = time.time()
            w = m.generate(t, language_id='ms', cfg_weight=0.5, exaggeration=0.5, temperature=0.7).squeeze(0).numpy().astype(np.float32)
            w = w / max(1e-6, np.abs(w).max()) * 0.89
            f = OUT / f'{i}{k}.flac'; sf.write(f, w, m.sr); parts += [w, gap]
            h = whisper(f)
            lap.append(dict(no=i, varian=k, teks_dihantar=t, whisper=h, saat=round(len(w) / m.sr, 1)))
            print(f'{i}{k} ({time.time() - t0:.0f} s) | {t} | whisper: {h}', flush=True)
        y = np.concatenate(parts[:-1]); semua += [y, gap, gap]
    sf.write(OUT / 'semua-ABC.flac', np.concatenate(semua), m.sr)
    json.dump(lap, open(OUT / 'laporan.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
