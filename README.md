[What is Microblog]

    A tutorial that uses the building of a blog application to facilitate learning the
    Flask framework [ http://flask.pocoo.org/docs/1.0/ ]. 
    
[How can I run & play around with this application?]

Pre-requisites: 

You will need to open a terminal for these steps.

* Install Git: https://git-scm.com/

* Install Python 3: https://www.python.org/ 
This application uses Python 3.6.7

* Please install pipenv: https://pipenv.readthedocs.io/en/latest/ 

* Clone this github repository into the directory you just made. Your directory structure should look like - 
    microblog/
        [*.py, *.db, notes, Pipfile, Pipfile.lock, README.md]
        microblog_app/
            templates/
                [html & text files are here]
        migrations/
            [don't touch this]
            
* Navigate to the directory you just cloned and type <code>cd flask-microblog</code>
* Setup the virtual environment. Type <code>pipenv install</code>
* Enter the virtual environment. Type <code>pipenv shell</code>
* Set your environment variables: <code>export FLASK_APP=microblog.py</code> then <code>export FLASK_ENV=development</code>

Now type <code>flask run</code>

You should now be able to access the application by pasting the following into your browser: <code>127.0.0.1:5000</code>
            
