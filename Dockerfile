FROM python:3.11-slim
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install pipenv alembic

# Copy dependency files
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

CMD ["flask", "run", "--host=0.0.0.0"]