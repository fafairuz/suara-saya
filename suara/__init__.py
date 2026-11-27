"""suara-saya: enjin suara peribadi (Chatterbox Multilingual V3, MIT), tempatan dan luar talian."""
import os
os.environ['HF_HUB_OFFLINE'] = '1'; os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'    # tiada apa keluar dari Mac ini
os.environ.setdefault('TQDM_DISABLE', '1'); os.environ.setdefault('TRANSFORMERS_VERBOSITY', 'error')
from pathlib import Path

VERSI = '0.1.0'
D = Path(__file__).resolve().parent.parent          # akar repo
MODEL = D / 'models' / 'chatterbox'
KERJA = D / 'kerja'
ISTILAH = D / 'istilah-saya.csv'
WHISPER_MODEL = os.environ.get('WHISPER_MODEL', os.path.expanduser('~/.local/share/whisper/models/ggml-large-v3-turbo.bin'))
