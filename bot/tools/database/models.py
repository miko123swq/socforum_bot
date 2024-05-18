from sqlalchemy import String, BigInteger, Integer, Boolean, Text, DateTime, JSON, Float, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
  active: Mapped[int] = mapped_column(Integer, default=1)
  is_banned: Mapped[int] = mapped_column(Integer, default=0)
  user_coin: Mapped[int] = mapped_column(Integer, default=0)
  pay_status: Mapped[bool] = mapped_column(Boolean, default=False)


class Lawyer(Base):
  __tablename__ = 'lawyers'

  id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  telegram_id = mapped_column(BigInteger, nullable=False)
  telegram_name:Mapped[str] = mapped_column(String(255), nullable=False)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  surname: Mapped[str] = mapped_column(String(255), nullable=False)
  middle_name: Mapped[str] = mapped_column(String(255), nullable=False)
  number: Mapped[str] = mapped_column(String(255), nullable=False)
  email: Mapped[str] = mapped_column(String(255), nullable=False)
  description: Mapped[str] = mapped_column(Text)
  short_description: Mapped[str] = mapped_column(Text)
  diplomas: Mapped[str] = mapped_column(String(255), nullable=False)
  experience: Mapped[str] = mapped_column(String(255), nullable=False)
  legal_services_section: Mapped[str] = mapped_column(String(255), nullable=False)
  photo: Mapped[str] = mapped_column(String(255), nullable=False)
  earnings: Mapped[float] = mapped_column(Float, default=0.0)
  clients: Mapped[list] = mapped_column(JSON, default=[])
  active: Mapped[int] = mapped_column(Integer, default=1)
  is_banned: Mapped[int] = mapped_column(Integer, default=0)


  

