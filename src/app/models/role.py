from .base import Base
from .mixins import NameMixin


class Role(Base, NameMixin):
    _name_nullable = False
    _name_unique = True
    _name_primary_key = True
