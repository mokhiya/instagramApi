FROM python:3.11.7-alpine3.19
LABEL maintainer="instagramAPI"

ENV PYTHONUNBUFFARED=1
COPY ./requirements.txt /app/requirements.txt
RUN python -m venv /venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install -r /app/requirements.txt && \
    adduser --disabled-password --gecos "" django-user  && \
    chown -R django-user /app

COPY ./ /app
WORKDIR /app

USER django-user

ENV PATH="/venv/bin:$PATH"

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0.8000"]