from curses import raw
from dotenv import load_dotenv
import dspy
import os
import requests
from conference import Conference
import argparse
from lxml import html
import re


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract conference info from CFP page"
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="The URL of the conference Call For Papers page",
    )
    return parser.parse_args()


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
    print("=" * 80)
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
    print("=" * 80)


def main():
    load_dotenv()
    args = parse_args()

    link = args.url
    cfp_html = extract_cfp_html(link)

    lm = dspy.LM("openai/gpt-5-mini", api_key=os.environ["OPENAI_API_KEY"])
    dspy.configure(lm=lm)

    module = dspy.Predict(Conference)
    response = module(html=cfp_html)
    print_yml(response, link)


if __name__ == "__main__":
    main()
