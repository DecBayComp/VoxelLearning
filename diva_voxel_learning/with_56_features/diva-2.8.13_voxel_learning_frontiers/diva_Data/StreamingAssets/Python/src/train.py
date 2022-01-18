################################################################################
################                                                ################
################ Definition of the class combining_classifier   ################
################                                                ################
################################################################################


# Import relevant packages
import pandas as pd
import numpy  as np

try:
    from   .classifier_utilities import *
except ImportError:
    from   classifier_utilities import *
try:
    from   .utilities import *
except ImportError:
    from   utilities import *

import warnings
import pickle
import argparse


################################################################################
################################################################################
################################################################################


class combining_classifiers:



	# Search for existing learner ; create new one if doesn't exist
	def __init__(self, full_path_or_features, classifier_path, classification_strength):

		# Path to the features table
		self.full_path = full_path_or_features
		# Path to the classifier
		self.classifier_path = classifier_path
		# Store classification strength denoting type of classifier
		self.classification_strength = classification_strength

		# Random Forest Classifier
		if self.classification_strength == 1:
			self.classif = 'rfc'

		# Gradient Boosting Classifier
		elif self.classification_strength == 2:
			self.classif = 'xgb'

		# Support Vector Machine Classifier
		elif self.classification_strength == 3:
			self.classif = 'sgd'

		# Naive Bayes Classifier
		elif self.classification_strength == 4:
			self.classif = 'nbc'

		# Multi-Layer Perceptron Classifier
		elif self.classification_strength == 5:
			self.classif = 'mlp'

		# Gaussian Process Classifier (under progress)
		elif self.classification_strength == 10:
			self.classif = 'gpc'

		# Strong Learner (Gradient Boosting Classifier with 4 weak learners)
		else:
			self.classif = 'full_xgb'

		# Create list of learner if not already existing
		try:
			liste_learner      = pickle.load(open(self.classifier_path, 'rb'))
			self.liste_learner = liste_learner
		
		except FileNotFoundError:
			self.liste_learner = []



	# Adapt training dataset to existing classifier, if applicable
	def __prepare_data_for_training__(self):
		
		# Separate states (i.e. label tags -- 0 or 1) from features
		state, features                  = prepare_data_equalize_state(self.full_path)
		self.state                       = state
		self.features                    = features

		# If no existing classifier is specified, then nothing happens
		if not self.liste_learner:
			pass

		# If an existing classifier is specified, then we perform inference and add log_proba to the features matrix
		else:
			self.__recreate_all_features_from_previous_learners__()



	# Preparde data for inference
	def __prepare_data_for_inference__(self):
		
		if not self.liste_learner:
			raise FileNotFoundError("Classifier file not found")

		self.features = self.full_path



	# In case of strong learner, apply weak classifiers to the dataset
	def __apply_multiple_classifier_to_features__(self):

		
		if self.classif == 'full_xgb':

			classifier_1, score      = create_the_random_forest_classifier(self.state, self.features)
			classifier_2, score      = create_adaboost_classifier_tree(self.state, self.features)
			classifier_3, score      = create_adaboost_classifier_SGD(self.state, self.features)
			classifier_4, score      = create_catboost_classifier(self.state, self.features)
			
			self.set_classifier      = {'c1': classifier_1, 'c2':classifier_2, 'c3':classifier_3, 'c4':classifier_4}

			self.features            = create_new_features_from_weak_classifiers(self.set_classifier, self.features)



	# Create and fit the classifier corresponding to the classification strength specified
	def __apply_main_classifier__(self, classif=None):


		if self.classif == 'rfc':
			classifier_main, score      = create_the_random_forest_classifier(self.state, self.features)


		elif self.classif == 'xgb':
			classifier_main, score      = create_xgboost_classifier(self.state, self.features)


		elif self.classif == 'sgd':
			classifier_main, score      = create_SGD_classifier(self.state, self.features)


		elif self.classif == 'nbc':
			classifier_main, score      = create_naive_bayes_classifier(self.state, self.features)


		elif self.classif == 'mlp':
			classifier_main, score      = create_multilayer_perceptron_classifier(self.state, self.features)


		elif self.classif == 'gpc':
			classifier_main, score      = create_the_gaussian_process_classifier(self.state, self.features)

		else:
			classifier_main, score      = create_xgboost_classifier(self.state, self.features)


		# Perform here inference 
		state_out, log_proba     = perform_inference_general(classifier_main, self.features, 0)

		# Define main classifier: if only 1 classifier, nothing to do 
		# in case of stacked succesive classifiers, the last one become the main one
		try:
			self.set_classifier['main']    = classifier_main
		except AttributeError:
			self.set_classifier = {'main': classifier_main}
		
		# Adapt the list of classifier as a consequence
		if not self.liste_learner:
			self.liste_learner             = [self.set_classifier]
		else:
			self.liste_learner.append(self.set_classifier)


	# Use the list of existing classifiers to perform inference and adapt then the features dataframe by adding resulting logprobas
	def __recreate_all_features_from_previous_learners__(self):

		liste_learner = self.liste_learner
		features      = self.features

		for dict_classif_loc in liste_learner:
			log_proba,_,features =  perform_inference_all_classifiers(dict_classif_loc, features)
		
		self.features  = features
		self.log_proba = log_proba


	# Perform inference and compute log proba
	def __predict_log_proba__(self):

		self.__recreate_all_features_from_previous_learners__()

		# Under progress for GPC
		# if self.classification_strength == 10:
			
		# 	proba = np.exp(self.log_proba)

		# 	def sig(x, k=50):
		# 		return 1/(1 + np.exp(-(x-.5) * k))

		# 	sig_proba = sig(proba)

		# 	self.log_proba = np.log(sig_proba)
 

		return self.log_proba


	# Perform inference and compute proba
	def __predict_proba__(self):

		self.__recreate_all_features_from_previous_learners__()

		return np.exp(self.features[:,-1])