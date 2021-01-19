FROM registry.access.redhat.com/ubi8/python-36

USER 0


ENV OC_VERSION "v3.11.0"
ENV OC_RELEASE "openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit"

# install the oc client tools
ADD https://github.com/openshift/origin/releases/download/$OC_VERSION/$OC_RELEASE.tar.gz /opt/oc/release.tar.gz
RUN tar --strip-components=1 -xzvf  /opt/oc/release.tar.gz -C /opt/oc/ && \
    mv /opt/oc/oc /usr/bin/ && \
    rm -rf /opt/oc

ADD . /mocks
WORKDIR /mocks
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install --no-cache .

EXPOSE 8080

USER 1001

CMD ["start_crcmocks"]
