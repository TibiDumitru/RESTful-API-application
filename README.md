# RESTful-API-application 
# Python 3 - Flask
RESTful API application that exposes an endpoint to manage a catalog product.
The product fields are Id, Name, Price, Category, CreatedDate, UpdatedDate.

  + flask
  + flask_sqlalchemy - for persistent data management
  + jwt - for authorization (encode id -> token)

  Python Console
  
  ->> from api import db
  
  ->> db.create_all()
  
  => creates the tables - mydb.db file (the database which contains the needed tables)


  Terminal (CMD)
  
  set FLASK_APP=api
  
  flask run



