FROM python:3
ADD . /mocks
WORKDIR /mocks
RUN pip3 install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "run.sh"]
