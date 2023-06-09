import os
import shutil
from fastapi import FastAPI, UploadFile, File, Query, Path, Form, Depends, Body
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from helpers import *
from models import *
from typing import List
from pydantic import Required
import pyodbc
from face_recog import *
from database import *
import glob
import os
import shutil
from datetime import datetime

app = FastAPI()

app.mount("/images", StaticFiles(directory="./Images"), name="images")
app.mount("/faces", StaticFiles(directory="./ImagesCropped"),
          name="cropped_images")


# DB
constr = "DRIVER={SQL Server}; SERVER=DESKTOP-LMK4CI3\\SQLEXPRESS; DATABASE=PhotoGallery; UID=sa; PWD=123"
conn = pyodbc.connect(constr)
cursor = conn.cursor()

# Utilities
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Utitlity Function


def Allowed_File(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get('/')
def index():
    return "Hello"


@app.post('/saveImage')
async def saveImage(file: UploadFile):
    filePath = f"Images/{file.filename}"

    if Allowed_File(file.filename):  # type: ignore
        fp = open(filePath, 'w')
        fp.close()
        with open(filePath, 'wb+') as buffer:
            shutil.copyfileobj(file.file, buffer)
    # send this picture to image recog function to get names
    names_locations = await face_recog_function(filePath)
    return names_locations


@app.post('/syncNow')
async def syncNow(items: List[SyncItem]):
    print('started')
    # Source folder path
    source_folder = "Images\\"
    # Destination folder path
    destination_folder = Path.home() / "Desktop" / "Pictures"
    # destination_folder = "C:\\Users\\Hassan\\Desktop\\Pictures"

    # Creates Pictures Folder if not exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print("Directory created successfully.")
    else:
        print("Directory already exists.")

    # Loop through the list of objects
    for obj in items:
        image_name = obj.title
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(destination_folder, image_name)

        # Check if the image file exists in the source folder
        # print('source path', source_path, 'destination path', destination_path)
        if os.path.exists(source_path):
            # Check if the image file already exists in the destination folder
            if not os.path.exists(destination_path):
                # Copy the file to the destination folder
                shutil.copyfile(source_path, destination_path)
                print('File copied successfully')
            else:
                print('File already exists in destination folder')
        else:
            print(
                f"Image '{image_name}' not found in the source folder. Skipping...")

        # WRITING IN DB
        # WRITE PHOTO
        count = await CHECK_PHOTO(obj.title)
        # PHOTO NOT PRESENT IN SQL
        if count == 0:
            # Date Taken & Last Modified Date
            # date_format = "%m/%d/%Y, %I:%M:%S %p"
            # last_modified_datetime = datetime.strptime(
            #     obj.last_modified_date, date_format)
            # date_taken = datetime.strptime(obj.date_taken, date_format)

            # Define the format of the input date
            input_format = "%Y:%m:%d %H:%M:%S"
            # Parse the input date into a datetime object
            date_taken = datetime.strptime(obj.date_taken, input_format)
            last_modified_datetime = datetime.strptime(
                obj.last_modified_date, input_format)

            p = Photo(
                id=None,
                title=obj.title,
                lat=obj.lat,
                lng=obj.lng,
                date_taken=date_taken,
                last_modified_date=last_modified_datetime,
                path=destination_path,
                label=obj.label,
                isSynced=1,
            )
            # WRITE PHOTO
            photoID = await handle_photo(p)
            # WRITE PERSON
            for person in obj.people:
                await handle_person(person, photoID)
            # WRITE EVENT
            for event in obj.events:
                await handle_event(event, photoID)
        # PHOTO PRESENT IN SQL
        else:
            photo = await FETCH_PHOTO_BY_NAME(obj.title)
            if photo is not None:
                input_format = "%Y:%m:%d %H:%M:%S"
                # Parse the input date into a datetime object
                phone_date = datetime.strptime(
                    obj.last_modified_date, input_format)
                # windows_date = datetime.strptime(photo[6], input_format)
                # windows_date = photo[6].strftime("%Y-%m-%d %H:%M:%S")
                windows_date = photo[6]
                print("Phone Date", phone_date)
                print("Windows Date", windows_date)
                if phone_date > windows_date:
                    print("Phone Date is latest")
                    await handle_remove_photo_data(obj)
                    await handle_add_photo_data(obj)
                    await update_photo_data(obj)
                else:
                    print("Windows Date is Latest, Nothing gonna happen")
    response_to_send = []
    # Return all the photos
    photos = await FETCH_PHOTOS()
    for photo in photos:
        # PERSONS
        persons = await FETCH_PERSONS_IN_PHOTO(photo.id)
        personsArray = []
        for person in persons:
            personsArray.append(person.name)

        # EVENTS
        events = await FETCH_EVENTS_IN_PHOTO(photo.id)
        eventsArray = []
        for event in events:
            eventsArray.append(event.name)

        # Response Object
        item = SyncItem(title=photo.title,
                        people=personsArray,
                        events=eventsArray,
                        label=photo.label,
                        lat=photo.lat,
                        lng=photo.lng,
                        date_taken=str(photo.date_taken),
                        last_modified_date=str(photo.last_modified_date),
                        isSynced=photo.isSynced,
                        )
        response_to_send.append(item)
    await handle_isSynced_status()
    return response_to_send


@app.get('/getAllPhotosNames')
def getAllPhotosNames():
    folderPath = "Images/"

    file_extension1 = '*.png'  # change the extension to match your image format
    file_extension2 = '*.jpg'  # change the extension to match your image format
    file_extension3 = '*.jpeg'  # change the extension to match your image format

    # use glob to get a list of all files in the folder with the specified extension
    file_list = glob.glob(os.path.join(folderPath, file_extension1)) + \
        glob.glob(os.path.join(folderPath, file_extension2)) + \
        glob.glob(os.path.join(folderPath, file_extension3))

    # print the list of files
    # print(file_list)
    img_list = []
    for file in file_list:
        x = file.rsplit("\\")[1]
        img_list.append(x)

    print(img_list)
    return img_list


@app.get('/getPhotoDetails')
async def getPhotoDetails(name: str):
    filePath = f"Images/{name}"
    names_locations = await face_recog_function(filePath)
    return names_locations


@app.post('/updateName')
async def updateName(old_names: List[str], new_names: List[str]):
    # Load data from dat file
    with open('dataset_faces.dat', 'rb') as f:
        data = pickle.load(f)

    # Rename keys in dictionary
    for old_key, new_key in zip(old_names, new_names):
        old_value = data.get(old_key)
        if old_value is not None:
            data[new_key] = old_value
            del data[old_key]

    # Save updated data back to dat file
    with open('dataset_faces.dat', 'wb') as f:
        pickle.dump(data, f)

    for old_name, new_name in zip(old_names, new_names):
        await rename_cropped_face(old_name, new_name)
        print('renamed')

    return "Done"
