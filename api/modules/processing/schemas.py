from core.pydantic_ext.base import ConfiguredModel


class UploadCSVResponse(ConfiguredModel):
    """
    Schema for uploading CSV file request.
    
    Attributes:
        file_path (str): Path to the CSV file to be uploaded.
    """
    message: str
    inserted_count: int
