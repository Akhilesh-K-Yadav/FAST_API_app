from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_pwd(passwd: str):
    return pwd_context.hash(passwd)

def verify(passwd, hashed_passwd):
    return pwd_context.verify(passwd, hashed_passwd)
        


