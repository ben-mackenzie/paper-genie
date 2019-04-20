# base image
FROM python:2

# set working directory
WORKDIR /usr/src/app

COPY requirements.txt .
COPY app.py .
COPY genes/ ./genes/
COPY ml/ ./ml
COPY api/ ./api
COPY datasets/testing/ ./datasets/testing/
COPY datasets/training/ ./datasets/training/

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt averaged_perceptron_tagger universal_tagset

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
#CMD ["python", "./app.py"]
