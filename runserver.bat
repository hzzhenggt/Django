@echo off
chcp 65001
set port=8000
explorer http://localhost:%port%
python manage.py runserver 0.0.0.0:%port%
pause