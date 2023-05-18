import face_recognition  # operation face
import pickle
import uuid
import numpy as np
from typing import List


async def face_recog_function(__image):  # async
    print("Start")
    return_names = {}
    img1 = face_recognition.load_image_file(__image)
    img1_encodings = face_recognition.face_encodings(img1)
    img1_faceLocations = face_recognition.face_locations(img1)
    print("Locations", img1_faceLocations)
    try:
        all_face_encodings = pickle.load(open("dataset_faces.dat", "rb"))
        # print(type(all_face_encodings)) # DICTIONARY
        print("Length", len(all_face_encodings))  # Length
    except:
        all_face_encodings = {}
    if len(all_face_encodings) == 0:
        for encoding, location in zip(img1_encodings, img1_faceLocations):
            print("Loop will run:", len(img1_encodings), "times")
            # Generate a new UUID
            uuid_long = uuid.uuid4()
            # Extract the first 3 characters
            uuid_short = str(uuid_long)[:4]
            print("UUID", uuid_short)
            all_face_encodings[f"unknown_face_{uuid_short}"] = encoding
            # all_face_encodings[f"unknown_face_{face_count}"] = encoding
            # return_names.append(f"unknown_face_{uuid_short}")
            return_names[f"unknown_face_{uuid_short}"] = location

        print("About to write ")
        with open('dataset_faces.dat', 'wb') as f:
            pickle.dump(all_face_encodings, f)
        # output = []
        # for i in range(1, face_count):
            # output.append(f"unknown_face_{i}")
        # print("Returing names", return_names)
        return return_names
    else:
        # return_names: List[str] = []
        face_names = list(all_face_encodings.keys())
        face_encodings = np.array(list(all_face_encodings.values()))
        for encoding, location in zip(img1_encodings, img1_faceLocations):
            print("ELSE: Loop will run:", len(img1_encodings), "times")
            result = face_recognition.compare_faces(face_encodings, encoding)
            if True in result:
                # names_with_result = list(zip(face_names, result))
                # Appends name to return_names to return output of this function
                for n, r in zip(face_names, result):
                    if (r):
                        return_names[n] = location
                        # return_names.append(n)
            else:
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
                return_names[f"unknown_face_{uuid_short}"] = location
                # return_names.append(f"unknown_face_{uuid_short}")
                # Save the updated data to the .dat file
                with open("dataset_faces.dat", "wb") as f:
                    pickle.dump(all_face_encodings, f)
    # print(return_names)
    return return_names


def get_all_names():
    all_face_encodings = pickle.load(open("dataset_faces.dat", "rb"))
    face_names = list(all_face_encodings.keys())
    print(face_names)


# get_all_names()
