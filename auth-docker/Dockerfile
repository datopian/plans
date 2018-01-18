FROM datopian/auth:external-providers

ADD . /ext/plans/

USER root
RUN pip3 install /ext/plans

ENV ALLOWED_SERVICES=source:plans;rawstore:plans

USER $GUNICORN_USER