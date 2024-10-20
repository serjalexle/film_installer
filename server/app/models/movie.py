from datetime import datetime

from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

from bson import ObjectId


class MovieDetails(BaseModel):
    year: Optional[str] = None
    age_rating: Optional[str] = None
    country: Optional[str] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    actors: Optional[str] = None
    duration: Optional[str] = None
    language: Optional[str] = None
    imdb_rating: Optional[str] = None
    description: Optional[str] = None
    trailer: Optional[str] = None
    full_video: Optional[str] = None


class Movie(Document):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str
    image_url: str
    link: str
    rating: Optional[str]
    quality: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[MovieDetails] = None

    class Settings:
        name = "movies"
        indexes = ["title", "created_at", "updated_at"]


class MovieDTO(BaseModel):
    title: str
    image_url: str
    link: str
    rating: Optional[str]
    quality: Optional[str]
    details: Optional[MovieDetails] = None
    created_at: datetime
    updated_at: datetime