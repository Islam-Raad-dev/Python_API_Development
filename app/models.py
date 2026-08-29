from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, column  # noqa: F401
from sqlalchemy.orm import relationship  # noqa: F401
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = column(Integer, primary_key= True, nullable=False)
    title = column(String, nullable=False)
    content = column(String, nullable=False)
    published = column(Boolean, default=True)
    created_at = column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )