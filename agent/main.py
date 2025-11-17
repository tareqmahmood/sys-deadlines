from dotenv import load_dotenv
import dspy
import os
import requests
from conference import Conference
import argparse


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
    return response.text


def print_yml(response: dspy.Prediction, link: str):
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


def main():
    load_dotenv()
    args = parse_args()

    lm = dspy.LM("openai/gpt-5-mini", api_key=os.environ["OPENAI_API_KEY"])
    dspy.configure(lm=lm)

    link = args.url
    cfp_html = extract_cfp_html(link)

    module = dspy.Predict(Conference)
    response = module(html=cfp_html)
    print_yml(response, link)


if __name__ == "__main__":
    main()
