from sqlalchemy import Column, Integer, String, Boolean, Float, text, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from app.backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # One-to-many relationship with Auction (one user can own many auctions)
    auctions = relationship("Auction", back_populates="owner")

    # One-to-many relationship with Bid (one user can make many bids)
    bids = relationship("Bids", back_populates="bidder")


class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    starting_price = Column(Float, nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    is_active = Column(Boolean, server_default="true", nullable=False)
    img = Column(String, nullable=False)
    # One-to-many relationship with Bid (one auction can have many bids)
    bids = relationship("Bids", back_populates="auction")

    # Many-to-one relationship with User (each auction has one owner)
    owner = relationship("User", back_populates="auctions", foreign_keys=[owner_id])

    # One-to-many relationship with Category (one auction can belong to many categories)
    categories = relationship("Categories", back_populates="auction")


class Bids(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Float, nullable=False)
    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Many-to-one relationship with Auction
    auction = relationship("Auction", back_populates="bids")

    # Many-to-one relationship with User
    bidder = relationship("User", back_populates="bids")


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False)

    # Many-to-one relationship with Auction
    auction = relationship("Auction", back_populates="categories")
