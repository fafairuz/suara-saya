# suara-saya

**Suara saya (pemilik repo ini) sebagai enjin TTS yang boleh dipakai sesiapa, dari projek apa pun.**
Teks Bahasa Melayu santai bercampur istilah English menjadi audio dalam suara saya. Semuanya jalan tempatan di mesin anda: tiada API, tiada langganan, dan teks atau audio tak dihantar ke mana-mana.

> *English summary:* a local, offline voice-clone TTS of my voice for Malay mixed with English tech terms.
> One CLI (`bin/suara`) that any project or AI agent (Claude Code, Codex, Cursor, Gemini, …) can call.
> Built on Chatterbox Multilingual V3 (MIT). Agents should read [AGENTS.md](AGENTS.md).

## Dengar dulu

| Fail | Apa |
|---|---|
| [sampel/asli-rakaman.flac](sampel/asli-rakaman.flac) | Rakaman **asli** suara saya, 12 s. Ini klip rujukan lalai. |
| [sampel/klon-1.flac](sampel/klon-1.flac) | Klon: "Bila dokumen sampai, sistem kira hash dia. Lepas tu, hash tu disimpan dalam blockchain sebagai cryptographic proof." |
| [sampel/klon-2.flac](sampel/klon-2.flac) | Klon: "Kita host LLM sendiri on-prem. Jadi data sensitif tak keluar langsung dari rangkaian agensi." |
| [sampel/klon-3.flac](sampel/klon-3.flac) | Klon: "Dashboard ni tunjuk status workflow secara real-time, dari request masuk sampai approval akhir." |
| [ujian/ab/semua-ABC.flac](ujian/ab/semua-ABC.flac) | Ujian ejaan sebutan: setiap ayat dibaca tiga kali (A asal, B sebutan cantum, C sebutan berjarak). |

Teks sampel ada dalam [sampel/teks.txt](sampel/teks.txt). GitHub tak memainkan FLAC dalam pelayar, jadi muat turun fail dan buka dengan pemain audio biasa.

## Terma guna suara saya

Suara ini milik saya. Anda **dibenarkan** memakainya untuk:

- video, taklimat, demo, tutorial, kandungan pembelajaran dan prototaip, termasuk projek kerja;
- narasi produk atau sistem yang anda bina sendiri.

Anda **tidak dibenarkan** memakainya untuk:

- menyamar sebagai saya, atau membuat orang percaya saya sendiri yang bercakap atau bersetuju dengan sesuatu;
- penipuan, *scam*, panggilan palsu, atau mengelak pengesahan suara atau identiti;
- kandungan politik, kebencian, lucah atau fitnah;
- melatih atau menjual model suara lain daripada bank suara ini.

Jika audio diterbitkan, nyatakan bahawa ia **suara AI (klon suara, dari repo suara-saya)**, contohnya dalam kapsyen atau kredit.
Audio ini juga ada tera air Perth yang tak didengar, daripada Chatterbox. Kalau ragu, tanya saya dulu.

## Keperluan

| | Minimum | Nota |
|---|---|---|
| Mesin | Mac Apple Silicon (`mps`), atau Linux/Windows dengan GPU NVIDIA (`cuda`) | CPU sahaja boleh, tapi sangat perlahan. |
| Python | 3.11 | `brew install python@3.11` |
| ffmpeg | wajib | `brew install ffmpeg` |
| whisper-cli | pilihan | `brew install whisper-cpp`, dengan model `ggml-large-v3-turbo.bin` di `~/.local/share/whisper/models/`. Ia dipakai untuk semak sendiri dan cuba semula, dan wajib untuk perakam. |
| Ruang | kira-kira 4.5 GB | `.venv` 1.3 GB dan model 3.0 GB. Kedua-duanya tidak masuk git. |

Kelajuan di Mac M-series: kira-kira 3 s kerja untuk setiap 1 s audio. Muat model ambil 15–25 s setiap panggilan.

## Mula (3 langkah)

```bash
git clone git@github.com:fafairuz/suara-saya.git
```

```bash
sh suara-saya/pasang.sh
```

```bash
suara-saya/bin/suara cakap "Kita host LLM sendiri on-prem." -o uji.wav
```

`pasang.sh` muat turun pakej Python dan model sekali sahaja, kemudian jalankan `bin/suara semak`. Selepas itu semuanya luar talian (`HF_HUB_OFFLINE=1`).

