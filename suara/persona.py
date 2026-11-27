"""Persona = satu suara (satu orang). Setiap persona ada folder sendiri:
  persona/<nama>/persona.json   siapa, izin, terma
  persona/<nama>/bank/          rakaman bank + manifest.json
  persona/<nama>/rujukan/       klip rujukan lalai (<gaya>.flac)
  persona/<nama>/gaya/          <gaya>.json untuk tetapkan klip rujukan
  persona/<nama>/sampel/        sampel untuk didengar
Nama persona: SATU perkataan, huruf kecil a–z sahaja (contoh `fairuz`, `ahmad`). Bukan dua perkataan yang dicantum
(`ahmaddeedat`, `AhmadDeedat`): pilih satu nama sahaja (`ahmad` atau `deedat`)."""
import json, os, re
from datetime import date
from . import D

PERSONA = D / 'persona'
NAMA_SAH = re.compile(r'^[a-z]{2,20}$')
ATURAN = 'Nama persona mesti SATU perkataan, huruf kecil a–z sahaja, 2–20 huruf (contoh: fairuz). Jangan cantum dua perkataan (AhmadDeedat, ahmad_deedat).'


class Persona:
    def __init__(self, nama):
        self.nama = nama; self.dir = PERSONA / nama
        self.bank = self.dir / 'bank'; self.gaya = self.dir / 'gaya'; self.rujukan = self.dir / 'rujukan'; self.sampel = self.dir / 'sampel'
        self.manifest = self.bank / 'manifest.json'

    @property
    def info(self):
        f = self.dir / 'persona.json'
        return json.load(open(f, encoding='utf-8')) if f.exists() else dict(nama=self.nama)

    def rel(self, p):
        """laluan relatif kepada akar repo (untuk URL /audio)"""
        return str(p.relative_to(D))

    def __repr__(self):
        return f'Persona({self.nama})'


def semak_nama(nama):
    if not isinstance(nama, str) or not NAMA_SAH.match(nama):
        raise ValueError(f'"{nama}" bukan nama persona yang sah. {ATURAN}')
    return nama


def senarai():
    return sorted(p.name for p in PERSONA.glob('*') if (p / 'persona.json').exists() and NAMA_SAH.match(p.name))


def lalai():
    n = os.environ.get('SUARA_PERSONA') or ((PERSONA / 'lalai.txt').read_text().strip() if (PERSONA / 'lalai.txt').exists() else '')
    s = senarai()
    return n if n in s else (s[0] if s else 'fairuz')


def dapat(nama=None):
    nama = nama or lalai(); semak_nama(nama)
    if nama not in senarai():
        raise ValueError(f'Persona "{nama}" tiada. Ada: {", ".join(senarai()) or "(tiada)"}. Cipta: bin/suara persona baru {nama} --paparan "…" --izin')
    return Persona(nama)


def cipta(nama, paparan, keterangan='', izin=False):
    """izin=True bermaksud pemilik suara sendiri mengesahkan izin. Tanpa itu, persona tidak dicipta."""
    semak_nama(nama)
    if not izin:
        raise ValueError('Persona hanya boleh dicipta dengan izin pemilik suara itu sendiri (--izin / tanda kotak izin).')
    p = Persona(nama)
    if (p.dir / 'persona.json').exists(): raise ValueError(f'Persona "{nama}" sudah wujud.')
    for d in (p.bank, p.gaya, p.rujukan, p.sampel): d.mkdir(parents=True, exist_ok=True)
    json.dump(dict(nama=nama, paparan=paparan or nama.title(), bahasa='ms', keterangan=keterangan,
                   izin='Saya pemilik suara ini dan saya izinkan ia digunakan mengikut terma dalam README.md.',
                   terma='README.md#terma-guna-suara-saya', tarikh_izin=date.today().isoformat()),
              open(p.dir / 'persona.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return p
