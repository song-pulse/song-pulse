from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase(object):
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


Base = declarative_base(cls=CustomBase)
