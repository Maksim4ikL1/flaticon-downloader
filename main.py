import argparse
import sys

import api


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description="Image and pack downloader from flaticon.com"
    )
    parser.add_argument(
        "url", type=str, help="url to image or pack from flaticon.com"
    )
    parser.add_argument("-r", "--resolution", type=int, default=512)
    parser.add_argument("-o", "--output", type=str, default=".")
    return parser.parse_args(args)


def main():
    arguments = parse_arguments(sys.argv[1:])
    images = api.get_image_url(arguments.url, arguments.resolution)
    for image in images:
        api.download(image, arguments.output)


if __name__ == "__main__":
    main()
