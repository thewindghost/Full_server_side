import requests
import os
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

base_url = "https://targets.com/"
payloads = "wordlists.txt"
file_extensions = ["txt", "zip", "html", "php", "aspx", "tar", "tar.gz", "bak", "old"]
MAX_THREADS = 20

def wordlists(lists):
    if os.path.exists(lists):
        with open(lists, "r") as file:
            return file.read().splitlines()
    else:
        print(Fore.RED + f"[!] File Not Found: {lists}")
        return []

def check_url(base_url, dirname, format_file):
    url = base_url.rstrip("/") + "/" + dirname + "." + format_file

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(Fore.WHITE + f"Found File: {url} " + Fore.GREEN + f"(status: {code})")
            
    except requests.RequestException:
        pass

def fuzzing_file(base_url, wordlists, file_extensions):
    tasks = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for dirname in wordlists:
            for format_file in file_extensions:
                tasks.append(executor.submit(check_url, base_url, dirname, format_file))

        for _ in as_completed(tasks):
            pass

file = wordlists(payloads)
if file:
    fuzzing_file(base_url, file, file_extensions)
