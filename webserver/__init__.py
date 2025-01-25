from pkg_resources import require

from .user import user_blueprint
from .admin import admin_blueprint

dependencies = [
    "flask",
]

require(dependencies)



