import subprocess
import sys
import re

if len(sys.argv) < 2:
    print(f"Kullanım: python3 {sys.argv[0]} <hedef_ip>")
    sys.exit(1)

target = sys.argv[1]
report_file = f"{target}_recon.txt"

print(f"[+] Hedef: {target} için dinamik tarama başladı\n")

# 1. Hızlı port taraması
print("[*] Nmap ile portlar ve servisler taranıyor...")
nmap_cmd = ["nmap", "-sV", "-T4", "-F", target]
nmap_res = subprocess.run(nmap_cmd, capture_output=True, text=True)
nmap_out = nmap_res.stdout

# Acik portlari ve servisleri yakalama (ornek: 80/tcp open http)
open_services = re.findall(r"(\d+)/tcp\s+open\s+([\w\-\?]+)", nmap_out)

print(f"[+] {len(open_services)} adet açık port bulundu.")
for port, srv in open_services:
    print(f"    -> Port {port}: {srv}")

extra_findings = ""

# 2. Servise gore otomatik aksiyon alma
for port, srv in open_services:
    # Web servisi yakalanirsa
    if srv in ["http", "https", "http-proxy"] or port in ["80", "443", "8080"]:
        proto = "https" if port == "443" else "http"
        url = f"{proto}://{target}:{port}"
        
        print(f"\n[*] Web servisi tespit edildi ({url}). WhatWeb ve dizin taraması başlatılıyor...")
        
        # Whatweb
        ww_res = subprocess.run(["whatweb", url], capture_output=True, text=True)
        extra_findings += f"\n--- WHATWEB ({url}) ---\n" + ww_res.stdout
        
        # Hizli gobuster (kali'deki default wordlist ile)
        wl = "/usr/share/wordlists/dirb/common.txt"
        gb_cmd = ["gobuster", "dir", "-u", url, "-w", wl, "-q", "-t", "25", "--no-error"]
        try:
            gb_res = subprocess.run(gb_cmd, capture_output=True, text=True, timeout=60)
            extra_findings += f"\n--- GOBUSTER ({url}) ---\n" + (gb_res.stdout if gb_res.stdout else "Dizin bulunamadı.\n")
        except subprocess.TimeoutExpired:
            extra_findings += f"\n--- GOBUSTER ({url}) ---\nZaman aşımı (60s).\n"

    # FTP servisi yakalanirsa anonymous kontrolu
    elif "ftp" in srv or port == "21":
        print("\n[*] FTP tespit edildi. Anonim giriş kontrol ediliyor...")
        ftp_check = subprocess.run(["nmap", "--script=ftp-anon", "-p", port, target], capture_output=True, text=True)
        extra_findings += f"\n--- FTP ANON KONTROL (Port {port}) ---\n" + ftp_check.stdout

# 3. Raporu kaydet
with open(report_file, "w") as f:
    f.write(f"=== RECON REPORT: {target} ===\n\n")
    f.write("[+] NMAP CIKTISI:\n")
    f.write(nmap_out + "\n")
    if extra_findings:
        f.write("\n[+] DETAYLI ANALIZ VE KESIFLER:\n")
        f.write(extra_findings)

print(f"\n[+] Tum islemler bitti. Sonuclar -> {report_file}")
