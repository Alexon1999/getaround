docker run -it\
 -p 4000:4000\
 -v "$(pwd):/home/app"\
 -e PORT=4000\
 -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 -e BACKEND_STORE_URI=$BACKEND_STORE_URI\
 -e ARTIFACT_ROOT=$ARTIFACT_ROOT\
 getaround-mlflow-server python train.py
 #jedha/sample-mlflow-server python train.py