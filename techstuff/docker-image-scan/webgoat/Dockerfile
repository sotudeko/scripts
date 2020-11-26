FROM openjdk:8-jre
VOLUME /tmp
RUN cd /root; mkdir -p webgoat
ADD WebGoat-1.2.4.war webgoat.war
RUN sh -c 'touch /webgoat.war'
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/webgoat.war"]

