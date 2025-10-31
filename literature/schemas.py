"""
Pydantic Schemas for Gemini API responses
"""
from pydantic import BaseModel


class AuthorInfo(BaseModel):
    """Schema for author information extraction"""
    name: str
    year_of_birth: str
    year_of_death: str
    information: str


class Motif(BaseModel):
    """Schema for literary motif"""
    motif_name: str
    info: str


class Theme(BaseModel):
    """Schema for literary theme"""
    theme_name: str
    info: str


class Character(BaseModel):
    """Schema for literary character"""
    name: str
    info: str


class WorkInfo(BaseModel):
    """Schema for literary work information extraction"""
    name: str
    year: str
    genre: str
    motifs: list[Motif]
    themes: list[Theme]
    characters: list[Character]
    analysis_summary: str
