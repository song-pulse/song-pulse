from sqlalchemy import Column, Integer, String, ForeignKey

from backend.app.database.base_class import Base


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlist.id"))
    name = Column(String)
    link = Column(String)
