from db import db
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class TimedLeaderboard(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    checksum: Mapped[str] = mapped_column(String, nullable=False)