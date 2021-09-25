FROM python:3.8

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src
CMD python app.py