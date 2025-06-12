import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

BASE_URL = "https://tophub.today"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def get_category_codes():
    """Return a set of category codes (e.g. {'news', 'tech', ...})."""
    resp = requests.get(urljoin(BASE_URL, "/"), headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    codes = set()
    for a in soup.select("a[href^='/c/']"):
        href = a.get("href", "")
        # href pattern: /c/news, sometimes followed by query string
        if href.startswith("/c/"):
            code = href.split("/c/")[1].split("?")[0]
            if code and not code.startswith("#"):
                codes.add(code)
    return codes


def fetch_platforms_for_category(code: str):
    url = urljoin(BASE_URL, f"/c/{code}")
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    platforms = []
    for div in soup.select("div.cc-cd-lb"):
        name = div.get_text(strip=True)
        if name:
            platforms.append(name)
    return platforms


def main():
    category_codes = get_category_codes()
    all_platforms = {}
    for code in sorted(category_codes):
        platforms = fetch_platforms_for_category(code)
        for p in platforms:
            all_platforms.setdefault(p, set()).add(code)
    # Prepare log output
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = "tophub_platforms.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"TopHub 收录平台列表 — 生成时间 {now}\n\n")
        for platform in sorted(all_platforms.keys()):
            category_list = ", ".join(sorted(all_platforms[platform]))
            f.write(f"{platform}    [{category_list}]\n")
    print(f"已记录 {len(all_platforms)} 个平台到 {log_path}")


if __name__ == "__main__":
    main()