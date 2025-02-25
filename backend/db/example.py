from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Example(Base):
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)