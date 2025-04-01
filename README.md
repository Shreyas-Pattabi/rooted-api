# Backend Setup

# Start by creating database
brew install postgresql (If not already installed)

# Log in and follow the following steps
psql -U postgres

CREATE DATABASE (database-name);
CREATE USER (user-name) WITH PASSWORD (password);
GRANT ALL PRIVILEGES ON DATABASE (database-name) TO (user-name);

\q

psql -U (user-name) -d (database-name)

# In the .env file replace the following lines
DATABASE_URL="postgresql+asyncpg://(user-name):(password)@localhost:5432/(database-name)"

# Cd into backend folder, create virtual environment
python -m venv .venv

# Install requirements
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload