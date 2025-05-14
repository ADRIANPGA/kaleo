# This file makes 'v1' a subpackage 

# Import the API implementation classes to ensure they are registered
# with their respective base classes from kaleo_core_api_server.apis

from .login import LoginApiImpl
from .register import RegisterApiImpl
from .users import UsersApiImpl

# Ensure all are loaded for subclass registration by BaseDefaultApi and its variants
__all__ = ['LoginApiImpl', 'RegisterApiImpl', 'UsersApiImpl']

print("kaleo_core.api.v1.__init__.py updated to import API implementations.") 