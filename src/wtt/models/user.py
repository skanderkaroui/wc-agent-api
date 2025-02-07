from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model representing users in the World Token Tracker system.
    This model stores both authentication information and gamification metrics.
    """
    __tablename__ = 'users'

    # Primary key and basic user identity information.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # World ID specific fields (optional, if you choose to store these)
    # For example, worldcoin_sub can store the unique identifier provided by World ID.
    worldcoin_sub: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)

    # Gamification and ranking metrics.
    # verification_score: A cumulative score reflecting the quality of the user's verifications.
    verification_score: Mapped[float] = mapped_column(Float, default=0.0)
    # total_verifications: The count of verifications contributed by the user.
    total_verifications: Mapped[int] = mapped_column(Integer, default=0)
    # accuracy_rate: The percentage of correct verifications (could be calculated as correct verifications / total_verifications).
    accuracy_rate: Mapped[float] = mapped_column(Float, default=0.0)

    # Rewards tracking: Total rewards (in WTT tokens or equivalent points) earned by the user.
    total_rewards: Mapped[float] = mapped_column(Float, default=0.0)

    # Timestamps for auditing and tracking user activity.
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<User(username='{self.username}', email='{self.email}', "
            f"verification_score={self.verification_score}, total_rewards={self.total_rewards})>"
        )
