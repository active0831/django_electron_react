call setpath.bat

xcopy %SOURCE_DIR%\electron-react-boilerplate-dj %PROGRAM_DIR% /eY

cd %PROGRAM_DIR%
call npm install
cd %cPath%

tar -zxvf %SOURCE_DIR%\python-3.10.11-embed-amd64-pip.tar -C "%cPath%"
xcopy %SOURCE_DIR%\DRF_Generic_v23.02 %PROGRAM_DIR%\backend\ /eY

python %PYTHON_DIR%\get-pip.py
pip install --upgrade pip
pip install virtualenv
python -m virtualenv --copies %PYTHON_VENV_DIR%
call %PYTHON_VENV_DIR%\Scripts\activate.bat

pip install django djangorestframework django-cors-headers
pip install pillow django-storages boto3
pip install dj_rest_auth
pip install django-allauth
pip install djangorestframework-simplejwt
pip install psutil

python %PROGRAM_DIR%\backend\manage.py makemigrations
python %PROGRAM_DIR%\backend\manage.py migrate
python %PROGRAM_DIR%\backend\manage.py createsuperuser

