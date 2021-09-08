FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY diva-python/requirements.txt /code/diva_python_requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade cython
RUN pip install -r diva_python_requirements.txt
COPY . /code/
RUN pip list
RUN chmod +x /code/manage.py
