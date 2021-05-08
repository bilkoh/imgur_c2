"""
██╗███╗   ███╗ ██████╗ ██╗   ██╗██████╗ 
██║████╗ ████║██╔════╝ ██║   ██║██╔══██╗
██║██╔████╔██║██║  ███╗██║   ██║██████╔╝
██║██║╚██╔╝██║██║   ██║██║   ██║██╔══██╗
██║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║  ██║
╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
            ██████╗██████╗                         
            ██╔════╝╚════██╗                        
            ██║      █████╔╝                        
            ██║     ██╔═══╝                         
            ╚██████╗███████╗                        
            ╚═════╝╚══════╝                        

   
Example (in your terminal):
    $ python3 argparse-template.py "hello" 123 --enable
Copyright (c) 2020, Alexander Hogen
"""

from imgur_c2.tng import generate_tag_name
import argparse
import sys
from datetime import datetime

TODAYS_TAG = generate_tag_name(datetime.utcnow())


def make_parser():
    add_tng_to_banner = "\nTag Name Generation is #" + TODAYS_TAG + "\n"

    # Make parser object
    p = argparse.ArgumentParser(
        description=__doc__ + add_tng_to_banner,
        prog="cli.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    group = p.add_mutually_exclusive_group(required=True)

    p.add_argument(
        "-t",
        "--tng",
        action="store_true",
        help="""Show tag name generated based on UTC time. This tag is what the \
                attacker will use when uploading the image. And what the victim wil\
                l use to find the image.""",
    )
    group.add_argument(
        "-b",
        "--binary",
        help="Path to binary that will be converted into stegano'd image.",
    )
    group.add_argument(
        "-i",
        "--image",
        help="Path to stegno'd image that will be converted back to binary.",
    )
    p.add_argument(
        "-o",
        "--output",
        help="""Path to output. For when generating an image from binary (-b) or\
                binary from image (-i).""",
    )

    # return p.parse_args()
    return p


def main():

    print(TODAYS_TAG)

    try:
        p = make_parser()
        args = p.parse_args()
        print(args)
    except:
        p.print_help(sys.stderr)


if __name__ == "__main__":
    main()
