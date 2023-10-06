FROM python:3.10-bullseye

# work directory (mapped from host))
WORKDIR /app

# install python
RUN apt -y update
RUN apt -y install python3 python3-pip

# copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# expose port
EXPOSE 5000

# ENTRYPOINT[] could be used insted of CMD[]. The latter allows default parameter overriding.
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000", "--reload"] 

