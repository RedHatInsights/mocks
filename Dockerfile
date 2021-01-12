FROM registry.access.redhat.com/ubi8/python-36

ADD . /mocks
WORKDIR /mocks
RUN pip3 install .

EXPOSE 8080

CMD ["start_crcmocks"]
