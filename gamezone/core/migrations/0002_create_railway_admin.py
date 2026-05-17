from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import migrations


def create_or_upgrade_admin(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)

    user, created = User.objects.get_or_create(
        username="Pratham",
        defaults={
            "email": "",
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
            "password": make_password("Immortal@12"),
        },
    )

    changed = created
    if not user.is_staff:
        user.is_staff = True
        changed = True
    if not user.is_superuser:
        user.is_superuser = True
        changed = True
    if not user.is_active:
        user.is_active = True
        changed = True

    if not check_password("Immortal@12", user.password):
        user.password = make_password("Immortal@12")
        changed = True

    if changed:
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_or_upgrade_admin, migrations.RunPython.noop),
    ]
