FROM python:3.12.9-bookworm

WORKDIR /app
COPY . .

RUN pip install -r requirements_alt

# Expose the Django port
EXPOSE 8000
 
# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
