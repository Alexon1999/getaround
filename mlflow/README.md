# MLFlow

MLFlow Helps you track all of your ML experiments

With MLFlow, you will be able to: 

- Monitor your models : Track your ML Trainings, metrics and parameters via a very nice UI,
- Standardize your training process to outsource it on any machine,
- Deploy your models on any technologies. 

## Local
``` 
$ docker build -t getaround-mlflow-server .

If, for some reason, your image is not working use Jedha's image jedha/sample-mlflow-server or if you have Apple M1 chips try this
$ docker buildx build --platform linux/amd64 -t getaround-mlflow-server .

# run a container
$ docker run -it\
 -p 4000:4000\
 -v "$(pwd):/home/app"\
 -e PORT=4000\
 -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 -e BACKEND_STORE_URI=$BACKEND_STORE_URI\
 -e ARTIFACT_ROOT=$ARTIFACT_ROOT\
 getaround-mlflow-server

# overrides the entrypoint command to execute the script train.py
$ ./run.sh
```

## Troubleshooting 

👋 **Make sure that you exported your personal environment variables on your local terminal**. Especially, you need:

* `MLFLOW_TRACKING_URI`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `BACKEND_STORE_URI`
* `ARTIFACT_ROOT`

Our advice is to create a `secrets.sh` file containing:

```bash
export MLFLOW_TRACKING_URI="REPLACE_WITH_YOUR_MLFLOW_TRACKING_URI";
export AWS_ACCESS_KEY_ID="REPLACE_WITH_YOUR_AWS_ACCESS_KEY_ID";
export AWS_SECRET_ACCESS_KEY="REPLACE_WITH_YOUR_AWS_SECRET_ACCESS_KEY";
export BACKEND_STORE_URI="REPLACE_WITH_YOUR_BACKEND_STORE_URI";
export ARTIFACT_ROOT="REPLACE_WITH_YOUR_ARTIFACT_ROOT";
```

You can then simply run `source secrets.sh` to export all your environmnet variables at once. 


# Deployment on Heroku
```
# Login to your console
$ heroku login

# Log in to Container Registry
$ heroku container:login

# Create a Heroku app
$ heroku create mlflow-server

# Create Docker image with Dockerfile
$ docker build -t getaround-mlflow-server .
$ docker tag getaround-mlflow-server web

# Push to heroku registry
$ heroku container:push web -a mlflow-server

# Release the newly pushed images to deploy your app
$ heroku container:release web -a mlflow-server

# Check out heroku logs
$ heroku logs --tail -a mlflow-server

# For Apple M1 chips
The above process might not work because, as of today, Apple M1 Chips don't build images based on the same linux architecture as normal computers (M1 chips build images based on linux arm64 architecture whereas normal computers build images based on linux amd64 architecture).

# Force image creation with `amd64` architecture with the following command
$ docker buildx build --platform linux/amd64 -t web .
$ docker tag web registry.heroku.com/mlflow-server/web
$ docker push registry.heroku.com/mlflow-server/web
$ heroku container:release web -a mlflow-server
```