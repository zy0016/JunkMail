import os
import base64
import requests

import click
import pandas as pd

from mlflow.utils import cli_args
import numpy as np
import re
from sklearn.naive_bayes import MultinomialNB
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn import tree
import json
import requests
from mail_pyfunc import log_model, KerasMailClassifierPyfunc,savelog_to_file

directory_file = "dic.ini"

def read_dic(filename):
    dic = []
    with open(filename) as f:
        for line in f:
            strall = line.strip()
            dic.append(strall)
    return dic

def build_feature_for_String(sentence,dictionary):
    #print("build_feature_for_String")
    features_matrix = np.zeros((1, len(dictionary)))
    
    words = sentence.split()
    for word_index, word in enumerate(dictionary):
        features_matrix[0, word_index] = words.count(word)

    return features_matrix

def savejson_to_file(filename,text):
    resultfile = open("/tmp/" + filename,'w')
    resultfile.write(text + "\n")
    resultfile.close()

def get_allfiles_list(dir):
    all_files_list = [] 
    for path,dir_list,file_list in os.walk(dir):
        for file_name in file_list:
            all_files_list.append(os.path.join(path, file_name))

    all_files_list.sort()
    return all_files_list

def score_model(path, uri, port):
    """
    Score mailfile on the local path with MLflow model deployed at given uri and port.

    :param path: Path to a single mail file.
    :param uri: URI the model is deployed at
    :param port: Port the model is deployed at.
    :return: Server response.
    """
    # if os.path.isdir(path):
    #     filenames = [os.path.join(path, x) for x in os.listdir(path)
    #                  if os.path.isfile(os.path.join(path, x))]
    # else:
    #     filenames = [path]

    # def read_image(x):
    #     with open(x, "rb") as f:
    #         return f.read()
    text = "path:" + path + " uri:" + uri + " port:" + port
    savelog_to_file(text,False)
    
    file_c = ""
    with open(path) as f:
        for line in f:
            strall = line.strip()
            file_c = file_c + strall + " "

    dictionary = read_dic(directory_file)
    features_test = build_feature_for_String(file_c,dictionary)
    curstr = "{\"columns\":["
    columns = ""
    for i in dictionary:
        columns = columns + "\"" + i + "\","

    curstr = curstr + columns[0:-1] + "],"

    dic={}
    dic['data']=features_test.tolist()
    dicJson = json.dumps(dic)
    json1 = dicJson.replace("{","")
    json2 = json1.replace("}","")
    curstr = curstr + json2 + "}"

    savejson_to_file(path[path.rfind("/") + 1:] + ".log",curstr)
    # data = pd.DataFrame(data=[base64.encodebytes(read_image(x)) for x in filenames],
    #                     columns=["image"]).to_json(orient="split")

    response = requests.post(url='{uri}:{port}/invocations'.format(uri=uri, port=port),
                             data=curstr,
                             headers={"Content-Type": "application/json; format=pandas-split"})

    if response.status_code != 200:
        raise Exception("Status Code {status_code}. {text}".format(
            status_code=response.status_code,
            text=response.text
        ))
    return response

def run(file_path, model_uri, port):
    """
    Score mail file with MLflow deployed deployed at given uri and port and print out the response
    to standard out.
    """
    if os.path.exists(file_path):
        filelist = get_allfiles_list(file_path)
        for i in filelist:
            text = i + " -> " + score_model(i, model_uri, port).text
            print(text)
    else:
        text = file_path + " -> " + score_model(file_path, model_uri, port).text
        print(txt)


if __name__ == '__main__':
    #run("/root/mlflow/junkmail/5-1298msg1.txt","http://localhost","54321")
    run("/root/mlflow/junkmail/test_data","http://localhost","54321")
