# Framework (WSGI)

FOLLOW THESE STEPS TO START THE APP
  1. Create and activate the virtual environment:  
       `python -m venv venv_name`  
       `venv\Scripts\activate.bat` - for Windows  
       `source venv/bin/activate` - for Linux & MacOS  
  2. Install the requirements:  
       `pip install -r requirements.txt`
  3. Launch gunicorn:  
       `gunicorn run:app -b 0.0.0.0:8080`
