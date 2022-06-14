FROM python:3.6.1-alpine
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
RUN mkdir temp
CMD ["python3", "app.py"]