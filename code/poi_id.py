#!/usr/bin/python

import poi_plot, poi_explore, poi_select, poi_tune, features_db, tester
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=4)

import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# Switch to True to display the main features of the Exploration
print_plot = False
print_explore = False
print_select = False
print_tune = False
print_validate = False

# Load the dictionary containing the dataset
with open("../data/final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


# PART 1: Data Exploration
# Related file: poi_explore.py

if print_explore:
    # Get the size of the dictionary containing the dataset
    print "* Dataset length:", poi_explore.get_size(data_dict)
    # Get the number of POI in the dataset
    print "* Number of POI:", poi_explore.count_poi(data_dict)

if print_explore:
    # Get a list of all the features and the number of NaNs each one contains
    print "* List of NaNs per feature:"
    pp.pprint(poi_explore.count_nan(data_dict))

# Replace all the NaNs in financial features with zeros
data_dict = poi_explore.nan_replacer(data_dict)

if print_explore:
    print "* List of NaNs per feature once replaced NaNs for zeros:"
    pp.pprint(poi_explore.count_nan(data_dict))

if print_plot:
    # Scatterplot: bonus vs. salary
    fig1 = poi_plot.scatterplot(data_dict, "salary", "bonus")

# Find the outlier with the highest salary
outlier = poi_explore.sort_data(data_dict, "salary", 1, reverse=True)

if print_explore:
    outlier_name = poi_explore.get_name(data_dict, "salary", outlier[0])
    print "* Outlier found:", outlier_name

# Remove outlier TOTAL
data_dict.pop('TOTAL', None)

if print_explore:
    # Find persons with little or no information
    print "* List of persons with more than 90% of data missing:"
    pp.pprint(poi_explore.get_incompletes(data_dict, 0.90))

# Remove outliers from get_incompletes()
more_outliers = ['WHALEY DAVID A',
                 'WROBEL BRUCE',
                 'LOCKHART EUGENE E',
                 'THE TRAVEL AGENCY IN THE PARK',
                 'GRAMM WENDY L']

for o in more_outliers:
    data_dict.pop(o, None)


# PART 2: Selected Features
# Related file: poi_select.py

# Default dataset features to test base line performance
feat_1 = features_db.feat_1

# Get baseline performance from the three algorithms
if print_select:
    print "Settings: \n* Features: default \n* Tuning: default"
    clf_AB = AdaBoostClassifier()
    # tester.test_classifier(clf_AB, data_dict, feat_1)
    clf_RF = RandomForestClassifier()
    # tester.test_classifier(clf_RF, data_dict, feat_1)
    clf_SVC = SVC(kernel='linear', max_iter=1000)
    # tester.test_classifier(clf_SVC, data_dict, feat_1)
    print "\n"

# Updated feature list, removed features w/ +60% NaNs
feat_2 = features_db.feat_2

# Get new performance with feat_2
if print_select:
    print "Settings: \n* Features: remove features w/ +60% NaN \n* Tuning: default"
    clf_AB = AdaBoostClassifier()
    # tester.test_classifier(clf_AB, data_dict, feat_2)
    clf_RF = RandomForestClassifier()
    # tester.test_classifier(clf_RF, data_dict, feat_2)
    clf_SVC = SVC(kernel='linear', max_iter=1000)
    # tester.test_classifier(clf_SVC, data_dict, feat_2)
    print "\n"

# Create new engineered features
# f_bonus
data_dict = poi_select.create_feature(data_dict,
                                      "bonus",
                                      "total_payments",
                                      "f_bonus")
# f_salary
data_dict = poi_select.create_feature(data_dict,
                                      "salary",
                                      "total_payments",
                                      "f_salary")
# f_stock
data_dict = poi_select.create_feature(data_dict,
                                      "total_stock_value",
                                      "total_payments",
                                      "f_stock")
# r_from
data_dict = poi_select.create_feature(data_dict,
                                      "from_this_person_to_poi",
                                      "from_messages",
                                      "r_from")
# r_to
data_dict = poi_select.create_feature(data_dict,
                                      "from_poi_to_this_person",
                                      "to_messages",
                                      "r_to")

# Add new engineered features
feat_3 = features_db.feat_3

# Get new performance with feat_3
if print_select:
    print "Settings: \n* Features: add engineered features \n* Tuning: default"
    clf_AB = AdaBoostClassifier()
    # tester.test_classifier(clf_AB, data_dict, feat_3)
    clf_RF = RandomForestClassifier()
    # tester.test_classifier(clf_RF, data_dict, feat_3)
    clf_SVC = SVC(kernel='linear', max_iter=1000)
    # tester.test_classifier(clf_SVC, data_dict, feat_3)
    print "\n"

# Get the most important features based on SelectKBest
if print_select:
    poi_select.kbest(data_dict, feat_1)

# New feature list with 10 most important features from SelectKBest
feat_K = features_db.feat_K

# Get new performance with feat_K
if print_select:
    print "Settings: \n* Features: SelectKBest \n* Tuning: default"
    clf_AB = AdaBoostClassifier()
    # tester.test_classifier(clf_AB, data_dict, feat_K)
    clf_RF = RandomForestClassifier()
    # tester.test_classifier(clf_RF, data_dict, feat_K)
    clf_SVC = SVC(kernel='linear', max_iter=1000)
    # tester.test_classifier(clf_SVC, data_dict, feat_K)
    print "\n"

# Get the importance of each feature from feature_importances_
if print_select:
    poi_select.feature_importances(data_dict, feat_3, 0.35)

# Remove less important features from feature_importances_
feat_4AB = features_db.feat_4AB
feat_4RF = features_db.feat_4RF
feat_4SVC = features_db.feat_4SVC

# Get new performance with feat_4*
if print_select:
    print "Settings: \n* Features: .feature_importances_ \n* Tuning: default"
    clf_AB = AdaBoostClassifier()
    tester.test_classifier(clf_AB, data_dict, feat_4AB)
    clf_RF = RandomForestClassifier()
    tester.test_classifier(clf_RF, data_dict, feat_4RF)
    clf_SVC = SVC(kernel='linear', max_iter=1000)
    tester.test_classifier(clf_SVC, data_dict, feat_4SVC)
    print "\n"


# PART 3: Algorithm Tuning
# Related file: poi_tune.py

# Fine tune the classifiers
if print_tune:
    poi_tune.ab_tune(data_dict, feat_4AB, True)
    poi_tune.rf_tune(data_dict, feat_4RF, True)
    poi_tune.svc_tune(data_dict, feat_4SVC)

# Code Review: store to my_dataset and my_features for easy export below
my_clf = poi_tune.get_svc(data_dict, feat_4SVC)
my_dataset = data_dict
my_features = feat_4SVC

dump_classifier_and_data(my_clf, my_dataset, my_features)

# Validate the algorithm
if print_validate:
    poi_select.test_clf(data_dict, feat_4SVC, random_state=42)
