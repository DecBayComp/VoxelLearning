################################################################################
################                                                ################
################ This script is responsible for model training  ################
################                                                ################
################################################################################


# Import relevant packages
import socket
import sys
import numpy as np
import pandas as pd
from train import combining_classifiers
import pickle
import warnings
import argparse
import time
import os


# Keep track of the timing to signal the user
start_time = time.time()


# Set a constant buffer size
DEFAULT_BUFFER_SIZE = 64


# Define the function to receive data from DIVA
def Receive(connection, remove_padding, buffer_size = DEFAULT_BUFFER_SIZE):
    
    data = b''
    msg_len = 0

    while True:
        message = connection.recv(buffer_size - msg_len)
        data += message
        msg_len = len(data)
        if len(data) == buffer_size:
            if remove_padding:
                data = data.replace(b'\x00',b'')
            return data


# Perform here the computation
if __name__ == "__main__":


    # Silence warnings
    warnings.filterwarnings('ignore')

    # Parse the input arguments
    parser = argparse.ArgumentParser()

    # Takes here server name and port for the host responsible for outsourced computing
    parser.add_argument('--server-name', type=str, help="server name", required=True)
    parser.add_argument('--server-port', type=int, help="server port", required=True)

    # Browse to point where the classifier trained will be saved
    parser.add_argument('--classifier-path', type=str, help="classifier file (.pckl) path")

    # Indicates with the slider which kind of model will be trained 
    # 1 : RFC / 2 : XGB / 3 : SVM / 4 : NBC / 5 : MLP / else : strong learner
    parser.add_argument('--classification-strength', type=int, help="classification strength (value between 1 and 10)")
    
    args = parser.parse_args()

    # Create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to the port
    server_address = (args.server_name, args.server_port)
    print("\nStarting up: " + str(server_address) +"\n")
    sock.connect(server_address)
    print("Connected...\n")

    connection_finished = False

    # Initiate dict where tagged voxels features will be stored
    tags = {}

    while True:

        # Boolean to break from loop
        if connection_finished:
            break

        # Receive size of tags array
        size_data = Receive(sock, True)
        SIZE = int(size_data)
 
        # Receive number of features, here 56
        number_of_features_data = Receive(sock, True)
        NUMBER_OF_FEATURES = int(number_of_features_data)

        print("Received inference-related metadata from DIVA\n")

        # Initiate feature number before iteration
        current_feature = 0

        # Condition reception of tags based on whether size of tags received

        if size_data:

            # Receive/send operations with Unity
            while True:

                # Receive label from Unity
                label_data = Receive(sock, True)

                if label_data:

                    # Receive data according to tags array size
                    tags_data = Receive(sock, False, SIZE)

                    # Add to tags dictionary
                    tags[label_data] = np.frombuffer(tags_data, dtype=np.uint8).astype(np.float)

                    # Increment feature received
                    current_feature += 1

                else:
                    connection_finished = True
                    break

                # Increment brick if number of features reached, all 56 features have been retrieved for this brick
                if current_feature == NUMBER_OF_FEATURES:
                    print("Training data received; exiting program\n")
                    connection_finished = True
                    break

        else:
            break

    # Clean up connection
    sock.close()

    # Transform features tags into pandas dataframe
    features_df = pd.DataFrame({str(label): tags[label] for label in tags})

    # Uncomment here to save features dataframe as csv file
    # features_df.to_csv(os.path.join(os.path.dirname(args.classifier_path), 'features_df.csv'), sep=';')

    # Initiate classifier
    glob_class = combining_classifiers(pd.DataFrame({str(label): tags[label] for label in tags}), args.classifier_path, args.classification_strength)

    # Prepare data for training
    glob_class.__prepare_data_for_training__()
    glob_class.__apply_multiple_classifier_to_features__()

    # Train final model
    glob_class.__apply_main_classifier__()

    # Print type of model trained and training time in seconds
    print(glob_class.classif)
    print("--- %s seconds ---" % (time.time() - start_time))


    # Save classifier in specified folder
    if args.classifier_path != "":
        # filename = "liste_classifier.pckl"
        pickle.dump(glob_class.liste_learner, open(args.classifier_path, 'wb'))

    # Exit script
    exit()
