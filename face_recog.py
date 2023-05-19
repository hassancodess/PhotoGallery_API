import face_recognition  # operation face
import pickle
import uuid
import numpy as np
from typing import List
import cv2
import os
from PIL import Image


async def get_face_locations_and_encoding(image):
    img = face_recognition.load_image_file(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_face_locations = face_recognition.face_locations(img)
    img_face_encodings = face_recognition.face_encodings(
        img, img_face_locations)

    return img_face_locations, img_face_encodings


async def get_all_encodings_from_dataset():
    try:
        all_face_encodings = pickle.load(open("dataset_faces.dat", "rb"))
        # print(type(all_face_encodings)) # DICTIONARY
        return all_face_encodings
    except:
        all_face_encodings = {}
        return all_face_encodings


async def rewrite_encodings_to_dataset(all_face_encodings):
    with open('dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)


async def get_names_encodings_of_dataset(all_face_encodings):
    face_names = list(all_face_encodings.keys())
    # print('faces', face_names)
    face_encodings = np.array(list(all_face_encodings.values()))
    return face_names, face_encodings


async def compare_face_encodings(encoding1, encoding2):
    result = face_recognition.compare_faces(
        encoding1, encoding2, tolerance=0.6)
    return result


async def handle_matched_faces(face_names, result, location, faces):
    for n, r in zip(face_names, result):
        print('here in for loop')
        if (r):
            print('here in IF')
            if n not in faces:
                faces[n] = location
                break


async def handle_empty_dataset(all_face_encodings, img_face_encodings, img_face_locations, image_path):
    response = {}
    for encoding, location in zip(img_face_encodings, img_face_locations):
        # print("Loop will run:", len(img_face_encodings), "times")
        # Generate a new UUID
        uuid_long = uuid.uuid4()
        # Extract the first 3 characters
        uuid_short = str(uuid_long)[:4]
        # print("UUID", uuid_short)
        all_face_encodings[f"unknown_face_{uuid_short}"] = encoding
        response[f"unknown_face_{uuid_short}"] = location

    # response
    print('here before crop faces')
    await crop_and_save_faces(image_path, response)
    print('here after crop faces')
    # save imaegs
    await rewrite_encodings_to_dataset(all_face_encodings)
    return response


async def face_recog_function(__image):  # async
    print("Start")
    faces = {}

    img_face_locations, img_face_encodings = await get_face_locations_and_encoding(__image)

    if (len(img_face_locations) != 0):
        all_face_encodings = await get_all_encodings_from_dataset()
        if len(all_face_encodings) == 0:
            faces = await handle_empty_dataset(all_face_encodings, img_face_encodings, img_face_locations, __image)
        else:
            await handle_dataset(all_face_encodings, img_face_encodings, img_face_locations, faces, __image)
        return faces

    else:
        return "No faces found"


async def handle_unmatched_faces(all_face_encodings, encoding, location, faces):
    # Generate a new UUID
    uuid_long = uuid.uuid4()
    # Extract the first 3 characters
    uuid_short = str(uuid_long)[:4]
    print("ELSE: UUID", uuid_short)
    # Adding unique face name to dictionary
    # print("Length before writing", len(all_face_encodings))
    all_face_encodings[f"unknown_face_{uuid_short}"] = encoding
    # print("Length after writing", len(all_face_encodings))
    # appending new name to return_names
    faces[f"unknown_face_{uuid_short}"] = location


async def handle_dataset(all_face_encodings, img_face_encodings, img_face_locations, faces, __image):
    face_names, face_encodings = await get_names_encodings_of_dataset(all_face_encodings)
    results = []
    # adds result to m results
    for encoding, location in zip(img_face_encodings, img_face_locations):
        result = await compare_face_encodings(face_encodings, encoding)
        # print('result', result)
        my_tuple = (encoding, location, result)
        results.append(my_tuple)

    sorted_results = sorted(results, key=lambda tuple_: sum(tuple_[2]))

    # print('Sorted Results', sorted_results)
    for tuple_ in sorted_results:
        array = tuple_[2]  # Access the array inside the tuple using indexing
        print("Sorted", array)
        if True in array:
            await handle_matched_faces(face_names, array, tuple_[1], faces)
        else:
            await handle_unmatched_faces(all_face_encodings, tuple_[0], tuple_[1], faces)
            await rewrite_encodings_to_dataset(all_face_encodings)
        # print('results', results)
    await crop_and_save_faces(__image, faces)


def get_all_names():
    all_face_encodings = pickle.load(open("dataset_faces.dat", "rb"))
    face_names = list(all_face_encodings.keys())
    print(face_names)


async def crop_and_save_faces(image_path, faces):

    output_folder = f"ImagesCropped/"
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create a folder for image
    folderName = await get_image_name_from_image_path(image_path)
    image_folder = os.path.join(output_folder, folderName)
    os.makedirs(image_folder, exist_ok=True)

    # for i, location in enumerate(face_locations):
    for name, location in zip(faces.keys(), faces.values()):
        top, right, bottom, left = location
        cropped_face = image[top:bottom, left:right]

        # Save the cropped face image
        output_path = os.path.join(image_folder, f"{name}.jpg")
        cv2.imwrite(output_path, cropped_face)


async def get_image_name_from_image_path(imagePath):
    # Extracts the last part after splitting by "/"
    filename = imagePath.split("/")[-1]
    # Remove the file extension
    filename = filename.split(".")[0]
    return filename


async def get_image_name_and_extension(file_path):
    # # Get the filename without the extension
    # filename = os.path.splitext(os.path.basename(imagePath))[0]
    # # Extract the relevant part from the filename
    # relevant_part = filename.split("_", 1)[1]
    # return relevant_part
    # Get the filename with extension
    filename = os.path.basename(file_path)

    # Split the filename into name and extension
    name, extension = os.path.splitext(filename)

    # Return the name and extension
    return name, extension


async def rename_cropped_face(old_name, new_name):
    root_folder = "ImagesCropped"
    for folder_name, subfolders, filenames in os.walk(root_folder):
        # print('folder name', folder_name)
        for filename in filenames:
            # print('file name', filename)
            # Check if the filename matches the condition
            if filename.startswith(old_name):
                # Get the full path of the image file
                file_path = os.path.join(folder_name, filename)
                # print('file path', file_path)
                name, extension = await get_image_name_and_extension(file_path)
                # print('name, extension', name, extension)

                # Create the new name for the image based on your requirements
                new_filename = f"{new_name}{extension}"
                # print('new file name', new_filename)

                # Construct the new full path with the updated name
                new_file_path = os.path.join(folder_name, new_filename)
                # print('new file path', new_file_path)
                # Rename the image file
                os.rename(file_path, new_file_path)
