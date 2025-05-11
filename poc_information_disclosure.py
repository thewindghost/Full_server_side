import requests
import os
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

base_url = "https://upload.koinbase.cyberjutsu-lab.tech/"
payloads = "wordlists.txt"
file_extensions = ["txt", "zip", "html", "php", "aspx", "tar", "tar.gz", "bak", "old"]
MAX_THREADS = 20

def load_wordlists(path):
    if os.path.exists(path):
        
        with open(path, "r") as f:
            return f.read().splitlines()
        
    else:
        print(Fore.RED + f"[!] File Not Found: {path}")
        return []

def check_url(base_url, dirname, ext):
    url = f"{base_url.rstrip('/')}/{dirname}.{ext}"
    try:

        resp = requests.get(url, timeout=5, allow_redirects=False, stream=True)
        status = resp.status_code
        resp.close()
        if status == 200:
            print(Fore.WHITE + f"Found File: {url} "
                  + Fore.GREEN + f"(status: 200)")
            
    except Exception:
        pass

def fuzzing_file(base_url, wordlists, file_extensions):
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        
        futures = [
            executor.submit(check_url, base_url, name, ext)
            for name in wordlists
            for ext in file_extensions
        ]
        
        for _ in as_completed(futures):
            pass

if __name__ == "__main__":
    
    wl = load_wordlists(payloads)
    
    if wl:
        fuzzing_file(base_url, wl, file_extensions)
        print(Fore.CYAN + "🟢 Scan complete!")
