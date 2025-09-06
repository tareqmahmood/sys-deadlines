podman run --rm -it \
  -p 4000:4000 \
  -v "$PWD:/srv/jekyll:z" \
  -v "$PWD/vendor/bundle:/usr/local/bundle:z" \
  docker.io/jekyll/jekyll:latest \
  jekyll serve --watch --host 0.0.0.0