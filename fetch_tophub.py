import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_tophub_news(url: str = "https://tophub.today/c/news", top_n: int = 10):
    """Fetch headlines from tophub.today and return a list of tuples (section_title, items)."""
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
    sections = []

    for container in soup.select("div.cc-cd"):
        name_div = container.select_one("div.cc-cd-lb")
        if not name_div:
            continue
        platform_name = name_div.get_text(strip=True)
        category_span = container.select_one("span.cc-cd-sb-st")
        category = category_span.get_text(strip=True) if category_span else ""
        section_title = f"{platform_name} {category}".strip()

        items = []
        for li in container.select("div.cc-cd-cb-ll")[:top_n]:
            rank_span = li.select_one("span.s")
            title_span = li.select_one("span.t")
            if not title_span:
                continue
            rank = rank_span.get_text(strip=True) if rank_span else ""
            title = title_span.get_text(strip=True)
            item_line = f"{rank}. {title}" if rank else title
            items.append(item_line)

        if items:
            sections.append((section_title, items))

    return sections


def save_summary(sections, path: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"今日热榜（综合）汇总 — 生成时间：{now}\n\n")
        for title, items in sections:
            f.write(f"# {title}\n")
            for line in items:
                f.write(f"- {line}\n")
            f.write("\n")


def main():
    sections = fetch_tophub_news()
    output_path = "tophub_summary.txt"
    save_summary(sections, output_path)
    print(f"保存成功，共 {len(sections)} 个板块，文件路径: {output_path}")


if __name__ == "__main__":
    main()