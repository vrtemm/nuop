FROM ubuntu:20.04

RUN apt-get update --fix-missing && apt-get install -y openjdk-11-jdk wget

RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1-src.tar.gz \
    && tar -xzvf hadoop-3.4.1-src.tar.gz \
    && mv hadoop-3.4.1-src /usr/local/hadoop \
    && rm hadoop-3.4.1-src.tar.gz

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pandas scikit-learn nltk numpy


ADD spamtask.py /app/
ADD spam.csv /app/

WORKDIR /app

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc \
    && echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc \
    && echo 'export PATH=$PATH:/usr/local/hadoop/bin:/usr/local/hadoop/sbin' >> ~/.bashrc

CMD ["python3", "spamtask.py"]
