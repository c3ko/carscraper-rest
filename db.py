"""
    A single engine is created for use in all other files/modules
"""
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
from settings import DB_URI

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# engine = create_engine(DB_URI)
# Session = sessionmaker(bind=engine, convert_unicode=True)
# mysession = scoped_session(Session)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
#To get rid of warning messages
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Bind declaritive base to engine
db.Model.metadata.reflect(db.engine)