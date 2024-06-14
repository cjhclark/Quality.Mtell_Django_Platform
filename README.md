Build:

pscp -r C:\pyproject\mtell-test  root@10.148.69.74:/root/django/
docker build -t django-app .
docker run -d --name my-django-container -p 8001:8000 django-app

Create new Django:

python3 -m venv myenv
pip install Django
django-admin startproject my_project
python manage.py runserver
python manage.py makemigrations
python manage.py migrate 
python manage.py createsuperuser --username=admin --email=youremail@qq.com 


