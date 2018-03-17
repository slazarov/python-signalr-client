# Use an official Python runtime as a parent image
FROM python:3.6.3-alpine

RUN   apk update && apk add --no-cache --virtual .build-deps \
      g++ make && \
      pip install signalr_client_aio && \
      apk del .build-deps && \
      rm -rf /var/cache/apk/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Run app.py when the container launches
CMD ["python", "-u", "example.py"]
