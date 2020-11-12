FROM python:3
ADD . /mocks
WORKDIR /mocks
RUN pip3 install .

EXPOSE 8080

CMD ["start_crcmocks"]
