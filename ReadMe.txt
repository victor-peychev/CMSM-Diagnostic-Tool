To run

source virt/Scripts/activate

export FLASK_ENV=development

export FLASK_APP=server.py

flask run


To migrate 

flask db migrate -m''

flask db upgrade



