#!/usr/bin/python3
import argparse
import os
import random
import sys

import requests
import wget
from lxml import html

RESOLUTIONS = [16, 24, 32, 64, 128, 256, 512]
DOWNLOAD_URL = "https://cdn-icons-png.flaticon.com/{res}/{part}/{img}.png"
USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.88 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.88 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPod; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.88 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.5; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (X11; Linux i686; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/103.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 12_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/103.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPod touch; CPU iPhone OS 12_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/103.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/103.0",
    "Mozilla/5.0 (Android 12; Mobile; LG-M255; rv:103.0) Gecko/103.0 Firefox/103.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.5; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPod touch; CPU iPhone 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    # IE
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.2; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Edg/104.0.1293.54",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Edg/104.0.1293.54",
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36 EdgA/100.0.1185.50",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36 EdgA/100.0.1185.50",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36 EdgA/100.0.1185.50",
    "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36 EdgA/100.0.1185.50",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 EdgiOS/100.1185.50 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36 Edge/40.15254.603",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Edge/44.18363.8131",
    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 OPR/89.0.4447.83",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 OPR/89.0.4447.83",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 OPR/89.0.4447.83",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 OPR/89.0.4447.83",
    "Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36 OPR/63.3.3216.58675",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36 OPR/63.3.3216.58675",
    "Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36 OPR/63.3.3216.58675",
    # Vivaldi
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.68",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.68",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.68",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.68",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.68",
    # Yandex
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 YaBrowser/22.7.0 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 YaBrowser/22.7.0 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 YaBrowser/22.7.0 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 YaBrowser/22.7.6.660 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 YaBrowser/22.7.6.660 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (iPod touch; CPU iPhone 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 YaBrowser/22.7.6.660 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (Linux; arm_64; Android 12; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 YaBrowser/21.3.4.59 Mobile Safari/537.36",
]


# api


def download(image_url, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    wget.download(image_url, output_file, None)


def get_image_url(page_url, image_resolution):
    image_type = define_type(page_url)
    result = []
    if image_type == 0:
        page = requests.get(
            page_url,
            headers={
                "User-Agent": random.choice(USER_AGENTS)
            }
        )
        img = html.fromstring(page.text).xpath(
            ".//img[@class='img-small']/@src")
        img = img.rsplit("/", 3)
        if image_resolution == 0:
            for i in RESOLUTIONS:
                img[1] = str(i)
                result.append('/'.join(img))
        else:
            img[1] = str(image_resolution)
            result.append('/'.join(img))
    elif image_type == 1:
        img = page_url.rsplit("_", 1)[1]
        part = img[:len(img)-3]
        if image_resolution == 0:
            for i in RESOLUTIONS:
                result.append(
                    DOWNLOAD_URL.format(
                        res=i,
                        part=part,
                        img=img
                    )
                )
        else:
            result.append(
                DOWNLOAD_URL.format(
                    res=image_resolution,
                    part=part,
                    img=img
                )
            )
    elif image_type == 2:
        page = requests.get(
            page_url,
            headers={
                "User-Agent": random.choice(USER_AGENTS)
            }
        )
        imgs = html.fromstring(page.text).xpath(
            ".//a[contains(@class, 'view')]/img/@data-src")
        for url in imgs:
            url = url.rsplit("/", 3)
            url[1] = str(image_resolution)
            result.append('/'.join(url))
    elif image_type == 3:
        page = requests.get(
            page_url,
            headers={
                "User-Agent": random.choice(USER_AGENTS)
            }
        )
        imgs = html.fromstring(page.text).xpath(
            ".//li[contains(@class, 'icon--item')][@data-png]/@data-png")
        return []
        for url in imgs:
            url = url.rsplit("/", 3)
            url[1] = str(image_resolution)
            result.append('/'.join(url))
    return result


def define_type(page_url):
    if page_url.startswith("https://www.flaticon.com/search"):
        return 3
    elif page_url.startswith("https://www.flaticon.com/packs"):
        return 2
    elif page_url.startswith("https://www.flaticon.com/free-icon"):
        return 1
    elif page_url.startswith("https://www.flaticon.com/premium-icon"):
        return 0


# main


def logo():
    print(
        """\033[95m
 _____ _        _  _____ ___ ____ ___  _   _ ___
|  ___| |      / \|_   _|_ _/ ___/ _ \| \ | |__ \\
| |_  | |     / _ \ | |  | | |  | | | |  \| | / /
|  _| | |___ / ___ \| |  | | |__| |_| | |\  ||_|
|_|   |_____/_/   \_\_| |___\____\___/|_| \_|(_)

                          \033[92m* by Maksim4ikL1 *
        \033[0m"""
    )


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description="Image and pack downloader from flaticon.com"
    )
    parser.add_argument(
        "url", type=str, help="url to image or pack from flaticon.com"
    )
    parser.add_argument("-r", "--resolution", type=int,
                        default=512, choices=[0, 16, 24, 32, 64, 128, 256, 512])
    parser.add_argument("-o", "--output", type=str, default=os.getcwd())
    return parser.parse_args(args)


def main():
    logo()
    arguments = parse_arguments(sys.argv[1:])
    print(
        f"\033[92mGetting image(s) from \033[91m\"{arguments.url}\"\n\033[0m")
    images = get_image_url(arguments.url, arguments.resolution)
    print(f"\033[92mThe following image(s) will be donwloaded:\033[0m")
    print("\n".join(images))
    if input("\033[91mContinue? > \033[0m")[0].lower() != "y":
        print("\033[96m\n* * * STOP * * *\n\033[0m")
        sys.exit(0)
    print("\033[92m\n* * * DONWLOADING * * *\n\033[0m")
    for image in images:
        if arguments.resolution == 0:
            file_name = image.rsplit(
                "/", 1)[1].split(".")[0] + "-" + image.rsplit("/", 3)[1] + ".png"
            download(image, os.path.join(arguments.output, file_name))
        else:
            file_name = os.path.basename(image)
            download(image, os.path.join(arguments.output, file_name))
        print(f"(\033[92m\"{image}\"\033[0m) image №... downloaded")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt) as err:
        print("\033[96m\n* * * STOP * * *\n\033[0m")
    sys.exit(0)
