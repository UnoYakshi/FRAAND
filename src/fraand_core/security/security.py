"""Ductape solution based on https://fastapi.tiangolo.com/tutorial/security/get-current-user/."""

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.fraand_core.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

fake_users_db = {
    'johndoe': {
        'username': 'johndoe',
        'full_name': 'John Doe',
        'email': 'johndoe@example.com',
        'hashed_password': b'$2b$12$lfMBRaQ.9O0anlUrZtNIVu3f6jU8ooXNLJ0TfMeRSZVUa74jlGMZS',
        'disabled': False,
    },
    'alice': {
        'username': 'alice',
        'full_name': 'Alice Wonderson',
        'email': 'alice@example.com',
        'hashed_password': 'fakehashedsecret2',
        'disabled': True,
    },
}
fake_salt = b'$2b$12$lfMBRaQ.9O0anlUrZtNIVu'


def decode_token(token: str) -> User:
    """WIP: Fakes decoding a token..."""
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect token (empty)')
    return User(username=f'{token}__fakedecoded', email='john@example.com', full_name='John Doe')


def hash_password(password: str) -> bytes:
    """Fakes password hashing..."""
    from bcrypt import hashpw

    return hashpw(password.encode('utf-8'), fake_salt)
