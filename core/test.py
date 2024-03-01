from core.extractor.extract_processor import ExtractProcessor

pdf_file_path = '/Users/mylxsw/Library/Mobile Documents/iCloud~QReader~MarginStudy/Documents/单核工作法图解：事多到事少，拖延变高效.pdf'


def test_read_pdf():
    documents = ExtractProcessor().load_from_file(pdf_file_path)

    # 遍历所有的文档，打印出文档的内容，每个文档之间使用 ------ 文档名称 ----- 分割
    for document in documents:
        print(f"------ {document.meta} -----")
        print(document.content)


def test_read_url():
    documents = ExtractProcessor().load_from_url('https://boto3.amazonaws.com/v1/documentation/api/latest/index.html')

    # 遍历所有的文档，打印出文档的内容，每个文档之间使用 ------ 文档名称 ----- 分割
    for document in documents:
        print(f"------ {document.meta} -----")
        print(document.content)

