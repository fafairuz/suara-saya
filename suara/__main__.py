"""bin/suara <arahan>
  jana  --masuk ayat.json --keluar DIR        kontrak v1 (video-template)
  cakap "teks" [--gaya santai] -o fail.wav    guna pantas (teks "-" = baca stdin)
  sebut "teks"                                tunjuk teks_dihantar sahaja (tanpa model)
  rakam [--port 8765] [--fail istilah-saya.csv]  perakam bank suara (localhost)
  semak                                        semak pemasangan"""
import argparse, shutil, sys
from . import VERSI, MODEL, WHISPER_MODEL, ISTILAH, D


def semak():
    ok = True
    def baris(lulus, teks):
        nonlocal ok; ok &= bool(lulus); print(('  ok    ' if lulus else '  GAGAL ') + teks)
    print(f'suara-saya {VERSI} ({D})')
    for f in ('ve.pt', 't3_mtl23ls_v3.safetensors', 's3gen_v3.safetensors', 'grapheme_mtl_merged_expanded_v1.json'):
        baris((MODEL / f).exists(), f'model/{f}')
    baris(shutil.which('ffmpeg'), 'ffmpeg'); baris(shutil.which('whisper-cli'), 'whisper-cli')
    from pathlib import Path
    baris(Path(WHISPER_MODEL).exists(), f'model whisper {WHISPER_MODEL}')
    baris(ISTILAH.exists(), f'istilah {ISTILAH.name}')
    try:
        import torch, chatterbox  # noqa: F401
        baris(True, f'torch {torch.__version__}, mps={torch.backends.mps.is_available()}')
    except Exception as e:
        baris(False, f'import: {e}')
    from .bank import rujukan
    try:
        print('  gaya santai -> ' + rujukan('santai')[1])
    except SystemExit as e:
        baris(False, str(e))
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(prog='suara', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    j = sp.add_parser('jana'); j.add_argument('--masuk', required=True); j.add_argument('--keluar', required=True)
    c = sp.add_parser('cakap'); c.add_argument('teks'); c.add_argument('--gaya', default='santai')
    c.add_argument('-o', '--keluar', default='suara.wav'); c.add_argument('--benih', type=int, default=7)
    c.add_argument('--tanpa-semak', action='store_true', help='jangan semak dengan whisper / cuba semula')
    s = sp.add_parser('sebut'); s.add_argument('teks')
    r = sp.add_parser('rakam'); r.add_argument('--port', type=int, default=8765); r.add_argument('--fail', default=str(ISTILAH))
    r.add_argument('--tanpa-buka', action='store_true')
    sp.add_parser('semak'); sp.add_parser('versi')
    a = ap.parse_args()
    if a.cmd == 'jana':
        from .enjin import jana; jana(a.masuk, a.keluar)
    elif a.cmd == 'cakap':
        from .enjin import cakap; cakap(a.teks, a.gaya, a.keluar, a.benih, not a.tanpa_semak)
    elif a.cmd == 'sebut':
        from .sebutan import tukar; print(tukar(a.teks))
    elif a.cmd == 'rakam':
        from .rakam import jalan; jalan(a.port, a.fail, not a.tanpa_buka)
    elif a.cmd == 'semak':
        semak()
    elif a.cmd == 'versi':
        print(VERSI)


if __name__ == '__main__':
    main()
