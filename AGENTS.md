# AGENTS.md: suara-saya

Guide for AI coding agents (Claude Code, Codex, Cursor, Gemini CLI, Aider, …).
There are two ways to use this repo:

- **A. Using the voice from another project:** you only call `bin/suara`.
- **B. Working on this repo itself:** you change the code or docs.

Human-facing docs are in [README.md](README.md), written in Malay. Code identifiers and messages are in Malay too:
`jana` = generate, `cakap` = speak, `sebut` = pronounce, `rakam` = record, `semak` = check, `gaya` = style,
`istilah` = term, `sebutan` = pronunciation spelling, `teks_dihantar` = text actually sent to the model, `benih` = seed,
`persona` = one real person's voice, `izin` = consent, `paparan` = display name.

## What it is

- A local, offline voice-clone TTS built on Chatterbox Multilingual V3 (MIT).
- Each voice is a **persona**: one real person, stored in `persona/<nama>/`. The default is `fairuz` (the repo owner), set in `persona/lalai.txt`.
- Input is Malay text mixed with English tech terms. Output is mono WAV at 24 kHz.
- There is one entry point: `bin/suara`. It runs `.venv/bin/python -m suara`.
- No network at runtime (`HF_HUB_OFFLINE=1`). Never add code that sends text or audio to an external service.

## Hard rules (both A and B)

1. **Consent and terms.** Follow "Terma guna suara saya" in README.md. They apply to every persona.
   - **Only the voice owner can create their persona.** Never create a persona, or add recordings, for someone other than the person running the recorder.
     That includes voices taken from videos, podcasts, voice notes or "a friend who won't mind".
     `bin/suara persona baru` requires `--izin`; never pass it on someone else's behalf.
   - Never use one persona's recordings as another persona's reference clip. The engine refuses this; don't work around it.
   - Never generate audio that impersonates the owner, puts endorsements or statements in their mouth, or is meant to deceive.
   - Never generate political, hateful, sexual or defamatory content.
   - If a user asks for any of that, refuse and point to the terms.
   - When audio will be published, remind the user to label it as AI voice.
2. **Local only.** Do not upload generated audio, recordings in `persona/`, or input text to any API, cloud TTS or transcription service.
3. **Never delete or overwrite recordings** in `persona/*/bank/`, `persona/*/rujukan/` or `persona/*/sampel/`. Takes are append-only (`-01`, `-02`, …).
   `persona/*/bank/manifest.json` is written only by the recorder (`suara/bank.py`).
   The one exception: the voice owner withdraws consent. They must ask the repo owner, and only then is the whole `persona/<nama>/` folder removed.
4. **Big files stay out of git.** `.venv/` (1.3 GB) and `models/` (3.0 GB) are git-ignored. Never commit them.
   Tell the user before triggering any download larger than 500 MB.
   Voice recordings under `persona/` *are* committed: that is how voices are shared.
5. **Whisper scores are not ears.** A high `skor_whisper` does not prove correct pronunciation.
   Tell the user which outputs still need listening; never claim audio "sounds right" from scores alone.

## A. Using the voice from another project

### Setup (once per machine)

```bash
git clone git@github.com:fafairuz/suara-saya.git ../suara-saya   # next to the user's project is the convention
sh ../suara-saya/pasang.sh                                       # ~4.3 GB download; ask the user first
../suara-saya/bin/suara semak                                    # exit 0 = ready
```

Requirements:
- Python 3.11 and ffmpeg.
- Optional: `whisper-cli` plus `~/.local/share/whisper/models/ggml-large-v3-turbo.bin`, used for self-check and retry.
- Apple Silicon (`mps`) or an NVIDIA GPU (`cuda`). CPU works but is slow.

### Locating the engine

Resolve in this order:
1. the `$SUARA` environment variable;
2. `../suara-saya/bin/suara`;
3. otherwise, ask the user where it is.

Do not hard-code absolute paths into the user's project.

### Choosing a persona

