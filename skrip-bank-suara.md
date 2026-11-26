# Skrip bank suara (untuk klon suara, Bahagian B)

**Tujuan:** beri model contoh suara anda menyebut istilah teknikal BM–English dalam ayat penuh.
Anggaran 21 minit bacaan (241 ayat, 2525 perkataan), dalam 5 sesi lebih kurang 5 minit.

## Arahan rakaman

1. **Tempat:** bilik senyap dan "mati" (langsir, almari baju, tilam). Matikan kipas/aircond jika boleh.
2. **Telefon:** mod pesawat, 15–20 cm dari mulut, sedikit ke tepi (elak hembusan "p"/"b"). Apl rakaman suara biasa (m4a) sudah cukup.
3. **Cara baca:** santai macam beri taklimat, bukan macam baca berita. Kelajuan biasa anda. Satu ayat, jeda 1 saat, ayat seterusnya.
4. **Tersilap?** Berhenti, jeda, baca semula ayat tu dari mula. Skrip template akan ambil ambilan terakhir.
5. **Satu fail setiap sesi:** `bank-01.m4a`, `bank-02.m4a` … dalam `tts/bank/`. Minum air antara sesi.
6. **Konsisten:** tempat, jarak dan nada yang sama untuk semua sesi.

Nombor dan tarikh ditulis dalam perkataan supaya sebutan anda jelas.


## Sesi 01 (fail `bank-01.m4a`)

