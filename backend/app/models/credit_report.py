"""
Credit Report model
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class CreditReport(Base):
    """Credit report model for generated credit reports"""
    __tablename__ = "credit_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=False, index=True)
    credit_score = Column(Integer, nullable=False, index=True)  # 300-850 range
    score_factors = Column(JSON, nullable=True)  # JSON object with scoring factors
    report_data = Column(JSON, nullable=False)  # Full report data as JSON
    version = Column(Integer, default=1, nullable=False)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # User who requested
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # Report expiration
    pdf_path = Column(String(512), nullable=True)  # Path to generated PDF
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    consumer = relationship("Consumer", back_populates="credit_reports")
    
    def __repr__(self):
        return f"<CreditReport(id={self.id}, consumer_id={self.consumer_id}, score={self.credit_score})>"

