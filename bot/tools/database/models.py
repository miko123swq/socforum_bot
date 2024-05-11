from sqlalchemy import String, BigInteger, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  created:Mapped[DateTime] = mapped_column(DateTime, default=func.now())
  updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())



class User(Base):
  __tablename__ = 'users'

  id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  telegram_id = mapped_column(BigInteger, nullable=False)
  telegram_name:Mapped[str] = mapped_column(String(255), nullable=False)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  surname: Mapped[str] = mapped_column(String(255), nullable=False)
  middle_name: Mapped[str] = mapped_column(String(255), nullable=False)
  number: Mapped[str] = mapped_column(String(255), nullable=False)
  email: Mapped[str] = mapped_column(String(255), nullable=False)
  active: Mapped[int] = mapped_column(default=1)
  is_banned: Mapped[int] = mapped_column(default=0)