# app/models/__init__.py

"""
Models Package
Import all models here so they can be easily accessed.
"""

from app.models.user import User, UserRole

# This allows us to do: from app.models import User
# Instead of: from app.models.user import User