# Kontrak enjin suara (versi 1)

`sh build.sh --voice clone` tidak menjana suara sendiri. Ia memanggil **enjin suara** luar (repo `suara-saya`)
melalui satu arahan. Mana-mana enjin yang ikut kontrak ini boleh dipakai.

## Mencari enjin

Ikut susunan ini:
1. `SUARA=/laluan/ke/arahan sh build.sh --voice clone`
2. `../suara-saya/bin/suara` (repo `suara-saya` di sebelah folder ini)
3. `tts/enjin` (enjin sementara dalam template ini, Chatterbox zero-shot tanpa ejaan sebutan)

## Panggilan

```bash
<SUARA> jana --masuk <ayat.json> --keluar <folder>
```

Kod keluar 0 bermaksud semua ayat dijana. Selain 0 bermaksud gagal; mesej ralat ke stderr.

### `ayat.json` (dari template)

```json
{
  "kontrak": 1,
  "bahasa": "ms",
  "gaya": "santai",
  "istilah": "/laluan/penuh/istilah-saya.csv",
  "ayat": [
    {"id": "s1-0", "teks": "Dokumen boleh dipalsukan.", "benih": 7},
    {"id": "s3-1", "teks": "Melalui secure integration interface, cuma cryptographic proof yang dihantar.", "benih": 7}
  ]
}
```

- `teks` ialah ejaan sari kata (bentuk tulisan). Enjin sendiri yang menukarnya ke ejaan sebutan
  (contohnya lajur `sebutan` dalam `istilah`) jika perlu.
- `gaya` memilih suara atau intonasi enjin (contoh `santai`, `tegas`). Enjin guna gaya lalai jika tidak kenal.
- `benih` ialah benih rawak. Template menghantar benih lain bila ia minta ayat yang sama dijana semula.

### Hasil (dari enjin)

- `<folder>/<id>.wav`: satu fail setiap ayat, mono, sekurang-kurangnya 24 kHz. Senyap di hujung tak mengapa.
- `<folder>/hasil.json`:

```json
{
  "enjin": {"nama": "suara-saya", "versi": "0.1.0", "model": "chatterbox-multilingual-v3", "gaya": "santai"},
  "ayat": [{"id": "s1-0", "fail": "s1-0.wav", "teks_dihantar": "Dokumen boleh dipalsukan."}]
}
```

`teks_dihantar` ialah teks sebenar yang dibaca model (selepas tukar ejaan). Ia dipapar dalam laporan semakan.

## Apa yang template buat selepas itu

1. Potong senyap di awal dan hujung, tukar ke 48 kHz.
2. Whisper (tempatan) setiap ayat dan bandingkan dengan skrip.
3. Ayat dengan padanan bawah 85%: minta semula dengan benih lain, sehingga 3 cubaan. Ambil yang terbaik.
4. Masa setiap perkataan dari whisper → `script/timing.json`, sama seperti mod rakaman.
5. Laporan semakan menyenaraikan ayat yang masih lemah.

Semua audio kekal di Mac. Enjin tidak boleh menghantar teks atau suara ke servis luar.
