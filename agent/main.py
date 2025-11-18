from curses import raw
import sys
from dotenv import load_dotenv
import dspy
import os
import requests
import argparse
from lxml import html
import re
import json

from conference import Conference
from search import Search


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract conference info from CFP page"
    )
    parser.add_argument(
        "-c",
        "--conference",
        choices=[
            "NeurIPS",
            "ICML",
            "ICLR",
            "MLSys",
            "OSDI",
            "NSDI",
            "ASPLOS",
            "SOSP",
            "SIGCOMM",
            "FAST",
        ],
        type=str,
        help="Conference name, e.g. NeurIPS, ICML",
        required=True,
    )
    parser.add_argument(
        "-y", "--year", type=int, help="Conference year, e.g. 2023, 2024", required=True
    )
    return parser.parse_args()


def setup_dspy():
    lm = dspy.LM("openai/gpt-5-mini", api_key=os.environ["OPENAI_API_KEY"])
    dspy.configure(lm=lm)


def extract_cfp_html(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content
    tree = html.fromstring(response.text)

    # remove script & style nodes
    for bad in tree.xpath("//script | //style"):
        bad.getparent().remove(bad)

    # Extract text content from the HTML
    text = tree.text_content()

    # Convert multiple blank lines to one
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Collapse internal spacing
    text = re.sub(r"[ \t]+", " ", text).strip()

    # remove leading/trailing spaces on each line
    text = "\n".join(line.strip() for line in text.splitlines())

    return text


def print_yml(response: dspy.Prediction, link: str):
    print("=" * 20, "📅 Conference Info", "=" * 20)
    print(f"- title: {response.title}")
    print(f"  year: {response.year}")
    print(f"  id: {response.id}")
    print(f"  link: {link}")
    print(f"  deadline: {response.paper_deadline}")
    print(f"  abstract_deadline: {response.abstract_deadline}")
    print(f"  timezone: {response.timezone}")
    print(f"  place: {response.place}")
    print(f"  date: {response.date}")
    print(f"  start: {response.start}")
    print(f"  end: {response.end}")
    print(f"  sub: {response.sub}")
    print("=" * 60)


def search_cfp(conference: str, year: int, k: int = 5) -> str:
    print("Searching for CFP link of ", conference, year)

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": f"{conference} {year} call for papers"})
    headers = {
        "X-API-KEY": os.environ["SERPER_API_KEY"],
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()

    top_results = []
    for res in results["organic"]:
        position = res["position"]
        if position <= k:
            top_results.append(
                f"{position}: {res['title']}: {res['link']} ({res['snippet']})"
            )
    top_results = "\n".join(top_results)

    print("*" * 20, "🔍 Google Search", "*" * 20)
    print(top_results)
    print("*" * 60)

    return top_results


def extract_cfp_link(conference: str, year: int, top_results: str) -> str | None:
    link_extractor = dspy.Predict(Search)
    response = link_extractor(
        conference=conference,
        year=year,
        search_result=top_results,
    )
    if response.has_cfp:
        print("✅ Found CFP link:", response.cfp_link)
        return response.cfp_link
    else:
        print("❌ No CFP link found. Exiting.")
        sys.exit(1)


def extract_conf_info(cfp_html: str):
    cfp_extractor = dspy.Predict(Conference)
    response = cfp_extractor(html=cfp_html)
    return response


def main():
    load_dotenv()
    setup_dspy()
    args = parse_args()

    top_results = search_cfp(args.conference, args.year)
    link = extract_cfp_link(args.conference, args.year, top_results)

    cfp_html = extract_cfp_html(link)
    conf_info = extract_conf_info(cfp_html)
    print_yml(conf_info, link)


if __name__ == "__main__":
    main()
