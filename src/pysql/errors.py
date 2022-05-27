class PySQLException(Exception):
    def __init__(self, base):
        self.message = str(base)

    def __str__(self):
        return self.message
