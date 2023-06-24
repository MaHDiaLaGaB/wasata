import logging

from fastapi import Depends
from app.core.config import config
from app.db.models import Users

from app.db.schemas import UserCreate, UserUpdate
from app.db.sessions import UserRepository

logger = logging.getLogger(__name__)


class UserBL:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        # history_repository: HistoryRepository = Depends(),
        # auth0_api: Auth0Api = Depends(),
        # secrets_api: SecretsApi = Depends(),
    ) -> None:
        self.user_repository = user_repository
        # self.history_repository = history_repository
        # self.auth0_api = auth0_api
        # self.secrets_api = secrets_api

    # def process_registration(
    #     self, registration: RegistrationCreate
    # ) -> Tuple[User, bool]:
    #     """
    #     Process registration, returns true if the user was an admin
    #     """
    #     try:
    #         # co-owners will be invited so user will already exist
    #         user = self.user_repository.add_auth0_data_for_user(registration)
    #         return user, False
    #     except ObjectNotFound:
    #         # for company admin a new user has to be created
    #         logging.error(
    #             f"There is no user with email: {registration.email}, creating new user"
    #         )
    #         user = self.create_user(
    #             UserCreate(
    #                 auth_id=registration.auth_id,
    #                 email=registration.email,
    #                 first_name=registration.first_name,
    #                 last_name=registration.last_name,
    #             )
    #         )
    #         return user, True

    def create_user(self, user_create: UserCreate) -> Users:
        """creates an entry in the users-db and a keypair in the secrets-db"""

        # if user with this email exists, just update the auth_id on that user
        # if user_create.email:
        #     try:
        #         user = self.user_repository.get_by_email(user_create.email)
        #         # user.auth_id = user_create.auth_id
        #         return user
        #     except ObjectNotFound:
        #         pass
        user = self.user_repository.get_by_number(user_create.phone_number)
        if user is None:
            user = self.user_repository.create(user_create)

            return user

        # else:
        #     logger.info("the user already exist ...")
        #     user = self.user_repository.update(
        #         user=user,
        #         user_update=UserUpdate(
        #             tokens=user_create.tokens, price=float(config.PRICE)
        #         ),
        #     )
        #
        #     return user
        # if user with this auth id exists, just return it
        # try:
        #     return self.user_repository.get_by_auth_id(user_create.auth_id or "not set")
        # except ObjectNotFound:
        #     pass

        # create a new user

        # account: KeypairGet = self.secrets_api.create_keypair(user_id=user.id)
        # user = self.user_repository.update(user, UserUpdate(address=account.address))
        # self.history_repository.add_platform_joined_event(user)

    # def update_email(self, user: User, update_user_email: UserUpdateEmail) -> User:
    #     # update the email and return updated user object
    #     self.user_repository.update(user, update_user_email)
    #
    #     # update at auth0
    #     self.auth0_api.update_user_email(user.auth_id, update_user_email.email)
    #
    #     # return updated user object
    #     return user
    #
    # def email_verification(self, user: User) -> EmailVerification:
    #
    #     return self.auth0_api.send_verification_email(user.auth_id)
    #
    # def migrate_all_users(self, dry_run: bool) -> Tuple[int, int]:
    #     # get all users from the users-db
    #     users = self.user_repository._get_all(User)  # pylint: disable=protected-access
    #     # call secrets-api migrate endpoint with dryrun path param set to true
    #     records_migrated = 0
    #     skipped = 0
    #     for user in users:
    #         # users created before this pr will have a real private key in the db
    #         # any users that were created after will have a placeholder private key
    #         if user.private_key != PLACEHOLDER_PRIVATE_KEY:
    #             created_account = self.secrets_api.migrate_user_keypair(
    #                 user.id, user.private_key, dry_run
    #             )
    #             assert (
    #                 created_account.address == user.address
    #             ), f"wrong address created for user {user.id}"
    #             records_migrated += 1
    #         else:
    #             skipped += 1
    #     return records_migrated, skipped
