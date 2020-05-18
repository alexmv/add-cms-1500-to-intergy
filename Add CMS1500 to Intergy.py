import codecs
import copy
import shutil
import sys
from tempfile import NamedTemporaryFile

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject
from PyPDF2.pdf import ContentStream
from PyPDF2.utils import PdfReadError

SELF_PRODUCER = "Intergy with CMS-1500"


def main(files):
    try:
        cms1500 = PdfFileReader(open("CMS-1500.pdf", "rb"))
        template_page = cms1500.getPage(0)
    except OSError as e:
        print(f"Can't load the CMS-1500 background image: {e}")
        sys.exit(1)

    for filename in files:
        update(filename, template_page)


def update(filename, template_page):
    if not filename.lower().endswith(".pdf"):
        print(f"Not a pdf file: {filename}")
        return

    try:
        data = PdfFileReader(open(filename, "rb"))
    except OSError as e:
        print(f"Can't open {filename}: {e}")
        return
    except PdfReadError as e:
        print(f"{filename} is not a valid PDF file: {e}")
        return

    info = data.getDocumentInfo()
    producer = None
    creator = None
    title = None
    if info:
        producer = info.get("/Producer", None)
        creator = info.get("/Creator", None)
        title = info.get("/Title", None)

    # Check if we've already filled this
    if producer == "PyPDF2" or producer == SELF_PRODUCER:
        print(f"Skipping {filename}: Already added CMS-1500")
        return

    if data.getNumPages() < 1:
        print(f"Skipping {filename}: No pages")

    output = PdfFileWriter()
    output.addMetadata(
        {"/Producer": codecs.BOM_UTF16_BE + SELF_PRODUCER.encode("utf-16be")}
    )

    for page_no in range(data.getNumPages()):
        data_page = data.getPage(page_no)

        # If it's printed through the eBridge printer driver, it has an
        # image of the output with invisible text on top; look for those
        # and strip off the image
        if producer == "eBridgeToolkit 7.1":
            # Set a fixed-width font
            font = data_page[NameObject("/Resources")][NameObject("/Font")]
            if not NameObject("/T1_0") in font:
                print(
                    f"Skipping {filename}: it does not match the expected format (font name)"
                )
                return
            font[NameObject("/T1_0")][NameObject("/BaseFont")] = NameObject("/Courier")

            # Remove the image that covers everything
            content = ContentStream(data_page["/Contents"].getObject(), data)
            ops = [op[1] for op in content.operations[0:5]]
            if ops != [b"q", b"cm", b"Do", b"Q", b"rg"]:
                print(
                    f"Skipping {filename}: it does not match the expected format (obscuring image)"
                )
                return
            del content.operations[0:5]

            # Remove the flag that makes the text hidden
            if content.operations[2] != ([3], b"Tr"):
                print(
                    f"Skipping {filename}: it does not match the expected format (font invisible)"
                )
                return
            del content.operations[2]

            # Write that back
            data_page[NameObject("/Contents")] = content
        elif creator == "Intergy" and title == "CMSPrePrinted1500212":
            # Nothing to do; these overlay just fine
            pass
        else:
            print(f"Skipping {filename}: Unknown PDF")
            return

        merged_page = copy.copy(template_page)
        merged_page.mergePage(data_page)
        output.addPage(merged_page)

    # Write the output to a temporary file, so that any failures in
    # writing don't affect the original
    output_file = NamedTemporaryFile()
    output.write(output_file)
    output_file.flush()
    shutil.copy(output_file.name, filename)

    print(f"Successfully processed {filename}")


if __name__ == "__main__":
    main(sys.argv[1:])
