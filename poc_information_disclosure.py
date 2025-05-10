import requests
import os
from colorama import init, Fore

init()

base_url = "https://target.com/"
payloads = "wordlists.txt"
file_extensions = ["txt", "html", "php", "aspx", "zip", "tar", "json", "js", "md", "tar.gz", "bak", "old", "swp", "tmp", "log", "logs", "xml", "conf", "config", "require", "requirement", "cfm", "asa", "asax", "pub", "ca", "keys", "key", "htm", "mysql", "sql", "sql.bak", "sql.gz", "sql.zip", "sql~", "mf", "ini", "page", "swf", "reg", "bz2", "db", "readme", "LOG", "dll", "1", "cgi", "pl", "perl", "error", "access", "backend.log", "wadl", "wci", "local", "pgsql", "MF", "passwd"]

def wordlists(lists):
    if os.path.exists(lists):
        with open(lists, "r") as file:
            return file.read().splitlines()

def brute_force_directory(base_url, wordlists, file_extensions):
    for dirname in wordlists:
        for format_file in file_extensions:

            url = os.path.join(base_url, dirname + "." + format_file)
            response = requests.get(url)
            
            if response.status_code == 200:
                print(Fore.WHITE + f"Found File: {url} " + Fore.GREEN + f"(status: {response.status_code})")
            elif response.status_code in [301, 302]:
                print(Fore.WHITE + f"Redirected : {url} " + Fore.YELLOW + f"(status: {response.status_code})")

file = wordlists(payloads)
brute_force_directory(base_url, file, file_extensions)
