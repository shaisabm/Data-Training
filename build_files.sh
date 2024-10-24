
python3.9 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3.9 -m pip install Django
python3.9 manage.py collectstatic --noinput