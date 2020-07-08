from sqlalchemy import Column, String

from app.database.base_class import Base


class Spotify(Base):
    __tablename__ = "spotify"

    id = Column(String, primary_key=True, index=True)
    refresh_token = Column(String)
