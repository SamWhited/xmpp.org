#!/usr/bin/env python3

"""In order to have newsletter e-mails formatted properly,
we need to add inline style attributes to some elements.
This tool takes a post URL for input, processes its HTML,
and stores it afterwards ready for copy and paste."""

from http import HTTPStatus

import requests
from bs4 import BeautifulSoup


def process(input_url: str) -> None:
    """Processes page content for sending via e-mail."""

    print("Processing...")
    with requests.get(input_url, timeout=5) as response:
        if response.status_code != HTTPStatus.OK:
            print("Could not fetch URL:", input_url)
            return
        soup = BeautifulSoup(response.text, "html.parser")

    article = soup.find("article", {"role": "main"})
    if article is None:
        print("Could not find post's article element.")
        return

    # Remove social share box, since it uses FontAwesome icons
    # (not available in emails)
    social_share = article.find("section", {"id": "social-share"})
    if social_share is not None:
        social_share.decompose()

    # Add body padding
    article["style"] = "padding: 2em;"

    # Change color and text decoration of heading
    header_box = article.find("div", {"class": "header-internal"})
    link = header_box.find("a")
    link["style"] = "text-decoration: none; color: #333;"

    # Change post meta color
    meta_span = article.find("span", {"class": "post-meta"})
    meta_span["style"] = "color: gray;"

    # Improve rendering of figures
    figures = article.find_all("figure")
    for figure in figures:
        img = figure.find("img")
        img["style"] = "max-width: 100%;"

    with open("newsletter-mail.html", "w", encoding="utf-8") as html_file:
        html_file.write(str(article))
    print(
        "All done! Please copy and paste contents from 'newsletter-mail.html' "
        "into your e-mail client of choice (use 'Insert HTML')."
    )


if __name__ == "__main__":
    print(50 * "=")
    print(
        "This tool processes newsletter posts for emails.\n"
        "It takes a post URL, processes its content, "
        "and saves HTML ready for copy and paste."
    )
    print(50 * "=")
    url = input("Please paste the URL you want to process: ")
    process(url)
