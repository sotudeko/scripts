FROM jenkins
MAINTAINER Sola Otudeko (sotudeko@sonatype.com)
RUN cd /var/tmp && wget https://archive.apache.org/dist/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz
RUN cd /var/tmp && tar xvf apache-maven-3.5.2-bin.tar.gz
ENV PATH="/var/tmp/apache-maven-3.5.2/bin:${PATH}"
