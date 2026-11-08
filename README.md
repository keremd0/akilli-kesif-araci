# Akıllı Keşif ve Bilgi Toplama Aracı 🔍

Sızma testlerinde keşif (reconnaissance) ve numaralandırma (enumeration) aşamasını otomatikleştiren bir Python
aracı. Hedefteki açık portları tespit eder, bulunan servislere göre uygun tarama araçlarını (WhatWeb, Gobuster,
anonim FTP kontrolü) otomatik olarak çalıştırır ve tüm bulguları tek bir raporda toplar.

Aracın "akıllı" tarafı, her hedefe aynı taramaları körlemesine uygulamak yerine **önce neyin açık olduğuna
bakıp, servise özel adımları seçmesidir.**

## 📌 Özellikler

- **Port ve servis tespiti:** Nmap ile hızlı port taraması (en yaygın 100 port) ve servis sürümü tespiti.
- **Web servisleri:** Nmap'in web servisi olarak tanıdığı her portta (`http`, `https`, `http-proxy`, `ssl/http`
  vb.) ve 80, 443, 8080 portlarında otomatik WhatWeb teknoloji tespiti ve Gobuster dizin taraması.
- **HTTPS desteği:** SSL üzerinden çalışan servisler otomatik olarak `https://` ile taranır; CTF makinelerinde
  sık görülen kendinden imzalı sertifikalar sorun çıkarmaz.
- **FTP:** FTP servisi bulunan portlarda (ve 21 numaralı portta) otomatik anonim giriş testi.
- **Raporlama:** Tüm bulgular düzenli tek bir raporda toplanır.

## 🔄 Nasıl çalışır?

```
Hedef IP
   │
   ▼
Nmap port ve servis taraması
   │
   ├─ Web servisi (http/https) ──► WhatWeb + Gobuster
   ├─ FTP servisi ───────────────► Anonim FTP giriş testi
   │
   ▼
Tüm bulgular ──► rapor
```

## 📋 Gereksinimler

- Kali Linux veya başka bir Linux dağıtımı
- Python 3
- `nmap`, `whatweb`, `gobuster`
- Gobuster için kelime listesi: `/usr/share/wordlists/dirb/common.txt` (Kali'de varsayılan olarak gelir)

## 🚀 Kurulum

```bash
git clone https://github.com/keremd0/akilli-kesif-araci.git
cd akilli-kesif-araci
sudo apt install -y nmap whatweb gobuster
```

## 💻 Kullanım

```bash
python3 kesif.py <HEDEF_IP>
```

Örnek:

```bash
python3 kesif.py 10.10.10.5
```

Rapor, komutu çalıştırdığın klasöre `<HEDEF_IP>_recon.txt` adıyla kaydedilir (ör. `10.10.10.5_recon.txt`).
Rapor, Nmap çıktısını ve servis bazlı detaylı bulguları ayrı bölümlerde içerir.

## 📸 Örnek çıktı

```
$ python3 kesif.py 10.10.10.5
[+] Hedef: 10.10.10.5 için dinamik tarama başladı
[*] Nmap ile portlar ve servisler taranıyor...
[+] 3 adet açık port bulundu.
 -> Port 21: ftp
 -> Port 22: ssh
 -> Port 80: http
[*] FTP tespit edildi. Anonim giriş kontrol ediliyor...
[*] Web servisi tespit edildi (http://10.10.10.5). WhatWeb ve dizin taraması başlatılıyor...
[+] Tum islemler bitti. Sonuclar -> 10.10.10.5_recon.txt
```

## ⚠️ Sınırlamalar

- Nmap hızlı modda (`-F`) çalıştığı için yalnızca en yaygın 100 port taranır; daha az bilinen portlardaki
  servisler gözden kaçabilir.
- WhatWeb ve Gobuster, taramanın cevap vermeyen bir sunucuda takılı kalmaması için 60 saniyelik zaman aşımıyla
  sınırlandırılmıştır. Büyük sitelerde dizin taraması bu sürede tamamlanmayabilir.
- Şu an yalnızca HTTP ve FTP servisleri için özel adımlar var.

## 🗺️ Yol haritası

- [ ] Tam port taraması seçeneği (`-p-`)
- [ ] SMB, SSH ve SMTP için numaralandırma adımları
- [ ] HTML veya Markdown formatında rapor
- [ ] Birden fazla hedefi (IP aralığı veya liste) tarama

## ⚖️ Sorumlu kullanım

Bu araç, hedef sistemlere **aktif tarama** yapar. Yalnızca sahibi olduğun veya test etmek için yazılı
izin aldığın sistemlerde (ör. TryHackMe, HackTheBox makineleri veya kendi laboratuvarın) kullan.
İzinsiz tarama birçok ülkede yasa dışıdır.
