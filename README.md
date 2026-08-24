# Akıllı Keşif ve Bilgi Toplama Aracı

Sızma testlerinde keşif ve numaralandırma aşamasını otomatize eden python aracı. Hedefteki açık portları tespit eder özel tarama araçlarını (WhatWeb, Gobuster, FTP Anonim Giriş) otomatik çalıştırır.

## Özellikler
- Nmap ile hızlı port ve servis tespiti.
- 80/443/8080 portlarında otomatik WhatWeb ve Gobuster dizin taraması.
- 21 portunda otomatik anonim FTP giriş testi.
- Tüm bulguların düzenli tek bir raporda toplanması.

## Gereksinimler
- Kali Linux / Linux
- Python 3
- `nmap`, `whatweb`, `gobuster`

## Kullanım
```bash
python3 kesif.py <HEDEF_IP>
