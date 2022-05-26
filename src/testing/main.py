from src.pysql import PySQL, Types, Field, Condition

db = PySQL('root.db')
data = db.select('users', ['id', 'name', 'age'], condition=Condition.not_equal('name', 'John'))
print(data)
