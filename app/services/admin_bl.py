from fastapi import Depends
from app.db.models import Admin
from app.exceptions import BadRequest
from app.db.sessions import AdminRepository
from cryptography.fernet import Fernet
from app.db.schemas import AdminCreate
from werkzeug.security import generate_password_hash


class AdminBL:
    def __init__(self, admin_repository: AdminRepository = Depends()) -> None:
        self.admin_repository = admin_repository

    @staticmethod
    # TODO add this logic in the makefile
    def generate_privet_key():
        privet_secret_key = Fernet.generate_key()
        return privet_secret_key

    def create_admin(self, admin_create: AdminCreate) -> Admin:
        admin = self.admin_repository.get_by_email(admin_create.admin_email)
        if admin is None:
            hashed_password = generate_password_hash(admin_create.admin_password)
            admin_create.admin_password = hashed_password
            admin = self.admin_repository.create(admin_create)
            return admin
        else:
            raise BadRequest()
