# Fast API

### Dockerizing fastapi application
``` 
$ docker build -t getaround-api .

$ source run.sh
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
export MLFLOW_EXPERIMENT_NAME="REPLACE_WITH_YOUR_MLFLOW_EXPERIMENT_NAME";
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
$ heroku create getaround-ml-api

# Create Docker image with Dockerfile
$ docker build -t getaround-api .
$ docker tag getaround-api web

# Push to heroku registry
$ heroku container:push web -a getaround-ml-api

# Release the newly pushed images to deploy your app
$ heroku container:release web -a getaround-ml-api

# Check out heroku logs
$ heroku logs --tail -a getaround-ml-api

# For Apple M1 chips
The above process might not work because, as of today, Apple M1 Chips don't build images based on the same linux architecture as normal computers (M1 chips build images based on linux arm64 architecture whereas normal computers build images based on linux amd64 architecture).

# Force image creation with `amd64` architecture with the following command
$ docker buildx build --platform linux/amd64 -t web .
$ docker tag web registry.heroku.com/getaround-ml-api/web
$ docker push registry.heroku.com/getaround-ml-api/web
$ heroku container:release web -a getaround-ml-api
```