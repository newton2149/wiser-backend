# Start with a base image that includes conda
FROM continuumio/miniconda3

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN conda install -y python=3.11.0


# Copy your project code into the container
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py"]
