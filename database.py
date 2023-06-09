from models import *
from typing import List
from pydantic import Required
import pyodbc


constr = "DRIVER={SQL Server}; SERVER=DESKTOP-LMK4CI3\\SQLEXPRESS; DATABASE=PhotoGallery; UID=sa; PWD=123"
conn = pyodbc.connect(constr)
cursor = conn.cursor()


async def FETCH_PHOTOS():
    query = "SELECT * FROM Photo"
    cursor.execute(query)
    data = cursor.fetchall()
    photos = []
    for i in data:
        photos.append(i)
    return photos


async def FETCH_PHOTO_BY_NAME(name):
    query = f"SELECT * FROM Photo WHERE title = '{name}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if row is not None:
        return row
    return None


async def FETCH_UNSYNCED_PHOTOS():
    query = "SELECT * FROM Photo WHERE isSynced = 0"
    cursor.execute(query)
    data = cursor.fetchall()
    photos = []
    for i in data:
        photos.append(i)
    return photos


async def FETCH_PERSONS_IN_PHOTO(photo_id):
    query = f"SELECT * FROM Person INNER JOIN PhotoPerson ON Person.id = PhotoPerson.person_id WHERE photo_id = {photo_id}"
    cursor.execute(query)
    data = cursor.fetchall()
    people = []
    for i in data:
        people.append(i)
    return people


async def FETCH_EVENTS_IN_PHOTO(event_id):
    query = f"SELECT * FROM Event INNER JOIN PhotoEvent ON Event.id = PhotoEvent.event_id WHERE event_id = {event_id}"
    cursor.execute(query)
    data = cursor.fetchall()
    events = []
    for i in data:
        events.append(i)
    return events


async def CHECK_PERSON(person_name):
    # Check if the name already exists in the table
    query = "SELECT COUNT(*) FROM Person WHERE name = ?"
    cursor.execute(query, person_name)
    row = cursor.fetchone()
    # print('row', type(row), row)
    if row is not None:
        count = row[0]
        return count
    return None


async def CHECK_EVENT(event_name):
    # Check if the name already exists in the table
    query = "SELECT COUNT(*) FROM Event WHERE name = ?"
    cursor.execute(query, event_name)
    row = cursor.fetchone()
    # print('row', type(row), row)
    if row is not None:
        count = row[0]
        return count
    return None


async def CHECK_PHOTO(photo_title):
    query = "SELECT COUNT(*) FROM Photo WHERE title = ?"
    cursor.execute(query, photo_title)
    row = cursor.fetchone()
    if row is not None:
        count = row[0]
        return count
    return None


async def CHECK_PHOTOEVENT(photoID, eventID):
    # Check if the name already exists in the table
    query = "SELECT COUNT(*) FROM PhotoEvent WHERE photo_id = ? AND event_id = ?"
    cursor.execute(query, photoID, eventID)
    row = cursor.fetchone()
    # print('row', type(row), row)
    if row is not None:
        count = row[0]
        return count
    return None


async def CHECK_PHOTOPERSON(photoID, personID):
    # Check if the name already exists in the table
    query = "SELECT COUNT(*) FROM PhotoPerson WHERE photo_id = ? AND person_id = ?"
    cursor.execute(query, photoID, personID)
    row = cursor.fetchone()
    # print('row', type(row), row)
    if row is not None:
        count = row[0]
        return count
    return None


async def INSERT_PHOTO(p: Photo):
    try:
        # Construct the SQL INSERT statement
        query = "INSERT INTO Photo(title,lat, lng, path, date_taken, last_modified_date, label, isSynced) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, p.title, p.lat, p.lng, p.path,
                       p.date_taken, p.last_modified_date, p.label, p.isSynced)
        # Commit the transaction
        conn.commit()
        # id = cursor.fetchval()
        print("Photo inserted successfully.")
    except pyodbc.Error as e:
        print("Error INSERT_PHOTO:", e)


async def INSERT_PERSON(person_name):
    try:
        # Construct the SQL INSERT statement
        query = "INSERT INTO Person(name) VALUES (?)"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, person_name)
        # Commit the transaction
        conn.commit()
        # id = cursor.fetchval()
        print("Person inserted successfully.")
    except pyodbc.Error as e:
        print("Error INSERT_PERSON:", e)


async def INSERT_EVENT(event_name):
    try:
        # Construct the SQL INSERT statement
        query = "INSERT INTO Event(name) VALUES (?)"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, event_name)
        # Commit the transaction
        conn.commit()
        # id = cursor.fetchval()
        print("Event inserted successfully.")
    except pyodbc.Error as e:
        print("Error INSERT_PERSON:", e)


async def INSERT_PHOTOPERSON(photoID, personID):
    try:
        # Construct the SQL INSERT statement
        query = "INSERT INTO PhotoPerson(photo_id, person_id) VALUES (?, ?)"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, photoID, personID)
        # Commit the transaction
        conn.commit()
        # id = cursor.fetchval()
        print("PhotoPerson inserted successfully.")
    except pyodbc.Error as e:
        print("Error INSERT_PHOTOPERSON:", e)


async def INSERT_PHOTOEVENT(photoID, eventID):
    try:
        # Construct the SQL INSERT statement
        query = "INSERT INTO PhotoEvent(photo_id, event_id) VALUES (?, ?)"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, photoID, eventID)
        # Commit the transaction
        conn.commit()
        # id = cursor.fetchval()
        print("PhotoEvent inserted successfully.")
    except pyodbc.Error as e:
        print("Error INSERT_PHOTOEVENT:", e)