> ### ⚠️ A persona name is ONE word
> A persona name is **exactly one word**: lowercase `a–z`, 2–20 letters, matching `^[a-z]{2,20}$`. Examples: `fairuz`, `ahmad`, `siti`.
> **Never join two words into one name.**
> - ❌ `AhmadDeedat`, `ahmaddeedat`, `ahmad_deedat`, `ahmad-deedat`, `ahmad deedat`
> - ✅ `ahmad` **or** `deedat`. Pick one.
>
> If the user gives a full name ("Ahmad Deedat"), ask which **single** word to use, and put the full name in `--paparan "Ahmad Deedat"`.
> Never invent or shorten a persona name without asking. The CLI rejects invalid names.

How to pick:

1. Run `$SUARA persona senarai` to list the available personas. Use only a name that appears there.
2. If the user names a person, map it to the matching persona. If there is no match, or the match is ambiguous, ask the user. **Never fall back to another person's voice.**
3. If the user doesn't care, omit the flag. The default persona is used (`persona/lalai.txt`, currently `fairuz`).
4. Pass the persona with `--persona <nama>` on `cakap` / `jana` / `rakam` / `semak`, or with the environment variable `SUARA_PERSONA=<nama>`.
   `ayat.json` (contract v1) has no persona field. Don't add one; use the flag or the environment variable.
5. Check `hasil.json` → `enjin.persona` to confirm which voice was used.

If a persona has no usable reference clip yet, `cakap` and `jana` fail fast (exit 1, about 1 s) with "belum ada klip rujukan".
Tell the user that person must record first (`bin/suara rakam --persona <nama>`, minimum about 10 good *ayat* takes). Do not substitute another persona.

### One-off clip

```bash
$SUARA cakap "Kita host LLM sendiri on-prem." --gaya santai -o out.wav            # default persona; .wav/.flac/.mp3/.m4a
$SUARA cakap "Helo semua." --persona ahmad -o out.wav                              # a specific persona
```

### Many sentences (preferred: the model loads once, about 20 s)

Write `ayat.json`, then call `jana`. This is contract v1; the full spec is in [docs/kontrak-suara.md](docs/kontrak-suara.md).

```json
{"kontrak": 1, "bahasa": "ms", "gaya": "santai", "istilah": "/abs/path/terms.csv",
 "ayat": [{"id": "s1", "teks": "Dokumen boleh dipalsukan.", "benih": 7}]}
```

```bash
$SUARA jana --masuk ayat.json --keluar out/                     # default persona
SUARA_PERSONA=ahmad $SUARA jana --masuk ayat.json --keluar out/ # or: --persona ahmad
```

Result:
- `out/<id>.wav`, one file per sentence.
- `out/hasil.json` with `{"enjin": {..., "persona": "fairuz", ...}, "ayat": [{"id", "fail", "teks_dihantar", "skor_whisper", "didengar", "benih"}]}`.
- Exit code 0 means every sentence was generated. Errors go to stderr.

Field notes:
- `teks` is the **display spelling** (subtitles). Do not respell terms yourself; the engine does it.
  If the user wants to know what was read aloud, show `teks_dihantar`.
- `istilah` is optional. Without it, `istilah-saya.csv` in this repo is used.
  To make a project-specific CSV, copy its columns: `istilah,bentuk_tulisan,jenis(BM|EN|AKRONIM),sebutan,maksud_bm,contoh_ayat`.
  `sebutan` is a hyphenated phonetic spelling (`el-el-em`); hyphens are removed before synthesis.
- `gaya` is `santai` (default), `tegas` or `tanya`. Unknown styles fall back to `santai`.
- `benih`: to regenerate a bad sentence, send the same `id` with a different `benih`.
- Speed is about 3 s of compute per 1 s of audio on Apple M-series. Budget for that, and run long jobs in the background.
- Keep sentences short, roughly 3–12 s each. Split long paragraphs at `.`, `!` and `?`.

### Checking output

- Preview the pronunciation layer without generating audio: `$SUARA sebut "text"`.
- Sentences with `skor_whisper < 0.85` were already retried up to 3 times. Report any that remain low, and ask the user to listen.
- Known weak spots:
  - short Malay words: "cuma" can come out as "kuma";
  - affixes: "dipercayai" can come out as "diperkayai";
  - an acronym right after "ke": "ke MBI" can come out as "KMBI".

