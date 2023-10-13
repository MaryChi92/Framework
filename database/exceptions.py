class IntegrityError(Exception):
    def __init__(self, message):
        super().__init__(f'Database Integrity Error: {message}')