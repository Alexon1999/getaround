# Run Container on Local Environment
```
$ docker build -t getaround-dashboard .

$ docker run -it -p 4000:4000 -v "$(pwd):/app" -e PORT=4000 getaround-dashboard
```

# Deployment on Heroku
```
# Login to your console
$ heroku login

# Log in to Container Registry
$ heroku container:login

# Create a Heroku app
$ heroku create getaround-web-dashboard

# Create Docker image with Dockerfile
$ docker build -t getaround-dashboard .
$ docker tag getaround-dashboard web

# Push to heroku registry
$ heroku container:push web -a getaround-web-dashboard

# Release the newly pushed images to deploy your app
$ heroku container:release web -a getaround-web-dashboard

# Check out heroku logs
$ heroku logs --tail -a getaround-web-dashboard

# For Apple M1 chips
$ docker buildx build --platform linux/amd64 -t web .
$ docker tag web registry.heroku.com/getaround-web-dashboard/web
$ docker push registry.heroku.com/getaround-web-dashboard/web
$ heroku container:release web -a getaround-web-dashboard
```