from sqlalchemy import Column, Integer, String, ForeignKey
from src.models import Base


class AudioFile(Base):
    __tablename__ = "audio_file"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<AudioFile(id={self.id}, name={self.name}, user_id={self.user_id})>"