async def GET_PHOTO_ID(photo_title):
    try:
        # Construct the SQL INSERT statement
        query = "SELECT id FROM Photo WHERE title = ?"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, photo_title)
        # Commit the transaction
        row = cursor.fetchone()
        if row is not None:
            return row[0]
    except pyodbc.Error as e:
        print("Error GET_PHOTO_ID:", e)


async def GET_PERSON_ID(person_name):
    try:
        # Construct the SQL INSERT statement
        query = "SELECT id FROM Person WHERE name = ?"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, person_name)
        # Commit the transaction
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return None
    except pyodbc.Error as e:
        print("Error INSERT_PERSON:", e)


async def GET_EVENT_ID(event_name):
    try:
        # Construct the SQL INSERT statement
        query = "SELECT id FROM Event WHERE name = ?"
        # Execute the INSERT statement with the provided values
        cursor.execute(query, event_name)
        # Commit the transaction
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return None
    except pyodbc.Error as e:
        print("Error GET_EVENT_ID:", e)


async def getAllPersonNames():
    query = "SELECT * FROM Person"
    cursor.execute(query)
    data = cursor.fetchall()
    names = []
    for i in data:
        print(i)  # This will give Person Name
        names.append(i)
    return names


async def getAllPersonsOfPhoto(photo_id):
    query = f"SELECT * FROM Person INNER JOIN PhotoPerson ON Person.id = PhotoPerson.person_id WHERE photo_id = {photo_id}"
    cursor.execute(query)
    data = cursor.fetchall()
    people = []
    for i in data:
        print(i)  # This will give Person Name
        people.append(i)
    return people


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


async def CHECK_EVENT_COUNT(eventID):
    try:
        # Check if the name already exists in the table
        query = "SELECT COUNT(*) FROM PhotoEvent WHERE event_id = ?"
        cursor.execute(query, eventID)
        row = cursor.fetchone()
        # print('row', type(row), row)
        if row is not None:
            count = row[0]
            return count
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def CHECK_PERSON_COUNT(personID):
    try:
        # Check if the name already exists in the table
        query = "SELECT COUNT(*) FROM PhotoPerson WHERE person_id = ?"
        cursor.execute(query, personID)
        row = cursor.fetchone()
        # print('row', type(row), row)
        if row is not None:
            count = row[0]
            return count
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def REMOVE_EVENT(event_name):
    try:
        query = f"DELETE FROM Event where name = {event_name}"
        cursor.execute(query)
        conn.commit()
        return f"Event Deleted - {event_name}"
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def REMOVE_PERSON(person_name):
    try:
        query = f"DELETE FROM Person where name = {person_name}"
        cursor.execute(query)
        conn.commit()
        return f"Person Deleted - {person_name}"
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def REMOVE_PHOTO_EVENT(id):
    try:
        query = f"DELETE FROM PhotoEvent where photo_id = {id}"
        cursor.execute(query)
        conn.commit()
        return f"PhotoEvent Deleted for photo-id-{id}"
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def REMOVE_PHOTO_PERSON(id):
    try:
        query = f"DELETE FROM PhotoPerson where photo_id = {id}"
        cursor.execute(query)
        conn.commit()
        return f"PhotoPerson Deleted for photo-id-{id}"
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def UPDATE_PHOTO_LABEL(label, photo_id):
    try:
        query = f"UPDATE Photo SET label = '{label}' WHERE id = {photo_id}"
        cursor.execute(query)
        conn.commit()
        print(f"Photo label updated for photo-id-{photo_id}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def UPDATE_PHOTO_LOCATION(lat, lng,  photo_id):
    try:
        query = f"UPDATE Photo SET lat = {lat}, lng = {lng} WHERE id = {photo_id}"
        cursor.execute(query)
        conn.commit()
        print(f"Photo location updated for photo-id-{photo_id}")
    except Exception as e:
        print(f"UPDATE_PHOTO_LOCATION: {str(e)}")


async def UPDATE_LAST_MODIFIED_DATE(photo_id, last_modified_date):
    try:
        query = f"UPDATE Photo SET last_modified_date = ? WHERE id = {photo_id}"
        cursor.execute(query, last_modified_date)
        conn.commit()
        print(f"last modified date updated for photo-id-{photo_id}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def UPDATE_PHOTOS_ISSYNCED():
    try:
        query = f"UPDATE Photo SET isSynced = 1 WHERE isSynced = 0"
        cursor.execute(query)
        conn.commit()
        print(f"isSynced updated for 0 status")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def GET_EVENTS_OF_PHOTO(photo_id):
    try:
        query = f"SELECT Event.* FROM PhotoEvent INNER JOIN Event ON PhotoEvent.event_id = Event.id WHERE PhotoEvent.photo_id = {photo_id}"
        cursor.execute(query)
        data = cursor.fetchall()
        names = []
        for i in data:
            names.append(i)
        return names
    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def GET_PERSONS_IN_PHOTO(photo_id):
    try:
        query = f"SELECT Person.* FROM PhotoPerson INNER JOIN Person ON PhotoPerson.person_id = Person.id WHERE PhotoPerson.photo_id = {photo_id}"
        cursor.execute(query)
        data = cursor.fetchall()
        names = []
        for i in data:
            names.append(i)
        return names
    except Exception as e:
        print(f"An error occurred: {str(e)}")
