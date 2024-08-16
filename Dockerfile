# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code

ENV OPENAI_API_KEY "ENTER YOUR API KEY"

# 
# CMD ["fastapi", "dev", "app.py"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]