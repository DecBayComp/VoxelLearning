################################################################################
################                                                ################
################ This script is responsible for model inference ################
################                                                ################
################################################################################


# Import relevant packages
import socket
import sys
import numpy as np
import pandas as pd
import warnings
import argparse
import time
import pickle
import os

from train import combining_classifiers


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

# Define the function to send data back to DIVA
def Send(connection, add_padding, buffer, buffer_size = DEFAULT_BUFFER_SIZE):
    if add_padding:
        connection.sendall(buffer + b'\x00' * (buffer_size - len(buffer)))
    else:
        print(str(buffer) + " Sent")
        connection.sendall(buffer)


# Perform here the computation
if __name__ == "__main__":


    # Silence warnings
    warnings.filterwarnings('ignore')

    # Parse the input arguments
    parser = argparse.ArgumentParser()

    # Takes here server name and port for the host responsible for outsourced computing
    parser.add_argument('--server-name', type=str, help="server name", required=True)
    parser.add_argument('--server-port', type=int, help="server port", required=True)

    # Browse to point where the classifier used for inference will be loaded from
    parser.add_argument('--classifier-path', type=str, help="classifier file (.pckl) path", required=True)
    
    # Not used here
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

    # Initiate list of packets with proba format uint8 to reconstruct further
    proba_packet_list = []

    # Initiate dict where voxels features will be stored
    image_features = {}

    while True:
        
        # Boolean to break from loop
        if connection_finished:
            break

        # Receive size of tags array
        size_data = Receive(sock, True)
        SIZE = int(size_data)
        print("Size of brick: " + str(SIZE))

        # Receive number of bricks/packets, depending on the global size of the image
        number_of_bricks_data = Receive(sock, True)
        NUMBER_OF_BRICKS = int(number_of_bricks_data)
        print("Number of bricks: " + str(NUMBER_OF_BRICKS))

        # Receive number of features, here 56
        number_of_features_data = Receive(sock, True)
        NUMBER_OF_FEATURES = int(number_of_features_data)
        print("Number of features: " + str(NUMBER_OF_FEATURES) + "\n")

        # Initiate feature number and brick number before iteration
        current_feature = 0
        current_brick =  0

        # Condition reception of tags based on whether size of packet received
        if size_data:
            
            # Receive/send operations with Unity
            while True:
                
                # Receive label from Unity
                label_data = Receive(sock, True)
                if label_data:
                    
                    # Receive data according to feature array size
                    feature_data = Receive(sock, False, SIZE)

                    # Add to image feature dictionary
                    image_features[label_data] = np.frombuffer(feature_data, dtype=np.uint8).astype(np.float)

                    # Increment feature received
                    current_feature += 1
                
                else:
                    connection_finished = True
                    break

                # Increment brick if number of features reached, all 56 features have been retrieved
                if current_feature == NUMBER_OF_FEATURES:

                    # Indicates user which brick is being processed
                    print("Brick # " + str(current_brick))

                    # Reset number of features and start over
                    current_feature = 0
                    print("\nInferring... {0:.0f}%".format(100*(current_brick+1)/NUMBER_OF_BRICKS))
                    current_brick += 1


                    # Initiate classifier to perform inference
                    glob_class = combining_classifiers(pd.DataFrame({str(label): image_features[label] for label in image_features}), args.classifier_path, args.classification_strength)
                    glob_class.__prepare_data_for_inference__()

                    # Predict output log probabilities
                    log_proba = glob_class.__predict_log_proba__()
                    # Convert it to probabilities
                    proba = np.exp(log_proba)

                    # Convert it to level of gray in 8-bit
                    proba = (1 - proba) * 255
                    proba_uint8 = proba.astype(np.uint8)

                    # Send it back to DIVA
                    sock.sendall(proba_uint8.tobytes())

                    # Keep track of proba file for parallel saving
                    proba_packet_list.append(proba_uint8)


                    # Print final computation time
                    print("--- %s seconds ---" % (time.time() - start_time))


                    # Exit program after all bricks classified
                    if current_brick == NUMBER_OF_BRICKS:
                        print("Inference finished; exiting program")
                        connection_finished = True
                        break
        
        else:
            break


    # Uncomment here to save the proba file for further processing and comparison
    # file_name = os.path.join(os.path.dirname(os.getcwd()), 'Reconstruction', '{0}_proba_{1}.pckl'.format(args.classifier_path[-8:-5], NUMBER_OF_FEATURES))
    # pickle.dump(proba_packet_list, open(file_name, "wb"))


    # Clean up connection
    sock.close()

    # Exit script
    exit()
