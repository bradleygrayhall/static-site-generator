import sys

from copystatic import copy_static
from gencontent import generate_page, generate_pages_recursive
from textnode import TextNode, TextType


def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath += "/"
    
    copy_static("static","docs")
    generate_pages_recursive("content","template.html","docs",basepath)
main()