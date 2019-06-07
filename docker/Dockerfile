FROM centos:7.5.1804

RUN yum update -y \
    && yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y python36u python36u-libs python36u-devel python36u-pip \
    && yum install -y which gcc \ 
    && yum install -y openldap-devel  \
    && yum install -y systemd-sysv \
    && yum install -y cronie

# pipenv installation
RUN pip3.6 install pipenv

RUN ln -s /usr/bin/pip3.6 /bin/pip

RUN rm /usr/bin/python
# python must be pointing to python3.6
RUN ln -s /usr/bin/python3.6 /usr/bin/python

RUN pip install --upgrade pip

WORKDIR /app/src

ENV LANG en_US.utf8
ENV LC_ALL en_US.utf8
ENV LC_LANG en_US.utf8
ENV FLASK_APP /app/src/api.py

EXPOSE 5000

CMD [ "/app/docker/entrypoint.sh"]
ENTRYPOINT [ "sh" ]