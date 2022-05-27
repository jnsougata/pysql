from src.pysql import PySQL, Types, Field, Condition

db = PySQL('root.db')
db.show('albums')
