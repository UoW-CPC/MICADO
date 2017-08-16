FROM ubuntu:16.04
RUN apt-get update \
  && apt-get install -y wget curl jq \
  && wget https://github.com/occopus/docs/raw/devel/tutorial/autoscaling-dataavenue/deploy/prometheus/executor -O /root/executor \
  && chmod 777 /root/executor \
  && rm -rf /var/lib/apt/lists/*


# Expose the application on port 9095
EXPOSE 9095
#ADD conf.sh /etc/prometheus_executor/conf.sh
#RUN chmod 777 /etc/prometheus_executor/conf.sh
# Set the entry point of the container to the bee command that runs the
# application and watches for changes


CMD ./root/executor -l :9095 ./etc/prometheus_executor/conf.sh

