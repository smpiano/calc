docker run --rm -ti \
  -e DISPLAY \
  -v $PWD:/opt/project \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --user="$(id --user):$(id --group)" \
  smpiano/calc:0.0.1 \
  python ./src/calc.py
