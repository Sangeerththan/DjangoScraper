echo '-----------------------------Property Analyzer Installation started-------------------------'
echo '-----------------------------Install sqlite3------------------------------------------------'
sudo apt install sqlite3
echo '----------------------------- sqlite3 successfully installed -------------------------------'
echo '-----------------------------Install dependencies-------------------------------------------'
pip3 install -r requirements.txt
echo '----------------------------- Dependencies successfully installed --------------------------'
echo '---------------------------- Running migrations --------------------------------------------'
python3 manage.py makemigrations
python3 manage.py migrate
echo '----------------------------Completed migrations--------------------------------------------'
echo '-------Installation completed succcessfully and server is about to start--------------------'
echo '----------------------------starting server-------------------------------------------------'
python3 manage.py runserver
