git pull
cd server/
source env/bin/activate
cd server/
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart gunicornZigel
