################################################################################
################                                                ################
################ 		Definition of useful fonctions 		    ################
################                                                ################
################################################################################

# Import relevant packages
import pandas as pd
import numpy  as np
import os
import base64
import json


############################################
############################################
############################################


def split_state_features_with_header(data):

	liste_loc       = data.columns.tolist()

	if liste_loc[0] == "b'LABEL'":
		state    = data["b'LABEL'"].copy()
		# remove labels column
		features = data.drop("b'LABEL'", axis = 1)
	else:
		state    = data.iloc[:,0].copy()
		# remove labels column
		features = data.drop(data.columns[0],axis = 1)

	return state, features



def dataframe_to_array(state, features):
	
	state2     = state.values
	features2  = features.values

	return state2, features2



def prepare_data_equalize_state(full_path_to_tagged_data):

	if isinstance(full_path_to_tagged_data,str):
	 	data            = pd.read_csv(full_path_to_tagged_data)
	else:
		data 			= full_path_to_tagged_data

	# contains feature name for each column
	liste_loc       = data.columns.tolist()

	# header specified
	if (liste_loc[0] == "b'LABEL'"):
		data_0          = data[ data["b'LABEL'"]==0]
		data_1          = data[ data["b'LABEL'"]==1]
	# if no header
	else:
		data_0          = data[ data.iloc[:,0]==0]
		data_1          = data[ data.iloc[:,0]==1]

	nb_size_data    = data.shape
	nb_size_data_0  = data_0.shape
	nb_size_data_1  = data_1.shape

	nb_to_gen       = int(nb_size_data[0])
	nb_to_gen_2     = int(np.floor(nb_to_gen/2))
	nb_to_gen_0     = int(nb_size_data_0[0])
	nb_to_gen_1     = int(nb_size_data_1[0])

	II_0            = np.random.randint(nb_to_gen_0, size =nb_to_gen_2)
	II_1            = np.random.randint(nb_to_gen_1, size =nb_to_gen_2)

	data_0          = data_0.iloc[II_0]
	data_1          = data_1.iloc[II_1]
	data            = pd.concat([data_0,data_1])

	state, features = split_state_features_with_header(data)
	state, features = dataframe_to_array(state, features)

	state           = np.ravel(state)

	return  state, features



def create_file_list(path, extension):

    return_list = []
    for file_name in os.listdir(path):
        if file_name.endswith((extension)):
            return_list.append(file_name)
            
    return_list.sort()

    return return_list



def create_df_features(input_features_file):
    
    with open(os.path.join('inference', input_features_file), "r") as file:
        json_data = json.load(file)

    image_features = {}

    for label_data, feature_data_str in json_data.items():
        feature_data_str_ascii = feature_data_str.encode("ascii")
        feature_data = base64.b64decode(feature_data_str_ascii)
        image_features[label_data] = np.frombuffer(feature_data, dtype=np.uint8).astype(np.float)

    data_df = pd.DataFrame({str(label): image_features[label] for label in image_features})
    
    return data_df