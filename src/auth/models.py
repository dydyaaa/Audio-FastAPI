from sqlalchemy import Column, Integer, String, Boolean
from src.models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    yandex_id = Column(String, unique=True, index=True)
    email = Column(String(120), unique=True, nullable=False)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"