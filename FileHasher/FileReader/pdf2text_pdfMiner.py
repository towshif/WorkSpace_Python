# 
# Created by towshif ali (tali) on 7/21/2018
#

# Also check out recent changes and formats
# https://media.readthedocs.org/pdf/pdfminer-docs/latest/pdfminer-docs.pdf

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


with open("Output.md", "w") as text_file:
    text_file.write(convert(r"D:\Data\Weekly\LS-SWIFT_Product_Apps_Weekly_2018-07-13.pdf"))

# print convert(r"D:\Data\Weekly\LS-SWIFT_Product_Apps_Weekly_2018-07-13.pdf")
