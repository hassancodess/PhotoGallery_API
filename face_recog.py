import face_recognition  # operation face
import pickle
import uuid
import numpy as np
from typing import List
import cv2


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
    result = face_recognition.compare_faces(encoding1, encoding2)
    return result


async def handle_matched_faces(face_names, result, location, faces):
    for n, r in zip(face_names, result):
        print('here in for loop')
        if (r):
            print('here in IF')
            faces[n] = location
            break


async def handle_empty_dataset(all_face_encodings, img_face_encodings, img_face_locations):
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

    await rewrite_encodings_to_dataset(all_face_encodings)
    return response


async def face_recog_function(__image):  # async
    print("Start")
    faces = {}

    img_face_locations, img_face_encodings = await get_face_locations_and_encoding(
        __image)

    if (len(img_face_locations) != 0):
        all_face_encodings = await get_all_encodings_from_dataset()
        if len(all_face_encodings) == 0:
            faces = await handle_empty_dataset(all_face_encodings, img_face_encodings, img_face_locations)
        else:
            await handle_dataset(all_face_encodings, img_face_encodings, img_face_locations, faces)
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


async def handle_dataset(all_face_encodings, img_face_encodings, img_face_locations, faces):
    face_names, face_encodings = await get_names_encodings_of_dataset(all_face_encodings)
    for encoding, location in zip(img_face_encodings, img_face_locations):
        result = await compare_face_encodings(face_encodings, encoding)
        if True in result:
            # response = await handle_matched_faces(face_names, result, location)
            await handle_matched_faces(face_names, result, location, faces)
        else:
            await handle_unmatched_faces(all_face_encodings, encoding, location, faces)
            await rewrite_encodings_to_dataset(all_face_encodings)

    # en = await get_all_encodings_from_dataset()
    # f, b = await get_names_encodings_of_dataset(en)
    # print('new', f)

    # print(response)
    # else:
    #     # return_names: List[str] = []
    #     face_names = list(all_face_encodings.keys())
    #     print('faces', face_names)
    #     face_encodings = np.array(list(all_face_encodings.values()))
    #     ind = 1
    #     for encoding, location in zip(img_face_encodings, img_face_locations):
    #         # print("ELSE: Loop will run:", len(img_face_encodings), "times")
    #         print("Loop", ind)
    #         result = face_recognition.compare_faces(face_encodings, encoding)
    #         print(f"result-{ind}", result)
    #         ind = ind+1
    #         if True in result:
    #             print('here')
    #             # names_with_result = list(zip(face_names, result))
    #             # Appends name to return_names to return output of this function
    #             for n, r in zip(face_names, result):
    #                 print('here in for loop')
    #                 if (r):
    #                     print('here in IF')
    #                     return_names[n] = location
    #                     break
    #                     # return_names.append(n)
    #         else:
    #             # Generate a new UUID
    #             uuid_long = uuid.uuid4()
    #             # Extract the first 3 characters
    #             uuid_short = str(uuid_long)[:4]
    #             print("ELSE: UUID", uuid_short)
    #             # Adding unique face name to dictionary
    #             # print("Length before writing", len(all_face_encodings))
    #             all_face_encodings[f"unknown_face_{uuid_short}"] = encoding
    #             # print("Length after writing", len(all_face_encodings))
    #             # appending new name to return_names
    #             return_names[f"unknown_face_{uuid_short}"] = location
    #             # return_names.append(f"unknown_face_{uuid_short}")
    #             # Save the updated data to the .dat file
    #             with open("dataset_faces.dat", "wb") as f:
    #                 pickle.dump(all_face_encodings, f)
    # # print(return_names)
    # return return_names


def get_all_names():
    all_face_encodings = pickle.load(open("dataset_faces.dat", "rb"))
    face_names = list(all_face_encodings.keys())
    print(face_names)


# get_all_names()
