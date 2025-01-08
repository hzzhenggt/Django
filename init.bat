@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Making migrations...
python manage.py makemigrations
python manage.py makemigrations core
python manage.py makemigrations example

echo Applying migrations...
python manage.py migrate

echo Creating superuser...
call createsuperuser.bat

echo Done!
pause 