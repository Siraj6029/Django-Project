from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser
from user.models import CustomUser
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Create token for a user"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("username", type=str, help="Username for the user")

    def handle(self, *args: Any, **options: Any) -> str | None:
        username = options["username"]
        user = CustomUser.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        self.stdout.write(f"Token for user {username}: {token.key}")
