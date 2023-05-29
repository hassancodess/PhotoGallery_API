import os
import shutil
from fastapi import FastAPI, UploadFile, File, Query, Path, Form, Depends, Body
from fastapi.staticfiles import StaticFiles

from models import *
from typing import List
from pydantic import Required
import pyodbc
from face_recog import *
from utils import *
import glob
import os
import shutil

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
    for item in items:
        print('i', item)
    return "anc"
    # Source folder path
    # source_folder = "/Images"
    # # Destination folder path
    # destination_folder = "C:\\Users\\Hassan\\Desktop\\Pictures"
    # # Loop through the list of objects
    # for obj in items:
    #     image_name = obj.title
    #     source_path = os.path.join(source_folder, image_name)
    #     destination_path = os.path.join(destination_folder, image_name)
    #     # Check if the image file exists in the source folder
    #     if os.path.isfile(source_path):
    #         # Copy the file to the destination folder
    #         shutil.copyfile(source_path, destination_path)


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
