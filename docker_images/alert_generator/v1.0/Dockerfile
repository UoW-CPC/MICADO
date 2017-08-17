FROM ubuntu:16.04
RUN apt-get update \
  && apt-get install -y wget curl jq \
  && rm -rf /var/lib/apt/lists/*

CMD ./etc/prometheus/alert_generator.sh

