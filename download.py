#!/usr/bin/python3
import json
import os
import requests
import wget
from lxml import html
import re

SEP = os.path.sep
TEMPLATE = "https://cdn-icons-png.flaticon.com/"
DIRNAME = os.path.dirname(__file__) + SEP
RESOLUTIONS = (
    "16", "24", "32", "64", "128", "256", "512"
)
CONFIG = json.load(open(DIRNAME + "config.json", "r"))
OUT = DIRNAME + CONFIG["out"] + SEP
resolution = CONFIG["resolution"]


def request(url):
    response = requests.get(url)
    return html.fromstring(response.text)


def get_image_url(url):
    img = url.split("_")[-1:][0]
    part = img[:len(img)-3]
    if url.find("/premium-icon/") != -1:
        page = request(url)
        print(img)
        return page.xpath("//div[@data-type='img']/img/@src")[0]
    else:
        print(TEMPLATE + f"{part}/{img}.png")
        return TEMPLATE + f"{resolution}/{part}/{img}.png"


def parse_url(url):
    res = {
        "url": "",
        "name": ""
    }
    if url.find("<~") != -1:
        res["name"] = url[url.find("<~")+2:url.find("~>")] + ".png"
        res["url"] = re.sub(r"\?.*|<~.*", "", url)
    else:
        res["name"] = os.path.basename(url.split("?")[0])
        res["url"] = url.split("?")[0]
    return res


def download(urls, dest=OUT):
    os.makedirs(dest, exist_ok=True)
    for url in urls:
        if url == "":
            continue
        url = parse_url(url)
        img_url = get_image_url(url["url"])
        output = dest + url["name"]
        wget.download(img_url, output)


def get_input_urls():
    default = DIRNAME + CONFIG["list"]
    print(
        f"\nEnter urls list path\ncurrent path: '{DIRNAME}'\ndefault path: '{default}'")
    selected = os.path.normpath(input("> "))
    print(selected)
    if selected == ".":
        return DIRNAME + CONFIG["list"]
    if not os.path.isabs(selected):
        selected = DIRNAME + selected
    if not os.path.exists(selected):
        return default
    return selected


def get_resolution():
    global resolution
    default = CONFIG["resolution"]
    print(f"Enter resolution\ndefault: {default}")
    for i in RESOLUTIONS:
        print(f"{RESOLUTIONS.index(i)}. {i}")
    res = input("> ")
    if not res.isdigit():
        return
    resolution = RESOLUTIONS[int(res)]


def main():
    get_resolution()
    urls = open(get_input_urls(), "r").read().split("\n")
    download(urls)


if __name__ == "__main__":
    main()
