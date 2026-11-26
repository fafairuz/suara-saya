# suara-saya

Enjin suara peribadi: teks BM santai bercampur istilah English → audio dalam suara saya.
Ia jalan **tempatan** di Mac (Apple Silicon, `mps`). Selepas pasang, ia jalan luar talian, dan teks atau audio tak dihantar ke mana-mana.
Model: Chatterbox Multilingual V3 (MIT, Resemble AI), *zero-shot* dari klip rujukan bank suara saya.

## 1. Pasang

```bash
sh pasang.sh
```

- Perlu `python3.11`, `ffmpeg` dan `whisper-cli` (`brew install python@3.11 ffmpeg whisper-cpp`).
- Perlu model whisper di `~/.local/share/whisper/models/ggml-large-v3-turbo.bin`.
- Muat turun sekali sahaja: kira-kira 1.3 GB pakej Python ke `.venv/` dan 3.0 GB model ke `models/`. Kedua-duanya tak masuk git.
- Semak pemasangan bila-bila masa dengan `bin/suara semak`.

## 2. Rakam bank suara

```bash
bin/suara rakam                 # buka http://127.0.0.1:8765 (localhost sahaja)
```

- Pilih fail: `istilah-saya.csv` (setiap istilah dirakam dua kali: *perkataan sahaja* dan *dalam ayat*), atau `skrip-bank-suara.md` (241 ayat).
  Fail `.txt` juga boleh, dengan satu ayat sebaris.
- Pilih gaya: `santai`, `tegas` atau `tanya`. Tambah gaya baru dengan butang **+ gaya**.
- Kawalan papan kekunci:

  | Kekunci | Tindakan |
  |---|---|
  | **space** | rakam / henti |
  | **enter** | simpan dan pergi ke item seterusnya |
  | **r** | rakam semula |
  | **p** | main semula |
  | **← →** | item sebelum / selepas |
  | **n** | item belum siap seterusnya |

  *Shift*-klik pada satu ambilan untuk jadikan ia pilihan.
- Selepas setiap rakaman, perakam buat empat perkara secara automatik:
  - potong senyap;
  - semak aras (*clipping*, terlalu perlahan, bunyi latar);
  - whisper semak teks yang disebut;
  - papar skor, dengan amaran jika rendah.
- Fail disimpan di `bank/<istilah>/<gaya>-<kata|ayat>-NN.flac` (48 kHz mono). Ambilan lama tak dipadam.
  Semua ambilan direkod dalam `bank/manifest.json`.
- Sesi boleh disambung. Halaman bermula pada item terakhir, dan kemajuan dipapar di atas (contoh "87/205 istilah, gaya santai").

## 3. Uji suara

```bash
bin/suara cakap "Kita host LLM sendiri on-prem." --gaya santai -o uji.wav
bin/suara sebut "Data PII dihantar ke MBI trust layer."    # tunjuk teks yang dibaca model, tanpa jana
```

`cakap` boleh keluarkan `.wav`, `.flac`, `.mp3` atau `.m4a`. Teks `-` bermaksud baca dari stdin. Untuk laju, guna `--tanpa-semak` (tiada semakan whisper).

## 4. Guna dari video-template

```bash
sh ../video-template/build.sh --voice clone          # GAYA=tegas sh ... untuk gaya lain
```

`video-template` cari `../suara-saya/bin/suara` secara automatik. Kontraknya ada di `video-template/docs/kontrak-suara.md` (versi 1):

```bash
bin/suara jana --masuk ayat.json --keluar DIR    # DIR/<id>.wav + DIR/hasil.json
```

## Cara ia berfungsi

1. **Lapisan sebutan** (`suara/sebutan.py`). Teks sari kata diubah dahulu sebelum dihantar ke model.
   Ini ikut keputusan ujian A/B 26 Nov 2026, yang ada dalam `ujian/`.
   - Setiap istilah dalam `istilah-saya.csv` ditukar ke lajur `sebutan` tanpa sengkang (`LLM` → `elelem`, `PII` → `piiaiai`).
   - Akronim lain dieja huruf demi huruf (`GPU` → `jiipiiyu`).
   - Nombor ditukar ke perkataan BM (`12.5%` → "dua belas perpuluhan lima peratus").
   - Teks yang dibaca model dipulangkan sebagai `teks_dihantar` dalam `hasil.json`.
2. **Gaya → klip rujukan** (`suara/bank.py`). Klip dicari ikut susunan ini:
   1. `gaya/<gaya>.json` dengan `{"rujukan": "bank/…/x.flac"}`;
   2. ambilan *ayat* terbaik dalam bank, 8–12 s, skor whisper ≥ 90%, banyak istilah;
   3. gabungan beberapa ambilan *ayat* terbaik sehingga kira-kira 10 s;
   4. `rujukan/<gaya>.flac`;
   5. `rujukan/santai.flac` (12 s rakaman MBI).
3. **Semak sendiri.** Setiap ayat ditranskrip oleh whisper. Jika skor di bawah 85%, ayat dijana semula dengan benih lain, sehingga 3 cubaan. Yang terbaik dipulangkan.

## Had yang diketahui

- **Skor whisper bukan telinga.** Whisper memadankan perkataan yang hampir sama, jadi "diperkayai" masih dikira betul. Dengar sendiri.
- **Perkataan BM pendek atau berimbuhan masih boleh tergelincir.** Contohnya "cuma" jadi "kuma" dan "dipercayai" jadi "diperkayai". Lapisan sebutan tak menyentuh perkataan BM yang tiada dalam CSV.
- **Akronim di awal ayat atau selepas "ke" kadang-kadang dicantum.** Contohnya "ke MBI" jadi "KMBI". Cuba semula selalunya membantu.
- Output ada tera air Perth (tak didengar) dari Chatterbox.
- Resemble AI mengisytiharkan Chatterbox sebagai *retired research* sejak Ogos 2026. Tiada kemas kini lagi, tetapi lesen MIT kekal.
