import json, sys, urllib.error, urllib.request
from urllib.parse import quote

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def main(path):
    lines = [l.strip() for l in open(path) if l.strip()]
    no_pkg = no_ver = 0
    oldest = None

    for line in lines:
        name, version = [p.strip() for p in line.split("==")]

        if fetch(f"https://pypi.org/pypi/{quote(name)}/json") is None:
            no_pkg += 1
            continue

        rel = fetch(f"https://pypi.org/pypi/{quote(name)}/{quote(version)}/json")
        if rel is None:
            no_ver += 1
            continue

        t = rel["urls"][0]["upload_time"]
        if oldest is None or t < oldest[0]:
            oldest = (t, f"{name}=={version}")

    print(f"1. Dependencies checked: {len(lines)}")
    print(f"2. Packages not on PyPI: {no_pkg}")
    print(f"3. Versions not on PyPI: {no_ver}")
    print(f"4. Oldest pinned release: {oldest[1]} ({oldest[0][:4]})")

main(sys.argv[1] if len(sys.argv) > 1 else "requirements.txt")