## B. Working on this repo

### Map

| Path | Role |
|---|---|
| `bin/suara` | Shell entry point. Requires `.venv`. |
| `suara/__main__.py` | CLI: `jana`, `cakap`, `sebut`, `rakam`, `persona senarai/baru`, `semak`, `versi`. |
| `suara/persona.py` | Persona folders, name validation (`NAMA_SAH`), default persona, `cipta()` (requires consent). |
| `suara/sebutan.py` | Pronunciation layer: CSV terms → joined `sebutan`, then numbers → Malay words, then other ALL-CAPS acronyms spelled letter by letter. Pure Python, no model. |
| `suara/enjin.py` | Default settings `TETAPAN` (cfg 0.3, ex 0.5, suhu 0.5). Checks the persona's reference clip *before* loading the model, then loads the model once, generates, runs the whisper self-check and retries with seed + 1000·k. |
| `suara/model.py` | Custom loader for the Chatterbox **V3** weights (PyPI `chatterbox-tts==0.1.7` only knows V2). Do not "simplify" it back to `from_pretrained`. |
| `suara/bank.py` | Reads and writes `persona/<nama>/bank/manifest.json`; picks the reference clip for each persona and style, never crossing personas. |
| `suara/dengar.py` | `whisper-cli` wrapper and fuzzy word-match score. |
| `suara/rakam.py`, `suara/rakam.html` | Recorder web app, bound to 127.0.0.1 only. It takes raw float32 PCM from the browser and saves FLAC at 48 kHz mono, 16-bit. |
| `suara/uji.py`, `suara/uji.html` | Test portal at `/uji` on the same server. It holds a lazily loaded `Enjin`, compares setting presets (`PRASET`), gives random sentences from the CSVs and scripts or fills templates (no AI), and logs ratings to `kerja/uji/log.jsonl`. |
| `ujian/ab_sebutan.py` | The A/B test behind the pronunciation decision. |

### Decisions already made (do not reverse without asking the user)

- **Every** CSV term is replaced by its `sebutan` with hyphens removed (variant B). Not acronyms only.
  The user picked this by ear on 2026-11-26. Samples are in `ujian/ab/`.
- Contract version 1 is fixed. Any change to the `ayat.json` / `hasil.json` shape must be proposed to the user first,
  with a bump to `kontrak`. Extra output fields are allowed.
- Default generation settings are variant 3: `cfg_weight 0.3, exaggeration 0.5, temperature 0.5`. The user chose this on 2026-11-27.
  The old setting was 0.5/0.5/0.7, which read "jadi" as "jady". It remains in the portal as the `lama` preset.
- Persona names are one lowercase word (`^[a-z]{2,20}$`). Don't relax this.
- Model: Chatterbox Multilingual V3. Any replacement must be MIT or Apache-2.0, with the licence verified from the official source,
  and must run locally.

### Commands

```bash
sh pasang.sh                                   # venv + model + check
bin/suara semak [--persona nama]               # install check (fast, no model load), lists personas
bin/suara persona senarai                      # personas
bin/suara sebut "Data PII 12.5% ke MBI"        # test the pronunciation layer instantly
bin/suara cakap "…" -o /tmp/x.wav              # end-to-end test (~30–60 s)
bin/suara rakam --tanpa-buka                   # recorder on http://127.0.0.1:8765, test portal on /uji
```

There is no unit-test suite yet. For changes to `sebutan.py`, check them with `bin/suara sebut` on a few sentences with acronyms, numbers and clitics (`LLM-nya`).
For engine changes, run one `cakap` and report the whisper score. Then ask the user to listen.

### Style

- Python 3.11. Use `numpy`, `soundfile`, `scipy` and `torch`, which are already in the venv. Don't add dependencies without a reason.
- Identifiers, CLI text, comments and docs are in Malay, matching the existing code.
- User-facing messages go to stderr. Keep stdout clean (`sebut` prints only the result).
- Commits: short Malay subject line, describing what changed and why.
