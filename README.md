# ABOUT
This REST API allows users to upload a 1-page PDF file and returns a summarized version of its content using the OpenAI API.

# How to run
- create an `backend/.env` file with fields from `backend/.env.example` file
- `docker compose up --build`
- `docker compose exec web python manage.py migrate`
- go to [localhost:8000](http://localhost:8000/)

# How to use
Go to [http://localhost:8000/swagger/](http://localhost:8000/swagger/) -> click on `/summarize/` endpoint -> Try It out -> upload `file_test.pdf` -> Execute

# How to run Tests
