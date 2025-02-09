from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database.config import Base

class TokenExtractedData(Base):
    """
    SQLAlchemy model for storing token research results
    """
    __tablename__ = 'token_extracted_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(Integer, ForeignKey('tokens.id'), nullable=False)
    token_name = Column(String(100), nullable=False)
    research_results = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship with Token model
    token = relationship("Token", back_populates="extracted_data")

    def __repr__(self):
        return f"<TokenExtractedData(token_name='{self.token_name}', created_at='{self.created_at}')>"