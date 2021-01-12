FROM registry.access.redhat.com/ubi8/python-36

USER 0

ADD . /mocks
WORKDIR /mocks
RUN pip3 install --no-cache --upgrade pip setuptools .

EXPOSE 8080

USER 1001

CMD ["start_crcmocks"]