1. Untuk projek ni, AI bantu pegawai semak dokumen yang masuk.
2. Kita bagi model bahasa tu satu contoh ayat taklimat dulu.
3. Kalau kita host LLM sendiri, pasukan kena jaga kapasiti pelayan.
4. Dalam prompt tu, tulis siapa yang akan dengar taklimat ni.
5. Satu perkataan BM kadang-kadang dipecahkan kepada beberapa token.
6. Masa inference tu kita ukur dari permintaan masuk sampai jawapan siap.
7. Untuk uji reasoning, kita bagi model dua syarat yang dia kena padankan.
8. Untuk demo deepfake ni, kita guna rakaman simulasi.
9. Kita test speech-to-text dengan ayat yang campur BM dan English.
10. Untuk text-to-speech, kita bagi contoh sebutan nama agensi sekali.
11. Aku guna Whisper untuk buat draf sari kata sebelum kita review.
12. Kalau audio sebut huruf satu-satu, transkrip tetap pakai ejaan rasmi.
13. Untuk bank suara ni, aku rakam setiap istilah dalam satu ayat penuh.
14. Bila dokumen dikeluarkan, sistem rekodkan hash dia pada blockchain.
15. Sistem sedia ada boleh panggil trust layer masa pegawai nak sahkan dokumen.
16. Dalam lejar teragih ni, setiap organisasi boleh semak rekod yang dikongsi.
17. Untuk rekod on-chain, kita simpan hash dan rujukan transaksi.
18. Dokumen penuh kekal off-chain dalam storan agensi.
19. Bila fail sampai, sistem kira hash dan bandingkan dengan rekod asal.
20. Untuk cari imej yang nampak serupa, kita boleh bandingkan perceptual hash.
21. Lepas dokumen diluluskan, kita anchor hash dia pada lejar.
22. Untuk demo ni, kita tengok node mana yang terima transaksi.
23. Pegawai boleh guna verification node untuk semak rekod yang dirujuk.
24. Bila kita pilih consensus, kita kena tengok jenis kegagalan yang dijangka.
25. Kalau leader terputus, Raft perlukan majoriti untuk pilih pengganti.
26. Dalam Hyperledger Fabric, kita tentukan organisasi mana boleh sertai rangkaian.
27. Smart contract ni semak status aset sebelum benarkan pindah milik.
28. Kalau rangkaian tu serasi EVM, kita boleh uji kontrak yang sama.
29. Kita cuba transaksi pertama dekat testnet dulu.
30. Masa demo nanti, buka wallet dan semak transaksi yang baru masuk.
31. Sebelum hantar transaksi, semak address penerima dengan rangkaian yang dipilih.
32. Dengan ZKP, pengguna boleh buktikan umur cukup tanpa tunjuk tarikh lahir.
33. Untuk demo Groth16, kita ukur masa jana bukti dan masa semak.
34. Kita guna SP1 untuk jana bukti yang verifier boleh semak.
35. Verifier kena semak tarikh rujukan yang digunakan dalam bukti umur tu.
36. Orang yang pegang dokumen boleh scan QR code untuk semak bukti.
37. Bila pegawai scan dokumen ni, dia boleh tengok jejak audit yang dibenarkan.
38. Melalui pasport bateri, pegawai boleh semak model dan rekod bateri tu.
39. Untuk fasa pertama, kita sambungkan modul baharu kepada sistem sedia ada.
40. Dekat frontend, pegawai nampak status permohonan dan tindakan seterusnya.
41. Backend akan semak peranan pengguna sebelum pulangkan rekod.
42. Sistem agensi panggil API ni untuk semak status permohonan.
43. Untuk API jenis REST, setiap permohonan ada URL sumber sendiri.
44. Endpoint ni pulangkan status semasa berdasarkan ID permohonan.
45. Setiap request kena bawa rujukan supaya kita boleh jejak balik.
46. Kalau rekod dijumpai, response tu akan sertakan status terkini.
47. Dalam payload ni, OEM cuma perlu isi medan yang ditetapkan.
48. Pihak integrasi boleh bagi satu sampel JSON untuk kita semak.
49. Kita semak schema dulu supaya format tarikh kedua-dua sistem sepadan.
50. Kalau nombor rujukan kosong, proses validasi akan pulangkan ralat.
51. Untuk uji interoperability, dua sistem kena tafsir kod status dengan cara sama.
52. Untuk integrasi pertama, kita pilih transaksi yang paling kerap digunakan.
53. Penjanaan laporan besar kita jalankan sebagai background task.
54. Kalau dokumen tak lengkap, workflow hantar balik kepada pemohon.
55. Tempoh sah tempahan tu pentadbir boleh ubah melalui parameter.
56. Kita salin konfigurasi yang diluluskan masa naik ke production.
57. Kalau proses tu perlukan customisation, kita anggar effort dia dulu.
58. Deployment untuk modul ni kita jadualkan lepas waktu operasi.
59. Kita kena pastikan runtime untuk aplikasi lama tu masih serasi.
60. Bila trafik naik, kita boleh tambah container untuk servis carian.

## Sesi 02 (fail `bank-02.m4a`)

