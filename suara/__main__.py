"""bin/suara <arahan>
  jana  --masuk ayat.json --keluar DIR [--persona nama]   kontrak v1 (video-template)
  cakap "teks" [--persona nama] [--gaya santai] -o fail.wav   guna pantas (teks "-" = baca stdin)
  sebut "teks"                                tunjuk teks_dihantar sahaja (tanpa model)
  rakam [--persona nama] [--port 8765]        perakam bank suara + portal uji (localhost)
  persona senarai | persona baru <nama> --paparan "Nama" --izin
  semak                                       semak pemasangan
Persona boleh juga ditetapkan dengan SUARA_PERSONA=<nama>. Lalai: persona/lalai.txt.
Nama persona: SATU perkataan huruf kecil (contoh: fairuz). Bukan dua perkataan dicantum (AhmadDeedat)."""
import argparse, shutil, sys
from . import VERSI, MODEL, WHISPER_MODEL, ISTILAH, D


def semak(persona=None):
    ok = True
    def baris(lulus, teks):
        nonlocal ok; ok &= bool(lulus); print(('  ok    ' if lulus else '  GAGAL ') + teks)
    print(f'suara-saya {VERSI} ({D})')
    for f in ('ve.pt', 't3_mtl23ls_v3.safetensors', 's3gen_v3.safetensors', 'grapheme_mtl_merged_expanded_v1.json'):
        baris((MODEL / f).exists(), f'model/{f}')
    baris(shutil.which('ffmpeg'), 'ffmpeg')
    from pathlib import Path
    w = shutil.which('whisper-cli') and Path(WHISPER_MODEL).exists()
    print(('  ok    ' if w else '  pilihan ') + f'whisper-cli + {WHISPER_MODEL}' + ('' if w else ' (tiada: jana tanpa semakan; perakam perlukannya)'))
    baris(ISTILAH.exists(), f'istilah {ISTILAH.name}')
    try:
        import torch, chatterbox  # noqa: F401
        baris(True, f'torch {torch.__version__}, mps={torch.backends.mps.is_available()}')
    except Exception as e:
        baris(False, f'import: {e}')
    from .persona import senarai, lalai
    from .bank import rujukan, baca
    ps = senarai(); baris(bool(ps), f'persona: {", ".join(ps) or "(tiada)"}; lalai: {lalai()}')
    for n in ([persona] if persona else ps):
        try:
            print(f'  {n}: {len(baca(n)["ambilan"])} ambilan bank; gaya santai -> {rujukan(n, "santai")[1]}')
        except (SystemExit, ValueError) as e:
            print(f'  {n}: {e}')
    sys.exit(0 if ok else 1)


def persona_cmd(a):
    from .persona import senarai, lalai, cipta, Persona, ATURAN
    if a.tindakan == 'senarai':
        for n in senarai():
            i = Persona(n).info
            print(f"{n}{' (lalai)' if n == lalai() else ''}\t{i.get('paparan', '')}\t{i.get('keterangan', '')}")
    elif a.tindakan == 'baru':
        if not a.nama: sys.exit('Beri nama: bin/suara persona baru <nama> --paparan "Nama" --izin\n' + ATURAN)
        try:
            p = cipta(a.nama, a.paparan, a.keterangan or '', a.izin)
        except ValueError as e:
            sys.exit(str(e))
        print(f'Persona {p.nama} dicipta di {p.dir.relative_to(D)}. Seterusnya: bin/suara rakam --persona {p.nama}', file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(prog='suara', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    j = sp.add_parser('jana'); j.add_argument('--masuk', required=True); j.add_argument('--keluar', required=True)
    j.add_argument('--persona', help='nama persona (lalai: SUARA_PERSONA atau persona/lalai.txt)')
    c = sp.add_parser('cakap'); c.add_argument('teks'); c.add_argument('--gaya', default='santai'); c.add_argument('--persona')
    c.add_argument('-o', '--keluar', default='suara.wav'); c.add_argument('--benih', type=int, default=7)
    c.add_argument('--istilah', help='CSV istilah sendiri (lalai: istilah-saya.csv)')
    c.add_argument('--tanpa-semak', action='store_true', help='jangan semak dengan whisper / cuba semula')
    s = sp.add_parser('sebut'); s.add_argument('teks'); s.add_argument('--istilah')
    r = sp.add_parser('rakam'); r.add_argument('--port', type=int, default=8765); r.add_argument('--fail', default=str(ISTILAH))
    r.add_argument('--persona'); r.add_argument('--tanpa-buka', action='store_true')
    pe = sp.add_parser('persona'); pe.add_argument('tindakan', choices=['senarai', 'baru']); pe.add_argument('nama', nargs='?')
    pe.add_argument('--paparan', help='nama paparan, contoh "Ahmad"'); pe.add_argument('--keterangan')
    pe.add_argument('--izin', action='store_true', help='saya pemilik suara ini dan izinkan ia digunakan ikut terma README')
    sm = sp.add_parser('semak'); sm.add_argument('--persona'); sp.add_parser('versi')
    a = ap.parse_args()
    try:
        if a.cmd == 'jana':
            from .enjin import jana; jana(a.masuk, a.keluar, a.persona)
        elif a.cmd == 'cakap':
            from .enjin import cakap; cakap(a.teks, a.gaya, a.keluar, a.benih, not a.tanpa_semak, a.istilah, a.persona)
        elif a.cmd == 'sebut':
            from .sebutan import tukar; print(tukar(a.teks, a.istilah))
        elif a.cmd == 'rakam':
            from .rakam import jalan; jalan(a.port, a.fail, not a.tanpa_buka, a.persona)
        elif a.cmd == 'persona':
            persona_cmd(a)
        elif a.cmd == 'semak':
            semak(a.persona)
        elif a.cmd == 'versi':
            print(VERSI)
    except ValueError as e:           # contoh: nama persona tak sah / tiada
        sys.exit(str(e))


if __name__ == '__main__':
    main()
