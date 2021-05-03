from PIL import Image
from binascii import hexlify, unhexlify
import numpy as np
import pytest


class ImgMsg:
    """Class that hides a msg within the alpha values of an image.
        And converts a msg to an image and vice versa.
    """

    IMG_MAX_WIDTH = 1000  # must be even number
    EOF = "{0:0{1}x}".format(0xDE4DB33F, 2)

    def __init__(
        self,
        input_file=None,
        output_file=None,
        img_file=None,
        pil_img=None,
        hex_str=None,
        ascii_str=None,
    ):
        self.inputFile = input_file
        self.outputFile = output_file
        self.imgFile = img_file
        self.pilImg = pil_img
        self.hexStr = hex_str
        self.asciiStr = ascii_str
        pass

    def _getAlphaArrayFromPil(self):
        eof = self.EOF
        rgba = np.asarray(self.pilImg)
        alpha = np.dsplit(rgba, np.array([3]))[1]
        alpha = [i for i in alpha.flatten()]

        # now alpha is just a flat list of ints
        x = alpha
        eof_list = [int("0x" + eof[i : i + 2], 16) for i in range(0, len(eof), 2)]
        eof_index = [
            i for i in range(0, len(x)) if list(x[i : i + len(eof_list)]) == eof_list
        ][0]
        alpha = x[:eof_index]

        return alpha

    def loadInputFile(self, filename=None):
        """Load a file whose contents will be the hidden msg.

        Args:
            filename (string, optional): Defaults to None.
        """
        if not filename:
            filename = self.inputFile

        with open(filename, "rb") as f:
            self.msg = f.read()

    def loadImgFile(self, filename=None):
        """Load an image file whose contents already has the hidden msg.

        Args:
            filename (string, optional): Defaults to None.
        """
        if not filename:
            filename = self.imgFile

        self.pilImg = Image.open(filename)

    def loadAscii(self, ascii_str=None):
        """Load a ascii string as the hidden msg.

        Args:
            ascii_str (string, optional): Defaults to None.
        """
        if not ascii_str:
            ascii_str = self.asciiStr

        # self.msg = ascii_str.encode("ascii").hex()
        self.msg = bytes(ascii_str, "ascii")
        print(self.msg)

    def saveImgFile(self, filename=None):
        """Save the img built with hidden msg to file.add()

        Args:
            filename (string, optional): Output file path. Defaults to None.
        """
        if not filename:
            filename = self.imgFile

        self.pilImg.save(filename)
        pass

    def buildPilImg(self, hex_str=None):
        """Take a hex string and build an PIL img from it.

        Args:
            hex_str (string, optional): A hex string. Defaults to None.
        """
        if not hex_str:
            hex_str = self.hexStr

        hex_str += self.EOF

        # list of ints
        l = [
            int("0x" + hex_str[index : index + 2], 16)
            for index in range(0, len(hex_str), 2)
        ]

        n = self.IMG_MAX_WIDTH
        cols = int(np.ceil(len(l) / n))

        r = np.full((cols, n), 0, dtype=np.uint8)
        g = np.full((cols, n), 0, dtype=np.uint8)
        b = np.full((cols, n), 0, dtype=np.uint8)
        a = np.full((cols, n), 0, dtype=np.uint8)
        a.ravel()[: len(l)] = l

        rgba = np.dstack((r, g, b, a))
        self.pilImg = Image.fromarray(rgba)

    def buildMsg(self, pil_img=None):
        """Take pil_img and build hidden msg from its contents.

        Args:
            pil_img (PIL, optional): Defaults to None.
        """
        if not pil_img:
            pil_img = self.pilImg

        hex_ints = self._getAlphaArrayFromPil()

        msg = "".join(["{0:0{1}x}".format(i, 2) for i in hex_ints])
        msg = unhexlify(msg)

        self.msg = msg
        pass

    def buildHexStr(self, msg=None):
        """Build a hex string from msg.

        Args:
            msg (bytes, optional): Must be bytes. Defaults to None.
        """
        if not msg:
            msg = self.msg

        self.hexStr = hexlify(msg).decode("ASCII")

    def exportMsgToFile(self, filename):
        """Export msg hidden in image back to original form in file.

        Args:
            filename (string): File path.
        """
        if not filename:
            filename = self.outputFile

        with open(filename, "wb") as fd_out:
            fd_out.write(self.msg)

    def getMsg(self):
        return self.msg


###
# Use this factory functions
def imgMsgFromFile(input_file):
    imgmsg = ImgMsg(input_file=input_file)
    imgmsg.loadInputFile()
    imgmsg.buildHexStr()
    imgmsg.buildPilImg()
    imgmsg.buildMsg()

    return imgmsg


def imgMsgFromImage(img_file):
    imgmsg = ImgMsg(img_file=img_file)
    imgmsg.loadImgFile()
    imgmsg.buildMsg()

    return imgmsg


def imgMsgFromAscii(ascii_str):
    imgmsg = ImgMsg(ascii_str=ascii_str)
    imgmsg.loadAscii()
    imgmsg.buildHexStr()
    imgmsg.buildPilImg()

    return imgmsg
