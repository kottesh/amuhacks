from typing import Any
from sqlalchemy.orm import declared_attr, declarative_base

class CustomBase:
    """
    Custom base class for SQLAlchemy models to automatically generate table names.
    """
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        if not name.endswith('s'):
            name += 's'
        return name

# Create the base using the custom class
Base = declarative_base(cls=CustomBase)