61. Modul pentadbiran tu kita boleh bangunkan dengan Django.
62. Untuk portal pengguna, pasukan frontend guna Next.js.
63. Data aplikasi ni kita simpan dalam cloud ikut kawalan akses agensi.
64. Untuk reka bentuk cloud-native ni, setiap servis boleh diskalakan berasingan.
65. Komponen on-prem ni masih perlukan sambungan ke sistem agensi.
66. Untuk anggaran AWS, kita asingkan kos aplikasi dengan kos pangkalan data.
67. Kita letak jump box atas EC2 untuk akses pentadbiran.
68. ECS akan urus task yang jalankan servis portal ni.
69. Dengan Fargate, pasukan tetapkan CPU dan memori untuk setiap task.
70. Kalau projek perlukan Kubernetes, kita kena tetapkan siapa urus cluster.
71. Bila satu node keluar, kita semak kapasiti cluster yang tinggal.
72. ALB akan hantar trafik portal kepada task yang sihat.
73. Permintaan daripada OEM masuk melalui API Gateway sebelum diproses.
74. Lambda akan semak payload sebelum hantar data ke servis dalaman.
75. Untuk RDS, kita kira kos instance dan storan sekali.
76. Rekod transaksi utama kita simpan dalam PostgreSQL.
77. Kita pilih Multi-AZ untuk pangkalan data production.
78. Lampiran besar tu kita letak dalam S3 dan simpan rujukannya.
79. Fail statik portal tu kita edarkan melalui CloudFront.
80. Bila penggunaan memori naik, CloudWatch boleh hantar notifikasi.
81. Kita guna Route 53 untuk urus nama domain portal.
82. Pegawai sokongan boleh cari log transaksi melalui OpenSearch.
83. Dengan OpenTelemetry, kita boleh ikut satu request merentas beberapa servis.
84. Dalam SigNoz, kita boleh tengok servis mana yang paling lambat.
85. Untuk observability, kita kaitkan log dengan trace bagi transaksi yang sama.
86. Pasukan operasi guna monitoring untuk kesan ralat sebelum pengguna buat aduan.
87. Kita ukur latency dari portal sampai keputusan dipaparkan semula.
88. Ujian scalability ni tengok apa jadi bila jumlah pengguna serentak naik.
89. Kita ukur availability portal sepanjang waktu operasi yang dipersetujui.
90. Untuk reliability, kita semak berapa kerap transaksi gagal semasa operasi.
91. Kita semak capacity storan sebelum pindahkan fail sejarah.
92. Kalau CPU dah tinggi masa ujian, kita tengok proses mana yang berat.
93. Tambah RAM mungkin membantu kalau servis tu kerap kehabisan memori.
94. Dalam development, pasukan boleh cuba konfigurasi baharu dengan data contoh.
95. Kita sahkan integrasi dekat staging sebelum buka akses kepada pengguna.
96. Versi yang diluluskan tu kita naikkan ke production malam nanti.
97. Sebelum cutover, pasukan operasi akan ambil backup terakhir.
98. Kita cuba restore satu set data untuk sahkan sandaran tu boleh digunakan.
99. Ambil snapshot pangkalan data sebelum kita mula perubahan besar.
100. Masa latihan DR, kita rekod bila pengguna boleh akses portal semula.
101. Di DRC, pasukan semak aplikasi dan sambungan ke sistem luar.
102. Masa failover, kita ukur berapa lama sambungan aplikasi terputus.
103. Untuk uji recoverability, kita pulihkan servis dan semak transaksi terakhir.
104. Untuk keselamatan siber, setiap pasukan kena tahu siapa urus akses.
105. WAF tu kita letak pada laluan trafik web yang nak dilindungi.
106. Kita semak ACL supaya hanya rangkaian yang diluluskan boleh lalu.
107. Masa authentication, portal sahkan siapa pengguna yang cuba log masuk.
108. Lepas login, semakan authorisation tentukan siapa boleh luluskan permohonan.
109. Kita guna PKI untuk semak sijil yang berkait dengan tandatangan.
110. Operasi tandatangan boleh dibuat dalam HSM supaya kunci persendirian kekal terlindung.
111. Untuk integrasi GPKI, kita semak sijil dan aliran tandatangan yang diperlukan.
112. Verifier guna kunci awam untuk semak tandatangan digital tu.
113. Kunci persendirian untuk tandatangan tu perlu dilindungi sepanjang penggunaannya.
114. Kalau kandungan fail berubah, semakan tandatangan digital akan gagal.
115. Sistem kena semak tempoh sah sijil digital masa buat pengesahan.
116. Untuk token RS256, verifier pilih kunci awam yang sepadan.
117. Verifier ambil kunci awam daripada JWKS untuk semak tandatangan token.
118. Bila TTL kod tu habis, pengguna kena minta kod baharu.
119. Untuk demo ni, jangan masukkan PII sebenar dalam log.
120. Untuk perancangan PQC, kita kenal pasti dulu algoritma yang sistem guna.

## Sesi 03 (fail `bank-03.m4a`)

