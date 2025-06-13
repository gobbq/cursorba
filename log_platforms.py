import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_platforms(url: str = "https://tophub.today"):
    """Return a sorted list of unique platform names present on the homepage."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    platforms = set()
    for div in soup.select("div.cc-cd-lb"):
        name = div.get_text(strip=True)
        if name:
            platforms.add(name)
    return sorted(platforms)


def save_platforms_log(platforms, path: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"平台列表 — 生成时间：{now}\n总计：{len(platforms)}个\n\n")
        for p in platforms:
            f.write(f"- {p}\n")


def main():
    platforms = fetch_platforms()
    path = "tophub_platforms.log"
    save_platforms_log(platforms, path)
    print(f"已记录 {len(platforms)} 个平台到 {path}")


if __name__ == "__main__":
    main()