FROM tomcat:7
RUN wget --no-check-certificate -O /usr/local/tomcat/webapps/blacktop3.war https://dataavenue.s3.lpds.sztaki.hu/blacktop3.war
RUN rm -fr /usr/local/tomcat/webapps/ROOT
ENV IP=sql_ip_cime
COPY start.sh /
ENTRYPOINT ["/start.sh", $IP]
EXPOSE 8080