## Cara guna

### Dari terminal

```bash
bin/suara cakap "Teks anda di sini." -o keluar.wav        # .wav .flac .mp3 .m4a
bin/suara cakap "Satu ayat. Dua ayat." --gaya tegas -o a.mp3
echo "Teks panjang dari fail…" | bin/suara cakap - -o a.wav  # baca stdin
bin/suara cakap "…" --tanpa-semak -o a.wav                # lebih laju, tanpa semakan whisper
bin/suara cakap "…" --istilah istilah-projek-saya.csv -o a.wav
bin/suara sebut "Data PII ke MBI trust layer"             # tunjuk teks yang model baca, tanpa jana
bin/suara semak                                           # semak pemasangan
```

### Dari projek lain (banyak ayat sekali gus, model dimuat sekali)

Gunakan `jana` dengan fail JSON. Kontrak penuh ada dalam [docs/kontrak-suara.md](docs/kontrak-suara.md).

```bash
bin/suara jana --masuk ayat.json --keluar keluar/
```

```json
{
  "kontrak": 1,
  "bahasa": "ms",
  "gaya": "santai",
  "istilah": "/laluan/penuh/istilah.csv",
  "ayat": [
    {"id": "s1", "teks": "Dokumen boleh dipalsukan.", "benih": 7},
    {"id": "s2", "teks": "Cuma cryptographic proof yang dihantar ke MBI trust layer.", "benih": 7}
  ]
}
```

Hasilnya ialah `keluar/s1.wav`, `keluar/s2.wav` (mono, 24 kHz) dan `keluar/hasil.json`:

```json
{"enjin": {"nama": "suara-saya", "versi": "0.1.0", "model": "chatterbox-multilingual-v3", "gaya": "santai", "rujukan": "…"},
 "ayat": [{"id": "s1", "fail": "s1.wav", "teks_dihantar": "Dokumen boleh dipalsukan.", "skor_whisper": 0.98, "didengar": "…", "benih": 7}]}
```

- Kod keluar 0 bermaksud semua ayat dijana. Selain 0 bermaksud gagal, dan mesej ralat ke stderr.
- `skor_whisper` ialah `null` jika whisper tiada.

Contoh panggilan dari Python:

```python
import json, subprocess, pathlib
SUARA = pathlib.Path("~/kod/suara-saya/bin/suara").expanduser()
json.dump({"kontrak": 1, "bahasa": "ms", "gaya": "santai",
           "ayat": [{"id": "a1", "teks": "Selamat datang ke demo ni.", "benih": 7}]}, open("ayat.json", "w"))
subprocess.run([SUARA, "jana", "--masuk", "ayat.json", "--keluar", "suara-out"], check=True)
```

Contoh panggilan dari Node:

```js
import { execFileSync } from "node:child_process";
execFileSync(process.env.SUARA ?? "../suara-saya/bin/suara", ["cakap", "Helo semua.", "-o", "helo.wav"], { stdio: "inherit" });
```

**Petua:** biar projek anda baca laluan enjin dari pemboleh ubah `SUARA`, dengan lalai `../suara-saya/bin/suara`. Itulah cara [video-template](docs/kontrak-suara.md) mencarinya.

### Gaya

`--gaya` (atau `"gaya"` dalam JSON) memilih klip rujukan, dan klip itu menentukan nada.
Gaya sedia ada ialah `santai`, `tegas` dan `tanya`. Jika rakaman untuk gaya itu belum ada, enjin guna `santai`.
Klip rujukan dipilih ikut susunan ini:

1. `gaya/<gaya>.json`, contohnya `{"rujukan": "bank/llm/tegas-ayat-01.flac"}`;
2. ambilan ayat terbaik dalam `bank/`, 8–12 s, skor whisper ≥ 90%;
3. gabungan beberapa ambilan terbaik sehingga kira-kira 10 s;
4. `rujukan/<gaya>.flac`;
5. `rujukan/santai.flac`.

### Istilah dan sebutan

Model membaca akronim sebagai satu perkataan (contohnya LLM jadi "ilme"). Sebab itu teks diubah dahulu sebelum dibaca model:

- Istilah dalam CSV ditukar ke lajur `sebutan`, dengan sengkang dibuang: `LLM` → `elelem`, `PII` → `piiaiai`, `blockchain` → `blokcein`.
- Akronim lain yang ditulis huruf besar dieja huruf demi huruf: `GPU` → `jiipiiyu`.
- Nombor ditukar ke perkataan BM: `12.5%` → "dua belas perpuluhan lima peratus", `RM3000` → "tiga ribu ringgit".

