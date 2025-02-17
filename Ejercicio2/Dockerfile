FROM python:3.10

# Create a directory /dev in the container
WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/

# Copy the current directory contents into the container at /dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD [ "python", "manage.py", "runserver"]


