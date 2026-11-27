"""Banding tetapan Chatterbox untuk sebutan BM ("jadi" jadi "jady"). Benih sama untuk semua varian.
  .venv/bin/python ujian/tetapan.py  ->  ujian/tetapan/<varian>.flac + semua.flac + laporan.json"""
import json, sys, time
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R))
from suara.model import muat, device     # noqa: E402
from suara.sebutan import tukar          # noqa: E402
from suara.dengar import whisper         # noqa: E402
import numpy as np, soundfile as sf, torch

OUT = R / 'ujian' / 'tetapan'
AYAT = ["Jadi data sensitif tak keluar langsung dari rangkaian agensi.",
        "Sistem ni boleh dipercayai, cuma kena jaga betul-betul."]
S2 = '/Volumes/opt/claude/video-template/tts/rujukan/rujukan-s2.wav'
VARIAN = [   # nama, rujukan, cfg_weight, exaggeration, temperature
    ('1-semasa', R / 'persona/fairuz/rujukan/santai.flac', 0.5, 0.5, 0.7),
    ('2-cfg0', R / 'persona/fairuz/rujukan/santai.flac', 0.0, 0.5, 0.7),
    ('3-cfg03-suhu05', R / 'persona/fairuz/rujukan/santai.flac', 0.3, 0.5, 0.5),
    ('4-tenang', R / 'persona/fairuz/rujukan/santai.flac', 0.5, 0.3, 0.5),
    ('5-rujukan-s2', Path(S2), 0.5, 0.5, 0.7),
    ('6-rujukan-s2-cfg0', Path(S2), 0.0, 0.5, 0.7),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m = muat(device()); jeda = np.zeros(int(0.5 * m.sr), np.float32); semua = []; lap = []
    for nama, ruj, cfg, ex, suhu in VARIAN:
        if not ruj.exists(): print('langkau', nama, ruj); continue
        m.prepare_conditionals(str(ruj), exaggeration=ex); parts = []
        for t in AYAT:
            torch.manual_seed(7)
            w = m.generate(tukar(t), language_id='ms', cfg_weight=cfg, exaggeration=ex, temperature=suhu).squeeze(0).numpy().astype(np.float32)
            parts += [w / max(1e-6, np.abs(w).max()) * 0.89, jeda]
        y = np.concatenate(parts[:-1]); f = OUT / f'{nama}.flac'; sf.write(f, y, m.sr)
        h = whisper(f); lap.append(dict(varian=nama, rujukan=ruj.name, cfg=cfg, exaggeration=ex, suhu=suhu, whisper=h))
        print(f'{nama}: {h}', flush=True); semua += [y, jeda, jeda, jeda]
    sf.write(OUT / 'semua.flac', np.concatenate(semua), m.sr)
    json.dump(lap, open(OUT / 'laporan.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
