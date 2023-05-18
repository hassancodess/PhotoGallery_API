from pydantic import BaseModel
from typing import Dict, List, Optional
import datetime
from fastapi import UploadFile


class Album(BaseModel):
    id: int
    title: str


class Person(BaseModel):
    id: int
    name: str


class Photo(BaseModel):
    id: Optional[int]
    title: str
    event: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    path: Optional[str]
    date_taken: datetime.datetime
    last_modified_date: datetime.datetime


class PhotoList(BaseModel):
    data: List[Photo]
    names: List[str]
    path: List[str]


# class PhotoFileList(BaseModel):
#     files: List[UploadFile]
#     data: List[Photo]

class AlbumPhoto(BaseModel):
    aid: int
    pid: int


class PhotoPerson(BaseModel):
    pid: int
    personid: int
