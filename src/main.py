from copystatic import copy_static
from gencontent import generate_page, generate_pages_recursive
from textnode import TextNode, TextType


def main():
    copy_static("static","public")
    generate_pages_recursive("content","template.html","public")
main()