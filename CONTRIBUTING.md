# Menyumbang suara (persona baru)

Terima kasih! Setiap suara dalam repo ini ialah satu **persona**: suara seorang manusia sebenar, dirakam oleh orang itu sendiri.

## Syarat

1. **Suara anda sendiri sahaja.** Jangan sekali-kali rakam, muat naik atau cipta persona untuk suara orang lain, termasuk rakaman YouTube, podcast atau mesej suara. Ini juga terpakai walaupun orang itu "mesti tak kisah".
2. **Anda bersetuju dengan [terma guna suara](README.md#terma-guna-suara-saya).** Sesiapa yang ada akses repo boleh menjana audio dalam suara anda mengikut terma itu.
3. **Nama persona mesti SATU perkataan**, huruf kecil a–z, 2–20 huruf.

   | ✅ Betul | ❌ Salah |
   |---|---|
   | `ahmad` | `AhmadDeedat` (dua perkataan dicantum, huruf besar) |
   | `deedat` | `ahmaddeedat` (dua perkataan dicantum) |
   | `siti` | `ahmad_deedat`, `ahmad-deedat`, `ahmad deedat` |

   Pilih **satu** nama sahaja. Nama penuh boleh ditulis dalam `--paparan "Ahmad Deedat"`.

## Langkah

### 1. Pasang (sekali)

```bash
git clone git@github.com:fafairuz/suara-saya.git && cd suara-saya
```

```bash
sh pasang.sh
```

Muat turun kira-kira 4.3 GB (pakej Python dan model). Perakam perlukan `whisper-cli`; lihat bahagian Keperluan dalam README.

### 2. Cipta persona anda

```bash
bin/suara persona baru ahmad --paparan "Ahmad" --keterangan "suara taklimat, loghat utara" --izin
```

`--izin` bermaksud: *saya pemilik suara ini dan saya izinkan ia digunakan ikut terma README.* Tanpa `--izin`, persona tidak dicipta.

Anda juga boleh cipta persona dari perakam: butang **+ persona**, kemudian tandakan kotak izin.

### 3. Rakam

```bash
bin/suara rakam --persona ahmad
```

- **Minimum:** 10 item *AYAT* yang bagus dalam gaya `santai`, dengan skor whisper ≥ 90% dan tanpa amaran. Ini cukup untuk enjin memilih klip rujukan kira-kira 10 s.
- **Disyorkan:** beberapa ayat BM tulen dari `skrip-bank-suara.md`, dan item *AYAT* dari `istilah-video-integriti.csv`.
- **Lebih baik:** satu fail penuh, contohnya `istilah-saya.csv` atau `skrip-bank-suara.md`. Bank penuh berguna untuk fine-tune pada masa depan.
- Ikut arahan rakaman dalam halaman: jarak mikrofon 15–20 cm, bilik senyap, minum air.

### 4. Uji

Buka http://127.0.0.1:8765/uji, pilih persona anda, kemudian jana beberapa ayat. Atau dari terminal:

```bash
bin/suara semak --persona ahmad
```

```bash
bin/suara cakap "Jadi data sensitif tak keluar langsung dari rangkaian agensi." --persona ahmad -o uji.wav
```

### 5. Sampel untuk orang lain dengar

Letak satu rakaman asli anda dan tiga klip klon dalam `persona/ahmad/sampel/`:

```bash
cp persona/fairuz/sampel/teks.txt persona/ahmad/sampel/teks.txt
```

```bash
i=0; while IFS= read -r t; do i=$((i+1)); bin/suara cakap "$t" --persona ahmad -o persona/ahmad/sampel/klon-$i.flac; done < persona/ahmad/sampel/teks.txt
```

Untuk rakaman asli, salin satu ambilan *ayat* yang bagus dari `persona/ahmad/bank/…` ke `persona/ahmad/sampel/asli-rakaman.flac`.

### 6. Hantar

Ubah **hanya** `persona/<nama>/`:

```bash
git checkout -b persona-ahmad
```

```bash
git add persona/ahmad && git commit -m "Tambah persona ahmad" && git push -u origin persona-ahmad
```

Kemudian buka pull request. Satu gaya penuh (kira-kira 40 minit rakaman) ialah sekitar 100 MB FLAC.

## Tarik balik izin

Pemilik suara boleh minta persona dibuang bila-bila masa. Buka isu atau hubungi pemilik repo, dan folder `persona/<nama>/` akan dipadam.
Audio yang dah dijana dan disimpan orang lain sebelum itu tak dapat ditarik balik.
