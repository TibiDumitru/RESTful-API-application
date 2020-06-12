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



1. CRUD

    Product table was added in mydb.db database - SQLAlchemy
    
    API contains functions to see all products or a specific one, to add, delete
    or update specific products
    
    
    
2. Authentication

    User table also added in mydb.db
    
    User fields are Id, Name, Password, Admin
    
    An admin user can see all accounts, delete or add accounts
    
    Passwords are hashed
    
    Login is Basic and a token is needed - x-access-token with the value = token
   
   
   
3. Rate limit

    Number of requests is limited (per hour) - Limiter from flask_limiter
    
    