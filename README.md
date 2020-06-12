# RESTful-API-application 
# Python 3 - Flask
RESTful API application that exposes an endpoint to manage a catalog product.
The product fields are Id, Name, Price, Category, CreatedDate, UpdatedDate.

  + flask
  + flask_sqlalchemy - for persistent data management
  + werkzeug.security - hash password
  + jwt - for authorization (encode id -> token)
  + flask_limiter - for rate limit

  Python Console
  
  ->> from api import db
  
  ->> db.create_all()
  
  => creates the tables - mydb.db file (the database which contains the needed tables)


  Terminal (CMD)
  
  set FLASK_APP=api
  
  set FLASK_DEBUG=1
  
  flask run



