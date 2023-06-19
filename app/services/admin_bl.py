from fastapi import Depends
from app.db.models import Admins
from app.db.sessions import AdminRepository
from app.db.schemas import AdminCreate


class AdminBL:
    def __init__(self, admin_repository: AdminRepository = Depends()):
        self.admin_repository = admin_repository

    def create_admin(self, admin_data: AdminCreate) -> Admins:
        # Check if the admin already exists
        existing_admin = self.admin_repository.get(admin_data.username)
        if existing_admin:
            raise ValueError("Admin already exists")

        # Create the admin

        admin = self.admin_repository.create(admin_data)

        return admin
