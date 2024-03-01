from pydantic import BaseModel


class ExtractSetting(BaseModel):
    """
    Model class for provider response.
    """
    filepath: str = None

    # valid values: Unstructured or others
    etlType: str = ''

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data) -> None:
        super().__init__(**data)
