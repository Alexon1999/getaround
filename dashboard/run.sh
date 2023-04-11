docker build -t getaround/dashboard .

docker run -it\
  -p 4000:4000\
  -v "$(pwd):/app"\
  -e PORT=4000\
  getaround/dashboard