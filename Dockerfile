FROM python:rc
RUN pip install -U pip

COPY requirements.txt /kpl/
RUN pip install -r /kpl/requirements.txt

COPY kpl /kpl/kpl
COPY setup.py /kpl/
RUN pip install -e /kpl

WORKDIR /kpl/kpl

EXPOSE 80
# CMD [ "/usr/local/bin/python3", "/usr/local/bin/kpl" ]
CMD [ "/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload" ]