Sari kata dan skrip anda kekal dengan ejaan asal. Hanya `teks_dihantar` yang berubah.

Anda boleh beri CSV istilah projek anda sendiri (`--istilah` atau `"istilah"` dalam JSON), dengan lajur yang sama seperti [istilah-saya.csv](istilah-saya.csv):

```csv
istilah,bentuk_tulisan,jenis,sebutan,maksud_bm,contoh_ayat
"LLM","LLM","AKRONIM","el-el-em","Model bahasa berskala besar","Kalau kita host LLM sendiri, …"
"Kubernetes","Kubernetes","EN","ku-ber-ne-tis","Platform orkestrasi kontena","Kita deploy guna Kubernetes."
```

Lajur `jenis` diisi `BM`, `EN` atau `AKRONIM`. Akronim dipadankan ikut huruf besar dan kecil; jenis lain tidak. Jika sesuatu istilah berbunyi pelik, ubah `sebutan`, kemudian semak dengan `bin/suara sebut "…"`.

## Rakam bank suara (untuk pemilik suara)

```bash
bin/suara rakam      # http://127.0.0.1:8765, localhost sahaja
```

Perakam ini halaman web tempatan. Pilih `istilah-saya.csv` (setiap istilah dirakam sebagai *perkataan* dan *dalam ayat*) atau [skrip-bank-suara.md](skrip-bank-suara.md) (241 ayat).

| Kekunci | Tindakan |
|---|---|
| **space** | rakam / henti |
| **enter** | simpan dan pergi ke item seterusnya |
| **r** | rakam semula |
| **p** | main |
| **← →** | item sebelum / selepas |
| **n** | item belum siap seterusnya |

*Shift*-klik pada satu ambilan untuk jadikan ia pilihan.

Selepas setiap rakaman, perakam buat empat perkara secara automatik:
- potong senyap;
- semak aras (*clipping*, terlalu perlahan, bunyi latar);
- whisper semak teks yang disebut;
- papar skor, dengan amaran jika rendah.

Fail disimpan sebagai `bank/<istilah>/<gaya>-<kata|ayat>-NN.flac` (48 kHz mono). Ambilan lama tak dipadam. Semua ambilan direkod dalam `bank/manifest.json`.

## Had yang diketahui

- **Skor whisper bukan telinga.** Whisper memadankan perkataan yang hampir sama, jadi dengar sendiri sebelum terbitkan.
- **Perkataan BM pendek atau berimbuhan kadang-kadang tergelincir.** Contohnya "cuma" jadi "kuma" dan "dipercayai" jadi "diperkayai". Cuba benih lain (`"benih"` atau `--benih`).
- **Istilah English yang dieja ikut sebutan kadang-kadang lebih teruk** daripada ejaan asal. Contohnya `hesh` untuk "hash". Ubah `sebutan` dalam CSV anda jika begitu.
- **Satu panggilan memuat model sekali** (15–25 s). Untuk banyak ayat, guna `jana` dengan satu JSON, bukan banyak panggilan `cakap`.
- Resemble AI mengisytiharkan Chatterbox sebagai *retired research* sejak Ogos 2026. Lesen MIT kekal.

## Struktur

```
bin/suara              arahan utama (memanggil .venv/bin/python -m suara)
suara/                 kod: sebutan.py, enjin.py, bank.py, dengar.py, model.py, rakam.py + rakam.html
istilah-saya.csv       istilah lalai dan sebutannya
gaya/                  <gaya>.json, untuk menetapkan klip rujukan secara manual
bank/                  rakaman bank suara (FLAC) + manifest.json
rujukan/santai.flac    klip rujukan lalai
sampel/                sampel untuk didengar
ujian/                 ujian A/B ejaan sebutan
docs/kontrak-suara.md  kontrak jana v1
AGENTS.md              panduan untuk ejen AI (Claude Code, Codex, …)
```

## Lesen

- Kod dan dokumen repo ini: MIT, lihat [LICENSE](LICENSE).
- Model Chatterbox: MIT (Resemble AI).
- Suara dan rakaman dalam `bank/`, `rujukan/` dan `sampel/`: tertakluk pada **Terma guna suara saya** di atas.
