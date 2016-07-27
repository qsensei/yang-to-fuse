FROM ubuntu:14.04
COPY . /target
WORKDIR /target
RUN apt-get update && \
  apt-get install -y python python-pip && \
  rm -rf /var/lib/apt/lists/* && \
  pip install -r requirements.docker.txt && \
  rm -r dist requirements.docker.txt
ENTRYPOINT ["pyang", "--plugindir", "/target/plugins", "-f", "qsensei-fuse"]
