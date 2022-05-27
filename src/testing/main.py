from src.pysql import PySQL, Types, Field, Condition

db = PySQL('root.db')
db.insert(
    'users',
    [
        Field('id', 100),
        Field('age', 22),
        Field('name'),

    ]
)
data = db.select('users', ['id', 'name', 'age'], order_by=['age', 'id'])
print(data)
