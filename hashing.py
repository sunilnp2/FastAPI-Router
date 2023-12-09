from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def password_hash(password):
    return pwd_context.hash(password)

def verify_hashed_password(db_password, user_password):
    return pwd_context.verify(db_password, user_password)