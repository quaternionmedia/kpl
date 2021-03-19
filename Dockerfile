FROM python:rc-slim
RUN pip install -U pip

COPY kpl /kpl/kpl
COPY setup.py /kpl/

RUN pip install -e /kpl

EXPOSE 80
CMD [ "/usr/local/bin/python3", "/usr/local/bin/kpl" ]
# CMD bash kpl