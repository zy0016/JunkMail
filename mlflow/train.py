#!/usr/bin/python

import math
import os

import click
import keras
from keras.utils import np_utils
from keras.models import Model
from keras.callbacks import Callback
from keras.applications import vgg16
from keras.layers import Input, Dense, Flatten, Lambda
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import re
from sklearn.naive_bayes import MultinomialNB
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn import tree

import mlflow

from mail_pyfunc import log_model, KerasMailClassifierPyfunc,savelog_to_file

directory_file = "dic.ini"

def output_dic_to_file(dic):
    print("output_dic_to_file for dictionary")
    resultfile = open(directory_file,'w')
    for i in dic:
        resultfile.write(i + "\n")
    resultfile.close()

def get_allfiles_list(dir):
    all_files_list = [] 
    for path,dir_list,file_list in os.walk(dir):
        for file_name in file_list:
            all_files_list.append(os.path.join(path, file_name))

    all_files_list.sort()
    return all_files_list

def build_dictionary(dir):
    print("build_dictionary for:",dir)
    # Read the file names
    emails = get_allfiles_list(dir)
    emails.sort()
    # Array to hold all the words in the emails
    dictionary = []
    
    # Collecting all words from those emails
    for email in emails:
        m = open(os.path.join(dir, email))
        for i, line in enumerate(m):
            if len(line) > 0:
                words = line.split()
                dictionary += words
    
    # We now have the array of words, whoch may have duplicate entries
    dictionary = list(set(dictionary)) # Removes duplicates
    
    # Removes puctuations and non alphabets
    for index, word in enumerate(dictionary):
        if (word.isalpha() == False) or (len(word) == 1):
            del dictionary[index]
            
    return dictionary

def build_labels(dir):
    print("build_labels for:",dir)
    #Read the file names
    emails = get_allfiles_list(dir)
    emails.sort()
    # ndarray of labels
    labels_matrix = np.zeros(len(emails))
    for index, email in enumerate(emails):
        labels_matrix[index] = 1 if re.search('spms*', email) else 0

    return labels_matrix

def build_features(dir,dictionary):
    print("build_features for:",dir)
    # Read the file names
    emails = get_allfiles_list(dir)
    emails.sort()
    # ndarray to have the features
    features_matrix = np.zeros((len(emails), len(dictionary)))
    
    # collecting the number of occurances of each of the words in the emails
    for email_index, email in enumerate(emails):
        m = open(os.path.join(dir, email))
        for line_index, line in enumerate(m):
            words = line.split()
            for word_index, word in enumerate(dictionary):
                features_matrix[email_index, word_index] = words.count(word)
                # print("email_index:",email_index," word_index:",word_index," words.count:",str(words.count(word))," for:",word)
                
    # print(str(features_matrix))
    return features_matrix

def build_feature_for_String(sentence,dictionary):
    print("build_feature_for_String")
    features_matrix = np.zeros((1, len(dictionary)))
    
    words = sentence.split()
    for word_index, word in enumerate(dictionary):
        features_matrix[0, word_index] = words.count(word)

    return features_matrix

def output_feature_to_file(features):
    print("output_feature_to_file")
    filename = "feature.ini"
    resultfile = open(filename,'w')
    [rows, cols] = features.shape
    for i in range(rows):
        for j in range(cols):
            s = str(features[i, j]) + " "
            resultfile.write(s)
        resultfile.write("\n")

def output_txt_to_file(filename,txt):
    resultfile = open(filename,'a+')
    resultfile.write(txt + "\n")
    resultfile.close()


@click.command(help="Trains an Keras model on flower_photos dataset."
                    "The input is expected as a directory tree with pictures for each category in a"
                    " folder named by the category."
                    "The model and its metrics are logged with mlflow.")
@click.option("--training-data")
def run(training_data):
    text = "begin_study from:" + training_data
    savelog_to_file(text)
    #print(text)
    dictionary = build_dictionary(training_data)
    output_dic_to_file(dictionary)

    features_train = build_features(training_data, dictionary)
    labels_train = build_labels(training_data)

    output_feature_to_file(features_train)

    classifier = MultinomialNB()
    savelog_to_file('Training the classifier')
    classifier.fit(features_train, labels_train)
    #print("classifier:",classifier)
    text = "classifier:" + str(classifier) + "mlflow.sklearn.log_model start"
    savelog_to_file(text)

    log_model(classifier,"model")


if __name__ == '__main__':
    run()