"""Pemuat Chatterbox Multilingual V3. Pakej PyPI 0.1.7 hanya kenal V2, jadi fail V3 dimuat sendiri."""
import sys
from . import MODEL


def device():
    import torch
    if torch.cuda.is_available(): return 'cuda'
    return 'mps' if torch.backends.mps.is_available() else 'cpu'


def muat(dev=None):
    import logging, warnings
    warnings.filterwarnings('ignore'); logging.getLogger('chatterbox').setLevel(logging.ERROR)
    import torch
    from safetensors.torch import load_file
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from chatterbox.models.voice_encoder import VoiceEncoder
    from chatterbox.models.t3 import T3
    from chatterbox.models.t3.modules.t3_config import T3Config
    from chatterbox.models.s3gen import S3Gen
    from chatterbox.models.tokenizers import MTLTokenizer
    if not (MODEL / 't3_mtl23ls_v3.safetensors').exists():
        sys.exit(f'Model tiada di {MODEL}. Jalankan: sh pasang.sh')
    dev = dev or device()
    ve = VoiceEncoder(); ve.load_state_dict(torch.load(MODEL / 've.pt', map_location='cpu', weights_only=True)); ve.to(dev).eval()
    t3 = T3(T3Config.multilingual()); st = load_file(MODEL / 't3_mtl23ls_v3.safetensors')
    t3.load_state_dict(st['model'][0] if 'model' in st else st); t3.to(dev).eval()
    s3 = S3Gen(); r = s3.load_state_dict(load_file(MODEL / 's3gen_v3.safetensors'), strict=False)
    # fail .safetensors tak simpan dua penimbal tetap (penapis mel, tetingkap); selain itu ialah ralat
    assert set(r.missing_keys) <= {'tokenizer._mel_filters', 'tokenizer.window'} and not r.unexpected_keys, r
    s3.to(dev).eval()
    tok = MTLTokenizer(str(MODEL / 'grapheme_mtl_merged_expanded_v1.json'))
    return ChatterboxMultilingualTTS(t3, s3, ve, tok, dev)
