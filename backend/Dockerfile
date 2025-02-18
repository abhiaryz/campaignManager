FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x /app/entrypoint.sh
EXPOSE 80
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "dsp.wsgi:application", "--bind", "0.0.0.0:80"]
