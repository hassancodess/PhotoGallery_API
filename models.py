from pydantic import BaseModel
from typing import Dict, List, Optional, Union
import datetime
from fastapi import UploadFile
from datetime import datetime


class Album(BaseModel):
    id: int
    title: str


class Person(BaseModel):
    id: int
    name: str


class Photo(BaseModel):
    id: Optional[int]
    title: str
    lat: Optional[float]
    lng: Optional[float]
    path: str
    date_taken: datetime
    last_modified_date: datetime
    label: str
    isSynced: int

# class Photo(BaseModel):
#     id: Optional[int]
#     title: str
#     event: Optional[str]
#     lat: Optional[float]
#     lng: Optional[float]
#     path: Optional[str]
#     date_taken: datetime.datetime
#     last_modified_date: datetime.datetime


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


class SyncItem(BaseModel):
    title: str
    people: List[str]
    events: List[str]
    label: str
    lat: Optional[float]
    lng: Optional[float]
    date_taken: str
    last_modified_date: str
    isSynced: int
