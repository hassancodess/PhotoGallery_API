from database import *


async def handle_photo(photo: Photo):
    await INSERT_PHOTO(photo)
    # Gets ID OF Photo
    photoID = await GET_PHOTO_ID(photo.title)
    # print('photoID', photoID)
    return photoID


async def handle_person(person, photoID):
    # Check whether person already exists in DB
    count = await CHECK_PERSON(person)
    # Inserts if person NOT in DB
    if count == 0:
        await INSERT_PERSON(person)
    # Gets ID OF Person
    personID = await GET_PERSON_ID(person)
    # print('personID', personID)

    # Check whether PhotoPerson already exists in DB
    PhotoPerson_Count = await CHECK_PHOTOPERSON(photoID, personID)
    # Inserts if event NOT in DB
    if PhotoPerson_Count == 0:
        await INSERT_PHOTOPERSON(photoID, personID)


# Check whether person already exists in DB
async def handle_event(event, photoID):
    count = await CHECK_EVENT(event)
    # Inserts if event NOT in DB
    if count == 0:
        await INSERT_EVENT(event)

    # Gets ID OF Event
    eventID = await GET_EVENT_ID(event)
    # print('eventID', eventID)

    # Check whether PhotoPerson already exists in DB
    PhotoEvent_Count = await CHECK_PHOTOEVENT(photoID, eventID)
    # Inserts if event NOT in DB
    if PhotoEvent_Count == 0:
        await INSERT_PHOTOEVENT(photoID, eventID)


async def handle_remove_photo_data(item: SyncItem):
    photoID = await GET_PHOTO_ID(item.title)
    # Remove PhotoEvent
    await REMOVE_PHOTO_EVENT(photoID)
    # Remove PhotoPerson
    await REMOVE_PHOTO_PERSON(photoID)

    events = await GET_EVENTS_OF_PHOTO(photo_id=photoID)
    if events:
        for event in events:
            e_count = await CHECK_EVENT_COUNT(eventID=event[0])
            if e_count == 0:
                await REMOVE_EVENT(event_name=event[1])

    persons = await GET_PERSONS_IN_PHOTO(photo_id=photoID)
    if persons:
        for person in persons:
            p_count = await CHECK_PERSON_COUNT(personID=person[0])
            if p_count == 0:
                await REMOVE_PERSON(person_name=person[1])


async def handle_add_photo_data(item: SyncItem):
    photoID = await GET_PHOTO_ID(item.title)
    for e in item.events:
        eventID = await GET_EVENT_ID(e)
        if eventID is not None:
            await INSERT_PHOTOEVENT(photoID, eventID)
        else:
            await INSERT_EVENT(e)
            e_id = await GET_EVENT_ID(e)
            await INSERT_PHOTOEVENT(photoID, e_id)

    for p in item.people:
        personID = await GET_PERSON_ID(p)
        if personID is not None:
            await INSERT_PHOTOPERSON(photoID, personID)
        else:
            await INSERT_EVENT(p)
            p_id = await GET_PERSON_ID(p)
            await INSERT_PHOTOPERSON(photoID, p_id)


async def update_photo_data(photo: SyncItem):
    photoID = await GET_PHOTO_ID(photo.title)
    # Update Label
    await UPDATE_PHOTO_LABEL(photo.label, photoID)
    # Update Last Modified Date
    # Convert string to datetime object
    # Parse the input date into a datetime object
    datetime_obj = datetime.strptime(
        photo.last_modified_date, "%Y:%m:%d %H:%M:%S")
    # datetime_obj = datetime.strptime(
    #     photo.last_modified_date, "%m/%d/%Y, %I:%M:%S %p")
    # Format the datetime object as "YYYY-MM-DD HH:MM:SS"
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    await UPDATE_LAST_MODIFIED_DATE(photoID, formatted_datetime)
    # Update Lat Lng
    await UPDATE_PHOTO_LOCATION(photo.lat, photo.lng, photoID)


async def handle_isSynced_status():
    await UPDATE_PHOTOS_ISSYNCED()
