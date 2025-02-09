from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

Base = declarative_base()

class Token(Base):
    """
    SQLAlchemy model representing the tokens table in the World Token Tracker system.
    """
    __tablename__ = 'tokens'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(42), unique=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    decimals: Mapped[int] = mapped_column(Integer, nullable=False)
    total_supply: Mapped[Numeric] = mapped_column(Numeric, nullable=True)
    circulating_supply: Mapped[Numeric] = mapped_column(Numeric, nullable=True)
    holder_count: Mapped[int] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(String(10), nullable=True)
    icon_url: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_updated: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    website: Mapped[str] = mapped_column(String(512), nullable=True)
    is_native: Mapped[bool] = mapped_column(Boolean, default=False)
    app_id: Mapped[str] = mapped_column(String, nullable=True)
    humans: Mapped[int] = mapped_column(Integer, default=0)

    # Add this new line for the relationship
    extracted_data = relationship("TokenExtractedData", back_populates="token")

    def __repr__(self):
        return f"<Token(name='{self.name}', symbol='{self.symbol}', address='{self.address}')>"