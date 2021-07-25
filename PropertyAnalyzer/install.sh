echo '-----------------------------Installation started------------------------'
echo '-----------------------------Install sqlite3-----------------------------'
sudo apt install sqlite3
echo '----------------------------- sqlite3 successfully installed ------------'
echo '-----------------------------Install dependencies-----------------------------'
pip3 install -r requirements.txt
echo '----------------------------- Dependencies successfully installed ------------'
echo '---------------------------- running migrations -------------------------'
python3 manage.py makemigrations
echo '----------------------------completed migrations--------------------------'
echo '----------------------------starting server------------------------------ '
python3 manage.py runserver
