"""Whisper tempatan (whisper-cli) dan skor padanan teks. Tiada apa dihantar keluar."""
import difflib, os, re, subprocess, tempfile, unicodedata
from . import WHISPER_MODEL

HALU = {'terimakasihkeranamenonton', 'terimakasih', 'thankyouforwatching', 'thankyou', 'subtitlesbytheamaraorgcommunity'}


def ffmpeg(*a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def whisper(wav, lang='ms'):
    """transkrip satu fail audio (apa-apa format ffmpeg boleh baca)"""
    with tempfile.TemporaryDirectory() as td:
        w16 = os.path.join(td, 'a.wav')
        ffmpeg('-i', str(wav), '-ar', '16000', '-ac', '1', w16)
        r = subprocess.run(['whisper-cli', '-m', WHISPER_MODEL, '-l', lang, '-nt', '-np', '-f', w16], capture_output=True, text=True)
    t = ' '.join(r.stdout.split())
    return '' if norm(t).replace(' ', '') in HALU else t


def norm(t):
    t = unicodedata.normalize('NFKD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return ' '.join(re.sub(r"[^\w\s]", ' ', t.replace('-', '')).split())


def skor(rujuk, didengar):
    """pecahan perkataan rujukan yang didengar (padanan hampir >= 75% dikira, macam video-template)"""
    a, b = norm(rujuk).split(), norm(didengar).split()
    if not a: return 1.0
    if not b: return 0.0
    ok = 0.0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal': ok += i2 - i1
        elif tag == 'replace':
            # cuba padankan gabungan (whisper mungkin cantum/pecah perkataan)
            ra, rb = ''.join(a[i1:i2]), ''.join(b[j1:j2])
            r = difflib.SequenceMatcher(None, ra, rb).ratio()
            if r >= 0.75: ok += (i2 - i1) * r
    return round(ok / len(a), 3)


def skor_terbaik(didengar, *rujukan):
    return max(skor(r, didengar) for r in rujukan if r)
