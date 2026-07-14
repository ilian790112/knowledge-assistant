from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    """
    Metadata about an uploaded document.
    """

    filename: str
    content_type: str
    path: str
    status: str