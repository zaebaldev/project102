from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class IntIdMixin:
    _id_primary_key: bool = True
    _id_autoincrement: bool = True

    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(
            primary_key=cls._id_primary_key,
            autoincrement=cls._id_autoincrement,
        )