121. Aplikasi boleh ambil rahsia yang diperlukan melalui OpenBao.
122. Kita boleh guna reCAPTCHA pada borang yang terdedah kepada spam.
123. Dalam vulnerability management, setiap penemuan kena ada pemilik dan tarikh tindakan.
124. Untuk perlindungan data, kita hadkan medan yang dipaparkan kepada pengguna luar.
125. Bila permohonan diluluskan, status baharu disimpan dalam pangkalan data.
126. Laporan bulanan tarik data daripada data warehouse supaya transaksi harian tak terganggu.
127. Proses ETL akan padankan kod lama sebelum data masuk ke gudang.
128. Kita boleh jadualkan aliran FineDataLink untuk kemas kini jadual pelaporan.
129. Kita letak self-hosted integration runtime dalam rangkaian yang boleh capai sumber data.
130. Untuk migrasi data, kita kena kenal pasti jadual yang masih aktif.
131. Masa penukaran data, kod daerah lama kita padankan dengan kod baharu.
132. Masa cutover, pasukan akan rekod transaksi terakhir dari sistem lama.
133. Dengan incremental migration, kita boleh pindahkan perubahan selepas salinan awal siap.
134. Lepas migrasi, kita buat rekonsiliasi jumlah rekod dan nilai transaksi.
135. Masa deduplication, dua iklan dengan nombor tender sama kita semak dulu.
136. Crawler tu ambil senarai iklan untuk pasukan review pagi nanti.
137. Bila dokumen dikemas kini, indeks carian pun kena dikemas kini.
138. Dalam konfigurasi Fabric tu, CouchDB simpan keadaan semasa aset.
139. Fail CSV ni kita boleh buka dalam spreadsheet untuk semak sebutan.
140. Untuk ramalan jualan, kita tunjuk andaian sekali supaya orang boleh semak.
141. Kita kena test rangkaian dari pusat operasi sampai ke pelayan aplikasi.
142. Dalam VPC ni, kita asingkan subnet aplikasi dan pangkalan data.
143. Task aplikasi jalan dalam subnet yang ada laluan ke pangkalan data.
144. Pasukan operasi guna VPN untuk capai persekitaran yang dibenarkan.
145. Kita guna Site-to-Site VPN untuk sambungkan persekitaran awan dengan tapak DR.
146. Servis dalam subnet persendirian boleh keluar melalui NAT gateway.
147. Dalam rajah ni, internet gateway disambungkan kepada VPC.
148. Pentadbir masuk melalui jump box sebelum capai pelayan dalaman.
149. Kalau domain tak boleh dicapai, kita semak rekod DNS dulu.
150. Kita guna CDN untuk pendekkan masa muat turun fail statik.
151. Load balancer akan keluarkan sasaran yang gagal semakan kesihatan.
152. Kalau portal hidup tapi API tak sampai, kita semak routing.
153. Tempoh pindah fail bergantung pada bandwidth yang betul-betul tersedia.
154. Dalam seni bina berlapis ni, portal panggil servis melalui lapisan aplikasi.
155. Untuk skop projek rintis ni, kita fokus pada pengesahan dokumen.
156. Masa pilot run, pegawai tapak akan cuba proses dari mula sampai habis.
157. Untuk PoC ni, kita tunjuk satu dokumen boleh disahkan melalui imbasan.
158. Kes guna pertama tunjuk macam mana pegawai semak ketulenan laporan.
159. Masa sesi BPR, kita semak langkah kelulusan yang bertindih.
160. Untuk setiap NFR, kita tentukan ukuran dan cara nak uji.
161. Masa UAT, pegawai akan semak senario yang memang berlaku di kaunter.
162. Pasukan QA akan semak bukti ujian sebelum versi ni dilepaskan.
163. Untuk UX di kaunter, kita tengok berapa langkah pegawai perlu buat.
164. Dekat UI ni, butang pengesahan kena mudah dicari masa pegawai bertugas.
165. Kita uji bayaran end-to-end sampai resit keluar dalam portal.
166. Item dalam backlog ni kita susun ikut impak kepada pengguna.
167. Dalam roadmap ni, integrasi OEM masuk selepas modul pendaftaran siap.
168. Melalui gap analysis, kita nampak fungsi mana masih perlukan pembangunan.
169. Setiap stakeholder kena sahkan data yang dia akan bekalkan.
170. Masa handover, pasukan operasi akan cuba sendiri langkah pemulihan.
171. Kita buat rollout ikut lokasi supaya pasukan sokongan sempat pantau.
172. Untuk pengurusan perubahan, setiap pindaan workflow kena ada kelulusan.
173. Dalam tadbir urus projek, kita tetapkan siapa boleh luluskan perubahan skop.
174. Bukti pematuhan untuk item ni kita pautkan kepada keputusan ujian.
175. Untuk auditability, kita kena boleh tunjuk siapa ubah status dan bila.
176. Kawalan akses pastikan pegawai cuma nampak kes di bawah bidang tugas dia.
177. KPI ni kita ukur daripada bilangan transaksi yang berjaya disahkan.
178. Pada peringkat RFI, kita bagi gambaran penyelesaian dan andaian utama.
179. Untuk RFP ni, setiap keperluan kena dipadankan dengan jawapan teknikal.
180. Sebelum hantar sebut harga, kita semak skop dan tempoh sokongan.

