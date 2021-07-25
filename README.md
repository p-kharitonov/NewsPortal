<h1>Проект NewsPortal</h1>
<hr>
<p>sudo apt install python3-pip</p>
<p>pip3 install -r requirements.txt</p>
<hr>
<p>sudo add-apt-repository ppa:redislabs/redis</p>
<p>sudo apt-get update</p>
<p>sudo apt-get install redis</p>
<hr>
<p>pip3 install -U "celery[redis]"</p>
<p>redis-server</p>
<hr>
<p>celery -A mcdonalds worker -l INFO -B</p>
<hr>
<p>python3 manage.py makemigrations</p>
<p>python3 manage.py migrate</p>
<p>python3 manage.py createsuperuser</p>
<hr>
<p>python3 manage.py runserver</p>
