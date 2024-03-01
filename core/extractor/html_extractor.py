"""Abstract interface for document loader implementations."""
from bs4 import BeautifulSoup

from core.extractor.extractor_base import BaseExtractor
from core.models.document import Document


class HtmlExtractor(BaseExtractor):

    """
    Load html files.


    Args:
        file_path: Path to the file to load.
    """

    def __init__(
        self,
        file_path: str
    ):
        """Initialize with file path."""
        self._file_path = file_path

    def extract(self) -> list[Document]:
        return [Document(content=self._load_as_text())]

    def _load_as_text(self) -> str:
        with open(self._file_path, "rb") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            text = soup.get_text()
            text = text.strip() if text else ''

        return text