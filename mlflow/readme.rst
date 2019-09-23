How To Train and Deploy mail Classifier with MLflow and Keras

The example contains the following files:

 * MLproject
   Contains definition of this project. Contains only one entry point to train the model.

 * conda.yaml
   Defines project dependencies. NOTE: You might want to change tensorflow package to tensorflow-gpu
   if you have gpu(s) available.

 * train.py
   Main entry point of the projects. Handles command line arguments and possibly downloads the
   dataset.

 * score_mail_rest.py
   Score a mail or a directory of mailss using a model deployed to a REST endpoint.
   
Running this Example
To train the model, run the example as a standard MLflow project:

enter the "/root/mlflow" folder
run the "mlflow run junkmail"

The console will output below text if the mlflow successfully for example:
...
2019/08/22 07:01:50 INFO mlflow.projects: === Run (ID 'aaffce263fdb4fe29482922ae9f3f1e8') succeeded ===

To test your model, run the included scoring scripts. For example, say your model was trained with
run_id ``101``.

- To test REST api scoring do the following two steps:

  1. Deploy the model as a local REST endpoint by running ``mlflow models serve``:

  .. code-block:: bash

      # deploy the model to local REST api endpoint
      mlflow models serve --model-uri runs:/aaffce263fdb4fe29482922ae9f3f1e8/model --port 54321
Note: make sure the "anaconda3" is in your PATH, for example, run "export PATH=$PATH:/usr/local/anaconda3/bin/" before run the "mlflow models serve"

	There isn't exception or error after run the "mlflow models serve"

2. Apply the model to new data using the provided score_mail_rest.py script:

  .. code-block:: bash

      # score the deployed model
      python  python score_mail_rest.py

