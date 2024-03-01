from io import BytesIO

import pypdfium2 as pdfium


def convert_pdf_to_text(file_path):
    """
    Convert a PDF file into a single string of text.

    This function takes a path to a PDF file as input, reads the file, and returns the text
    content of the entire file as a single string.

    Args:
        file_path (str): The path to the PDF file to convert.

    Returns:
        str: The text content of the entire PDF file.
    """
    pdf_file = pdfium.PdfDocument(file_path)
    texts = []
    for page in pdf_file:
        texts.append(page.get_textpage().get_text_range())
    return "\n\n".join(texts)


def test_convert_pdf_to_text():
    text = convert_pdf_to_text(
        '/Users/mylxsw/Library/Mobile Documents/iCloud~QReader~MarginStudy/Documents/单核工作法图解：事多到事少，拖延变高效.pdf')
    print(text)


def convert_pdf_to_images(file_path, scale=300 / 72):
    """
    Convert a PDF file into a list of images.

    This function takes a path to a PDF file and a scale factor as input. It reads the PDF file,
    renders each page as an image, and returns a list of these images. Each image is represented
    as a dictionary where the key is the page index and the value is the image data in JPEG format.

    Args:
        file_path (str): The path to the PDF file to convert.
        scale (float): The scale factor to use when rendering the PDF pages as images.
                       The default value is 300/72, which corresponds to a DPI of 300.

    Returns:
        list: A list of dictionaries. Each dictionary represents an image and has a single key-value pair.
              The key is the page index (starting from 0), and the value is the image data in JPEG format.
    """
    pdf_file = pdfium.PdfDocument(file_path)
    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(pdfium.PdfBitmap.to_pil, page_indices=page_indices, scale=scale)
    final_images = []
    for i, image in zip(page_indices, renderer):
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        final_images.append(dict({i: image_byte_array}))

    return final_images


def test_convert_pdf_to_images():
    images = convert_pdf_to_images(
        '/Users/mylxsw/Library/Mobile Documents/iCloud~QReader~MarginStudy/Documents/单核工作法图解：事多到事少，拖延变高效.pdf')
    # 将 images 中的每一个图片保存到本地
    for i, image in enumerate(images):
        with open(f'./{i}.jpg', 'wb') as f:
            f.write(list(image.values())[0])
