class JWTSettings:
    SECRET_KEY = "123"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

class DB:
    INDEX_COLUMNS = ['pais', 'control']