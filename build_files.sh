
python3.12 -m venv env
source env/bin/activate
python3.12 -m pip install --upgrade pip
pip3 install -r requirements.txt
python3.12 install python-dotenv
#python3.12 manage.py collectstatic --noinput