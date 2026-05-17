import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a superuser from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "").strip()

        if not username or not password:
            self.stdout.write(
                "Skipping superuser setup because DJANGO_SUPERUSER_USERNAME or "
                "DJANGO_SUPERUSER_PASSWORD is not set."
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        updated = False
        if email and user.email != email:
            user.email = email
            updated = True

        if not user.is_staff:
            user.is_staff = True
            updated = True

        if not user.is_superuser:
            user.is_superuser = True
            updated = True

        if created or not user.check_password(password):
            user.set_password(password)
            updated = True

        if updated:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' is ready"))
