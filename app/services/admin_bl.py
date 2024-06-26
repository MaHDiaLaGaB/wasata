import logging
from fastapi import Depends
from db.models import Admins
from db.sessions import AdminRepository
from db.schemas import AdminCreate, AdminUpdate
from cus_exceptions import Forbidden


class AdminBL:
    def __init__(self, admin_repository: AdminRepository = Depends()):
        self.admin_repository = admin_repository

    def create_admin(self, admin_create: AdminCreate = Depends()) -> Admins:
        try:
            # Check if the admin already exists
            existing_admin = self.admin_repository.get(admin_create.username)
            if existing_admin:
                raise ValueError("Admin already exists")

            # Create the admin

            admin = self.admin_repository.create(admin_create)

            return admin
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            # Handle error appropriately

    def update_price_admin(self, secret_key: str, admin_update: AdminUpdate):
        admin = self.admin_repository.get_by_secret(secret_key)
        if not admin:
            raise Forbidden()

        return self.admin_repository.update(admin, admin_update)
