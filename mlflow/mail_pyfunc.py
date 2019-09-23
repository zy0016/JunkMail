"""
Example of a custom python function implementing mail classifier with mail preprocessing embedded
in the model.
"""
import base64
from io import BytesIO
import keras
import numpy as np
import os
import pandas as pd
import PIL
from PIL import Image
import yaml
import tensorflow as tf

import mlflow
import mlflow.keras
import mlflow.sklearn
from mlflow.utils import PYTHON_VERSION
from mlflow.utils.file_utils import TempDir
from mlflow.utils.environment import _mlflow_conda_env

class KerasMailClassifierPyfunc(object):
    def __init__(self,model):
        self._model = model

    def predict(self, input):
        """
        Generate predictions for the data.

        :param input: pandas.DataFrame with one column containing images to be scored. 
        :return: pandas.DataFrame containing predictions with the following schema:
                     Predicted class: string,
                     Predicted class index: int,
                     Probability(class==0): float,
                     ...,
                     Probability(class==N): float,
        """
        probs = self._predict_mail(input)
        return probs

    def _predict_mail(self,x):
        return self._model.predict(x)


def log_model(keras_model,artifact_path):
    savelog_to_file("log_model:" + artifact_path)
    with TempDir() as tmp:
        data_path = tmp.path("mail_model")
        os.mkdir(data_path)
        keras_path = os.path.join(data_path, "keras_model")
        
        savelog_to_file("data_path:" + data_path)
        savelog_to_file("call keras_path:" + str(keras_path))

        mlflow.sklearn.save_model(keras_model,path=keras_path)
        conda_env = tmp.path("conda_env.yaml")

        savelog_to_file("conda_env:" + conda_env)

        #txt = "python_version="+PYTHON_VERSION+"\nkeras_version="+keras.__version__+"\ntf_name="+tf.__name__+"\ntf_version="+tf.__version__+"\npillow_version="+PIL.__version__
        #output_txt_to_file(conda_env,txt)
        with open(conda_env, "w") as f:
            f.write(conda_env_template.format(python_version=PYTHON_VERSION,
                                              keras_version=keras.__version__,
                                              tf_name=tf.__name__,  # can have optional -gpu suffix
                                              tf_version=tf.__version__,
                                              pillow_version=PIL.__version__))

        savelog_to_file("call mlflow.pyfunc.log_model")
        mlflow.pyfunc.log_model(artifact_path=artifact_path,
                                loader_module=__name__,
                                code_path=[__file__],
                                data_path=data_path,
                                conda_env=conda_env)

def _load_pyfunc(path):
    """
    Load the KerasMailClassifierPyfunc model.
    """
    savelog_to_file("_load_pyfunc path:" + path)
    keras_model_path = os.path.join(path, "keras_model")
    savelog_to_file("keras_model_path from mail:" + keras_model_path)
    with tf.Graph().as_default() as g:
        with tf.Session().as_default() as sess:
            keras.backend.set_session(sess)
            keras_model = mlflow.sklearn.load_model(keras_model_path)
    #keras_model = mlflow.keras.load_model(keras_model_path)

    savelog_to_file("keras_model:" + str(keras_model))
    return KerasMailClassifierPyfunc(keras_model)

def savelog_to_file(text,console_output="true"):
    if console_output:
        print("savelog_to_file:",text)

    filename = "/tmp/trace.log"
    resultfile = open(filename,'a+')
    resultfile.write(text + "\n")
    resultfile.close()

conda_env_template = """        
name: junkmail
channels:
  - defaults
  - anaconda
dependencies:
  - python=={python_version}
  - keras=={keras_version}  
  - {tf_name}=={tf_version} 
  - pip:    
    - pillow=={pillow_version}
"""