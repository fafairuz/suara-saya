#!/bin/sh
# Pasang suara-saya: venv Python 3.11 + Chatterbox Multilingual V3 (MIT), kemudian semak.
# Sekali sahaja: ~1.3 GB pakej Python + ~3.0 GB model (fail V3 multilingual sahaja). Selepas itu luar talian.
set -e
D=$(cd "$(dirname "$0")" && pwd)
PY311=${PY311:-$(command -v python3.11 || true)}
[ -n "$PY311" ] || { echo "Perlu python3.11 (brew install python@3.11)"; exit 1; }
for t in ffmpeg whisper-cli; do command -v $t >/dev/null || { echo "Perlu $t (brew install ffmpeg whisper-cpp)"; exit 1; }; done
[ -x "$D/.venv/bin/python" ] || "$PY311" -m venv "$D/.venv"
"$D/.venv/bin/pip" install -q --upgrade pip
"$D/.venv/bin/pip" install -q -r "$D/requirements.txt"
if [ ! -f "$D/models/chatterbox/t3_mtl23ls_v3.safetensors" ]; then
  echo "Muat turun model Chatterbox V3 (~3.0 GB)…"
  HF_HUB_DISABLE_TELEMETRY=1 HF_HOME="$D/models/.hf" "$D/.venv/bin/python" -c "
from huggingface_hub import snapshot_download
snapshot_download('ResembleAI/chatterbox', local_dir='$D/models/chatterbox', allow_patterns=[
  've.pt', 't3_mtl23ls_v3.safetensors', 's3gen_v3.safetensors', 'grapheme_mtl_merged_expanded_v1.json', 'conds.pt', 'Cangjie5_TC.json', 'README.md'])"
  rm -rf "$D/models/.hf"
fi
W=${WHISPER_MODEL:-$HOME/.local/share/whisper/models/ggml-large-v3-turbo.bin}
[ -f "$W" ] || echo "AMARAN: model whisper tiada di $W (perlu untuk semakan)"
"$D/bin/suara" semak
echo "Siap. venv $(du -sh "$D/.venv" | cut -f1), model $(du -sh "$D/models" | cut -f1)."
