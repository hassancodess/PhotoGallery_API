from models import *
from typing import List
from pydantic import Required
import pyodbc


constr = "DRIVER={SQL Server}; SERVER=DESKTOP-LMK4CI3\\SQLEXPRESS; DATABASE=PhotoGallery; UID=sa; PWD=123"
conn = pyodbc.connect(constr)
cursor = conn.cursor()


async def getAllPersonNames():
    query = "SELECT name FROM Person"
    cursor.execute(query)
    data = cursor.fetchall()
    names = []
    for i in data:
        # print(i[0]) # This will give Person Name
        names.append(i[0])
    return names


async def getPersonIDByName(name: str):
    query = f"SELECT id FROM Person WHERE name = '{name}'"
    cursor.execute(query)
    data = cursor.fetchall()
    for i in data:
        # print(i[0])  # This will give Person ID
        return i[0]


async def getAllAlbumTitles():
    query = "SELECT title FROM Album"
    cursor.execute(query)
    data = cursor.fetchall()
    names = []
    for i in data:
        # print(i[0]) # This will give Album Name
        names.append(i[0])
    return names


async def getAlbumIDByTitle(title: str):
    query = f"SELECT id FROM Album WHERE title = '{title}'"
    cursor.execute(query)
    data = cursor.fetchall()
    for i in data:
        # print(i[0])  # This will give Album ID
        return i[0]


async def getPhotoIDByTitle(title: str):
    query = f"SELECT id FROM Photo WHERE title = '{title}'"
    cursor.execute(query)
    data = cursor.fetchall()
    for i in data:
        # print(i[0])  # This will give Person ID
        return i[0]


async def getRecentPhotoID():
    query = "SELECT TOP 1 id FROM Photo ORDER BY id DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    for i in data:
        return i[0]


async def getRecentPersonIDs(count: int):
    query = f"SELECT TOP {count} id FROM Person ORDER BY id DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    ids = []
    for i in data:
        ids.append(i[0])
    print(ids)
    return ids
# getRecentPersonIDs(2)


async def getRecentAlbumIDs(count: int):
    query = f"SELECT TOP {count} id FROM Album ORDER BY id DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    ids = []
    for i in data:
        ids.append(i[0])
    print(ids)
    return ids
