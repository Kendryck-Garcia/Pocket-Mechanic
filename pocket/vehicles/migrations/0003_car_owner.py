from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_existing_cars(apps, schema_editor):
    """Give pre-existing cars to the first superuser (or, failing that, the first user).

    Before this migration every car was visible to every account, so there is no
    record of who created what. Handing them to the admin keeps the data without
    leaking it to regular users; the admin can reassign cars in /admin. If the
    database has no users at all, nobody could have created those cars through
    the app, so they are dropped rather than left ownerless.
    """
    Car = apps.get_model("vehicles", "Car")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    orphans = Car.objects.filter(owner__isnull=True)
    if not orphans.exists():
        return
    owner = (
        User.objects.filter(is_superuser=True).order_by("id").first()
        or User.objects.order_by("id").first()
    )
    if owner is None:
        orphans.delete()
    else:
        orphans.update(owner=owner)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vehicles", "0002_part_part_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_existing_cars, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="car",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
