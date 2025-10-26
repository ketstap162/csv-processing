from sqlalchemy import Column, Integer, String, Float

from db.models.base import BaseModel


class Location(BaseModel):
    """
    Model representing location data from CSV file.
    
    Columns:
        id (int): Primary key
        region (str): Region/Oblast name (e.g., "Івано-Франківська", "Вінницька")
        district (str): District or City name (e.g., "Коломийський р-н", "м.Вінниця")
        value (float): Numerical value associated with the location
    """
    
    # Region name (область)
    region = Column(
        String(length=50),
        nullable=False,
        index=True,
        doc="Name of the region/oblast"
    )
    
    # District or city name (район/місто)
    district = Column(
        String(length=100),
        nullable=False,
        index=True,
        doc="Name of the district or city"
    )
    
    # Value from CSV
    value = Column(
        Float,
        nullable=False,
        doc="Numerical value associated with the location"
    )

    class Config:
        from_attributes = True
        
    def __str__(self) -> str:
        return f"{self.region}, {self.district}: {self.value}"
