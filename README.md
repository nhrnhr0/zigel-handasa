# run the server (Terminal 1)
```
cd server/
python -m venv env # create virtual environment
source env/bin/activate # (Linux)
env\Scripts\activate # (Windows)
cd server/
pip install -r requirements.txt
cp .examle-env .env
cp example-db.sqlite3 db.sqlite3
python manage.py migrate
python manage.py runserver
```

# run the client (Terminal 2)
```
cd client/
cp .example-env .env
npm install
npm run dev
```