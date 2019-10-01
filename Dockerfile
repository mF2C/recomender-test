FROM python:3.7
ADD . /recommender
WORKDIR /recommender
RUN bash -c "pip install -r requirements.txt"

CMD ["python", "-u", "recommender-test.py"]