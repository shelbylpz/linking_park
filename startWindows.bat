REM clone repo
git clone https://github.com/shelbylpz/linking_park.git
cd linking_park

REM Create env and install requirements
python -m venv venv
venv\bin\activate
pip install -r requirements.txt

REM Run app
python app/__init__.py