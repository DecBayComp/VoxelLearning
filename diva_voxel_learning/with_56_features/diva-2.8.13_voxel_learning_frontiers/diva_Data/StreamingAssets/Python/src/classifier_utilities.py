################################################################################
################                                                ################
################ 		Definition of useful fonctions 		    ################
################                                                ################
################################################################################


# Import relevant packages
import pandas as pd
import numpy  as np
## ensemble methods
from sklearn.ensemble        import RandomForestClassifier
from sklearn.tree            import DecisionTreeClassifier
from sklearn.ensemble 	     import AdaBoostClassifier
from catboost 				 import CatBoostClassifier
from xgboost         		 import XGBClassifier
## gaussian process
from sklearn.gaussian_process         import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
##
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
##
import time


################################################################################
################################################################################
################################################################################



def perform_inference_general(set_classifier, features, nature):

	classifier    = set_classifier

	try:
		log_proba = classifier.predict_log_proba(features)
		state_out = classifier.predict(features)
		log_proba[np.where(np.isinf(log_proba))] = -100

	except AttributeError:
		state_out = classifier.predict(features)
		proba = classifier.predict_proba(features)
		log_proba = np.log(proba)
		log_proba[np.where(np.isinf(log_proba))] = -100

	return state_out, log_proba



def perform_inference_all_classifiers(set_classifier, features):

	try:
		del log_proba_out
	except NameError:
		1

	for k in set_classifier.keys():
		if k[0] == "c":
			t = time.time()
			state_out, log_proba = perform_inference_general(set_classifier[k], features, k)
			try:
				log_proba_out = np.column_stack((log_proba_out ,log_proba[:,1]))
			except NameError:
				log_proba_out = log_proba[:,1]
			print('Classifier ' + str(k) + ' inference time: ' + str(time.time() - t))

	try:
		features 			 = np.column_stack((features,log_proba_out))
	except UnboundLocalError:
		pass

	k        			 = "main"
	t = time.time()
	state_out, log_proba = perform_inference_general(set_classifier[k], features, k)
	print('Main Classifier inference time: ' +  str(time.time() - t))
	features             = np.column_stack((features,log_proba[:,1]))

	return  log_proba[:,1],state_out,features



def create_new_features_from_weak_classifiers(set_classifier, features):

	try:
		del log_proba_out
	except NameError:
		1

	for k in set_classifier.keys():
		if k[0] == "c":
			state_out, log_proba = perform_inference_general(set_classifier[k], features, k)
			try:
				log_proba_out = np.column_stack((log_proba_out ,log_proba[:,1]))
			except NameError:
				# Do something
				log_proba_out = log_proba[:,1]

	features = np.column_stack((features,log_proba_out))

	return features



############################# C1 #############################

def create_the_random_forest_classifier(state, features):

	nb_tree      = 50
	max_depth    = 50

	criterion    = 'gini'
	max_features = "sqrt"

	oob_score    = True
	warm_start   = False
	bootstrap    = True
	class_weight = None


	classifier = RandomForestClassifier(n_estimators=nb_tree, max_depth=max_depth, criterion=criterion, max_features=max_features,
										oob_score=oob_score, warm_start=warm_start, bootstrap=bootstrap, class_weight=class_weight)

	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



############################# C2 #############################

def create_xgboost_classifier(state, features):

	classifier = XGBClassifier(booster='dart', max_depth=5,
								learning_rate=0.1, objective='binary:logistic',
								eval_metric='error', normalize_type='tree')

	classifier.fit(features, state)
	score = 0

	return classifier, score



############################# C3 #############################

def create_SGD_classifier(state, features):
	
	classifier = SGDClassifier(loss='log', penalty='elasticnet', max_iter=1000,
							   tol=0.001 , shuffle=True, learning_rate='optimal', eta0=0.0)

	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



############################# C4 #############################

def create_naive_bayes_classifier(state, features):

	classifier = GaussianNB()

	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



############################# C5 #############################

def create_multilayer_perceptron_classifier(state, features):

	classifier = MLPClassifier(hidden_layer_sizes=(15, 5), max_iter=200, alpha=1e-4, 
							   solver='sgd', verbose=False, random_state=0, learning_rate_init=.001)
	
	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



############################# C10 #############################

def create_the_gaussian_process_classifier(state, features):

	kernel               = 1.0 * RBF(1.0)
	n_restarts_optimizer = 0

	classifier = GaussianProcessClassifier(kernel=kernel, n_restarts_optimizer=n_restarts_optimizer,
										   copy_X_train=False, random_state=0)
	
	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



################################################
################################################
################################################

def create_catboost_classifier(state, features):

	classifier = CatBoostClassifier(iterations=3000,
	                               learning_rate=0.03,
	                               objective="Logloss",
	                               eval_metric='AUC')

	classifier.fit(features, state, silent=True)

	score = classifier.score(features, state)

	return classifier, score



def create_adaboost_classifier_tree(state,features):

	n_estimators    = 25
	learning_rate   = 0.1 # slower than usual
	nb_trees        = 10;
	weak_classifier = DecisionTreeClassifier(max_depth=nb_trees, min_samples_split=2)
	algorithm       ='SAMME.R'


	classifier      = AdaBoostClassifier( base_estimator=weak_classifier, n_estimators= n_estimators ,
                         learning_rate= learning_rate , algorithm = algorithm)

	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



def create_adaboost_classifier_SVM(state, features):

	n_estimators    = 25 
	learning_rate   = 0.1 # slower than usual
	nb_tress        = 10
	weak_classifier = SVC(probability = True, kernel = 'linear',gamma='auto')
	algorithm       ='SAMME.R'


	classifier   = AdaBoostClassifier( base_estimator=weak_classifier, n_estimators= n_estimators ,
                         learning_rate= learning_rate , algorithm = algorithm)

	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



def create_adaboost_classifier_SGD(state, features):

	n_estimators    = 25
	learning_rate   = 0.1 # slower than usual
	l1_ratio        = 0.1
	weak_classifier = SGDClassifier(loss = 'log', penalty = 'elasticnet',max_iter=1000,
	 tol=0.001 , shuffle = True, learning_rate='optimal', eta0=0.0)
	algorithm       ='SAMME.R'


	classifier   = AdaBoostClassifier(base_estimator=weak_classifier, n_estimators= n_estimators ,
                         learning_rate= learning_rate , algorithm = algorithm)

	classifier.fit(features, state)
	score = classifier.score(features, state)

	return classifier, score



def create_Nearest_Neighbors_classifier(state, features):

	n_neighbors = 3
	weigths     = 'uniform'
	algorithm   = 'kd_tree'
	leaf_size   = 25
	metric      = 'minkowski'
	p           = 1

	classifier = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weigths, algorithm=algorithm, leaf_size=leaf_size , p=p, metric=metric)
	classifier.fit(features, state)

	score = classifier.score(features, state)

	return classifier, score


################################################################################
################################################################################
################################################################################