## Sesi 04 (fail `bank-04.m4a`)

181. Dalam CRM, setiap peluang ada pemilik dan tarikh tindakan susulan.
182. Bila kita review pipeline, tengok peluang mana dah sampai peringkat tawaran.
183. Untuk recurring revenue, kita asingkan yuran tahunan daripada bayaran pelaksanaan.
184. Dalam jadual komersial, kita tunjuk komponen SST yang berkenaan.
185. OEM akan hantar maklumat bateri melalui API yang dipersetujui.
186. Untuk unjuran EV, kita asingkan angka pendaftaran sebenar daripada ramalan.
187. Untuk taklimat PDRM, kita tunjuk cara semak ketulenan salinan laporan.
188. Untuk senario JPN, kita tunjuk macam mana rekod boleh disahkan.
189. Untuk taklimat MOSTI, kita ringkaskan hasil projek dan impak kepada pengguna.
190. Untuk sesi bersama MIMOS, kita sediakan rajah seni bina dan demo.
191. Dalam demo ni, MBI tunjuk macam mana bukti dokumen boleh disemak.
192. Untuk MARii, kita petakan aliran data antara OEM dengan platform pasport bateri.
193. Untuk MAQIS, kita mulakan demo dengan tempahan ruang di pusat kuarantin.
194. Dalam MDP, pegawai boleh semak tempahan sebelum haiwan tiba di pusat kuarantin.
195. Untuk AKPS, kita petakan titik semakan yang berkait dengan proses pemeriksaan.
196. Untuk tapak pemulihan di PDSA, kita semak sambungan dan kapasiti yang tersedia.
197. Untuk sesi MCMC, kita guna data contoh bagi menerangkan pengesahan umur.
198. Pengguna boleh pilih MyDigital ID pada skrin log masuk portal.
199. Untuk notifikasi e-mel, kita cadangkan penghantaran melalui MyGovUC.
200. Pasukan semak iklan dalam ePerolehan sebelum masukkan peluang ke pipeline.
201. Untuk sesi TWG, kita bawa isu yang perlukan keputusan teknikal bersama.
202. Untuk peluang GLC, pasukan kena kenal pasti pemilik proses dan bajet.
203. Dalam laporan pipeline, kita asingkan peluang PLC ikut sektor industri.
204. Kalau pelanggan tu MNC, kita semak negara mana yang terlibat dalam integrasi.
205. Kalau slaid tulis Sdn Bhd, masa taklimat aku baca nama syarikat tu penuh.
206. Model machine learning ni kita train guna data yang dah dibersihkan, lepas tu kita deploy ke server dalam cloud.
207. Kalau database tu tak ada encryption, data sensitif boleh terdedah bila ada serangan cybersecurity.
208. Dashboard ni tunjuk status workflow secara real-time, dari request masuk sampai approval akhir.
209. Untuk compliance, setiap tindakan pegawai mesti ada audit trail yang tak boleh diubah.
210. Bila dokumen sampai, sistem kira hash dia, dan simpan hash tu dalam blockchain sebagai bukti.
211. API ni terima payload JSON, validate schema dia, dan pulangkan response dalam masa dua ratus milisaat.
212. Kita guna AI untuk classify dokumen, tapi keputusan akhir tetap pada pegawai yang authorised.
213. Server production kita ada backup setiap malam, dan failover ke DRC kalau zon utama down.
214. Encryption at rest dan encryption in transit dua-dua wajib untuk data PII.
215. Untuk cybersecurity, kita buat vulnerability scan setiap bulan dan patch dalam tujuh hari.
216. Pipeline ETL ni tarik data dari sistem lama, transform, dan load ke data warehouse.
217. Kalau latency naik, CloudWatch hantar alert, dan pasukan on-call semak log dalam dashboard.
218. Smart contract ni semak status aset dulu sebelum benarkan transaksi diteruskan.
219. Machine learning bukan magic; kalau data training bias, output model pun akan bias.
220. Workflow kelulusan ni ada tiga peringkat: penyedia, penyemak, dan pelulus.
221. Untuk audit trail, kita log siapa akses rekod, bila, dan dari IP mana.
222. Kita host LLM sendiri on-prem supaya data tak keluar dari rangkaian agensi.
223. Load balancer agihkan trafik ke tiga node, jadi kalau satu node gagal, servis tetap jalan.
224. Database PostgreSQL ni kita set Multi-AZ, dengan snapshot automatik setiap enam jam.
225. Sebelum go-live, kita buat UAT dengan pengguna sebenar, lepas tu baru rollout berperingkat.
226. Token akses ni ada TTL lima belas minit, lepas tu kena refresh guna JWKS yang sah.
227. Deepfake makin sukar dikesan, jadi kita perlukan provenance dan verification yang kukuh.
228. QR code pada sijil tu bawa pegawai terus ke halaman verification yang rasmi.
229. Kubernetes cluster kita autoscale bila CPU melebihi tujuh puluh peratus.
230. Dalam architecture ni, trust layer duduk di atas sistem sedia ada, bukan menggantikannya.
231. Kalau satu huruf dalam dokumen berubah, hash dia pun berubah, dan semakan akan gagal.
232. Kita simpan secret dalam OpenBao, bukan dalam source code atau fail konfigurasi.
233. Observability ni gabungan log, metrics dan tracing, contohnya guna OpenTelemetry dan SigNoz.
234. Untuk compliance dengan akta perlindungan data, kita minimumkan data yang dikumpul.
235. Speech-to-text ni kita test dengan ayat yang campur BM dan English, macam taklimat sebenar.
236. Ok, jadi ringkasnya: data kekal di agensi, cuma cryptographic proof yang dihantar ke blockchain.
237. So, soalan dia, macam mana kita nak pastikan rekod tu betul-betul original?
238. Betul ke? Hmm, kita semak dulu dalam dashboard sebelum buat keputusan.
239. Nombor ni penting: sembilan puluh sembilan perpuluhan sembilan peratus availability, dua puluh empat jam sehari.
240. Pada dua puluh satu Julai dua ribu dua puluh lima, sistem ni dilancarkan secara rasmi.

## Sesi 05 (fail `bank-05.m4a`)

241. Fasa satu, POC. Fasa dua, pilot run. Fasa tiga, rollout ke semua agensi.
