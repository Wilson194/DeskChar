# -*- coding: utf-8 -*-

import sys
import random
from loremipsum import generate_paragraphs
from jinja2 import Environment, PackageLoader
from PyQt5.QtWidgets import QApplication
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Jinja2 template environment
env = Environment(loader=PackageLoader("testing", "templates"))


def render_template(template_file, **kwargs):
    template = env.get_template(template_file)
    return template.render(**kwargs)


def print_pdf(html, destination):
    app = QApplication(sys.argv)

    web = QWebEngineView()
    web.setHtml(html)

    printer = QPrinter()
    printer.setPageSize(QPrinter.A4)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(destination)
    web.print_(printer)

    app.exit()


def main():
    # Random 2D list
    table = [[random.randint(0, 100) for j in range(10)] for i in range(10)]

    # Some Lorem Ipsum text
    paragraphs = [p[2] for p in generate_paragraphs(3)]

    html = render_template(
        "report.html",
        table=table,
        paragraphs=paragraphs
    )

    print_pdf(html, "file.html")


if __name__ == "__main__":
    main()