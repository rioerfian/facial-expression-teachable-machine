import numpy as np
import cv2
import os
import random
from pathlib import Path
from shutil import copyfile


#fungsi mencopy dan men split dataset ke data/training dan data/validation
def split_data(source, training, validation, split_size):
    files = []
    for filename in os.listdir(source):
        file = source + "/" + filename
        if os.path.getsize(file) > 0:
            files.append(filename)
        else:
            print(filename + " is zero length, so ignoring.")

    training_length = int(len(files) * split_size)
    valid_length = int(len(files) - training_length)
    shuffled_set = random.sample(files, len(files))
    training_set = shuffled_set[0:training_length]
    valid_set = shuffled_set[training_length:]

    for filename in training_set:
        this_file = source + "/" + filename
        destination = training + "/" + filename
        copyfile(this_file, destination)

    for filename in valid_set:
        this_file = source + "/" + filename
        destination = validation + "/" + filename
        copyfile(this_file, destination)


#fungsi mengambil dataframe image ke class
def capturingFrame(formatName):
    cap = cv2.VideoCapture(0)
    count = 0
    split_size = .85
    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        Path("dataset/{}".format(formatName)).mkdir(parents=True,
                                                    exist_ok=True)
        cv2.imwrite(
            "dataset/{}/{}_{}.jpg".format(formatName, formatName, count),
            frame)
        count = count + 1
        print(count)

        # Display the resulting frame
        cv2.imshow('{}'.format(formatName), frame)

        if cv2.waitKey(1) != -1:
            cv2.destroyAllWindows()
            break

    Path("data/training/{}".format(formatName)).mkdir(parents=True,
                                                      exist_ok=True)
    Path("data/validation/{}".format(formatName)).mkdir(parents=True,
                                                        exist_ok=True)

    #dan setelah mendapat dataset langsung dijalankan fungsi split data nya
    split_data("dataset/{}".format(formatName),
               "data/training/{}".format(formatName),
               "data/validation/{}".format(formatName), split_size)