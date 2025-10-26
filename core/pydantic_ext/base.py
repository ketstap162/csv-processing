from pydantic import BaseModel


class ConfiguredModel(BaseModel):
    class Config:
        from_attributes = True
