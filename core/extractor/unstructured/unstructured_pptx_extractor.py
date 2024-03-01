import logging

from core.extractor.extractor_base import BaseExtractor
from core.models.document import Document

logger = logging.getLogger(__name__)


class UnstructuredPPTXExtractor(BaseExtractor):
    """Load msg files.


    Args:
        file_path: Path to the file to load.
    """

    def __init__(
            self,
            file_path: str,
            api_url: str
    ):
        """Initialize with file path."""
        self._file_path = file_path
        self._api_url = api_url

    def extract(self) -> list[Document]:
        from unstructured.partition.pptx import partition_pptx

        elements = partition_pptx(filename=self._file_path, api_url=self._api_url)
        text_by_page = {}
        for element in elements:
            page = element.meta.page_number
            text = element.text
            if page in text_by_page:
                text_by_page[page] += "\n" + text
            else:
                text_by_page[page] = text

        combined_texts = list(text_by_page.values())
        documents = []
        for combined_text in combined_texts:
            text = combined_text.strip()
            documents.append(Document(content=text))

        return documents
