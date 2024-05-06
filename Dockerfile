FROM python:3.11-alpine3.19

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN apk add --update --no-cache postgresql-client build-base postgresql-dev

RUN pip install --upgrade pip -r /app/requirements.txt  # Install dependencies directly

COPY ./scripts /scripts
RUN chmod -R =x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

COPY ./app /app

WORKDIR /app

EXPOSE 80
CMD ["/scripts/run.sh"]