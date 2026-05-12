from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class GeoPoliticalEvent(Base):
    __tablename__ = "geopolitical_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    outlet: Mapped[str] = mapped_column(String(255), nullable=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(500), unique=True, nullable=True)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)


class MapAlerts(Base):
    __tablename__ = "map_alerts"   
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    raw_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    location_name: Mapped[str] = mapped_column(String(255), nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    latitude: Mapped[float] = mapped_column(nullable=True)

    sentiment_score: Mapped[float] = mapped_column(default=0.0)
    severity_label: Mapped[str] = mapped_column(String(50), default="low")

    signals: Mapped[JSON] = mapped_column(JSON, nullable=True)



class FlightPosition(Base):
    __tablename__ = "flight_positions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flight_number: Mapped[str] = mapped_column(String(50), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    altitude: Mapped[float] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    heading: Mapped[float] = mapped_column(nullable=True)
    speed: Mapped[float] = mapped_column(nullable=True)      
