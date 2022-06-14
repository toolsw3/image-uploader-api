FROM python:3.7-alpine
WORKDIR /project
ADD . /project
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir temp
CMD ["python3", "app.py"]
