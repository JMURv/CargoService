FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate && \
    poetry run python manage.py load_initial_data ./api/management/files/uszips.csv && \
    poetry run python manage.py runserver 0.0.0.0:8000
