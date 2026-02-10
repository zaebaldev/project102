import asyncio
import logging

from app.auth.utils import hash_password
from app.db.db_helper import db_helper
from app.models.role import Role
from app.models.user import User
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from core.config import settings
from core.enums.roles import RolesEnum

log = logging.getLogger(__name__)


async def create_roles() -> None:
    async with db_helper.session_factory() as session:
        role_repo = RoleRepository(
            session=session,
            model=Role,
        )

        existing_roles = await role_repo.get_all()
        existing_role_names = {role.name for role in existing_roles}

        roles_to_add = []
        for role_enum in RolesEnum:
            if role_enum.value not in existing_role_names:
                roles_to_add.append(Role(name=role_enum.value))

        if roles_to_add:
            await role_repo.add_many(roles_to_add)
            await session.commit()
            log.info(f"Added {len(roles_to_add)} new roles")
        else:
            log.info("All roles already exist, skipping role creation")

    await db_helper.dispose()


async def create_first_admin() -> None:
    async with db_helper.session_factory() as session:
        user_repo = UserRepository(
            session=session,
            model=User,
        )

        existing_admin = await user_repo.get_by_phone(
            phone_number=settings.first_admin.phone_number
        )

        if existing_admin is not None:
            log.info(
                f"Admin user with phone number {settings.first_admin.phone_number} already exists, skipping creation"
            )
            return

        hashed_password = hash_password(password=settings.first_admin.password)
        admin_create = User(
            hashed_password=hashed_password,
            phone_number=settings.first_admin.phone_number,
            full_name=settings.first_admin.full_name,
            role=RolesEnum.ADMIN.value,
        )
        await user_repo.add(admin_create)
        await session.commit()
        log.info(
            f"Created admin user with phone number {settings.first_admin.phone_number}"
        )

    await db_helper.dispose()


async def main() -> None:
    await create_roles()
    await create_first_admin()


if __name__ == "__main__":
    asyncio.run(main())
