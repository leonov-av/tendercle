FROM python:alpine3.7

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "tendercle.py" ]
