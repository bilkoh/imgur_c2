import pytest
import builtins
import io
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../imgur_c2"))
)

from ImgMsg import ImgMsg, imgMsgFromFile, imgMsgFromImage, imgMsgFromAscii


###
# Tests
def test_make_img_from_file():
    input_file = "test_small_file.txt"
    img_file = "test_small_file.png"

    imgmsg = ImgMsg(input_file=input_file, img_file=img_file)
    imgmsg.loadInputFile()
    expected = imgmsg.msg
    imgmsg.buildHexStr()
    imgmsg.buildPilImg()

    imgmsg.saveImgFile()

    imgmsg.buildMsg()
    msg = imgmsg.getMsg()

    assert expected == msg


def test_make_msg_from_img():
    img_file = "test_small_file.png"
    expected_file = "test_small_file.txt"

    imgmsg = ImgMsg(img_file=img_file)
    imgmsg.loadImgFile()
    imgmsg.buildMsg()
    msg = imgmsg.getMsg()

    with open(expected_file, "rb") as f:
        expected = f.read()

    assert expected == msg


def test_file_to_pil():
    input_file = "test_small_file.txt"
    expected = b"Hello World\n"

    imgmsg = ImgMsg(input_file=input_file)
    imgmsg.loadInputFile()
    imgmsg.buildHexStr()
    imgmsg.buildPilImg()
    imgmsg.buildMsg()
    msg = imgmsg.getMsg()

    assert expected == msg


def test_large_file_to_pil():
    input_file = "meterpreter.exe"
    output_file = "meterpreter.exe.diff"
    img_file = "meterpreter.png"

    imgmsg = imgMsgFromFile(input_file)
    imgmsg.saveImgFile(img_file)

    # make new imgmsg object and load png and compare msg to expected
    imgmsg = imgMsgFromImage(img_file)
    msg = imgmsg.getMsg()

    with open(input_file, "rb") as f:
        expected = f.read()

    imgmsg.exportMsgToFile(output_file)
    assert expected == msg


def test_ascii():
    ascii_str = "Hello World"
    img_file = "test_ascii.png"

    imgmsg = imgMsgFromAscii(ascii_str)
    imgmsg.saveImgFile(img_file)

    # make new imgmsg object and load png and compare msg to expected
    imgmsg = imgMsgFromImage(img_file)
    msg = imgmsg.getMsg()

    assert ascii_str == msg.decode("ascii")


def test_load_img_from_imgur():
    img_file = "imgur_download.png"
    input_file = "meterpreter.exe"
    # double checking manually with `diff` cmd
    output_file = "meterpreter_from_imgur.exe.diff"

    imgmsg = imgMsgFromFile(input_file)
    expected = imgmsg.getMsg()
    imgmsg.exportMsgToFile(output_file)

    imgmsg = imgMsgFromImage(img_file)
    msg = imgmsg.getMsg()

    assert expected == msg


###
# Cleanup created files
def patch_open(open_func, files):
    def open_patched(
        path,
        mode="r",
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ):
        if "w" in mode and not os.path.isfile(path):
            files.append(path)
        return open_func(
            path,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        )

    return open_patched


@pytest.fixture(autouse=True)
def cleanup_files(monkeypatch):
    files = []
    monkeypatch.setattr(builtins, "open", patch_open(builtins.open, files))
    monkeypatch.setattr(io, "open", patch_open(io.open, files))
    yield
    for file in files:
        os.remove(file)
