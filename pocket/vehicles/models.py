from django.db import models


class Car(models.Model):
    nickname = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=4)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Part(models.Model):
    CATEGORY_CHOICES = [
        ("maintenance", "Maintenance"),
        ("accessories", "Accessories"),
        ("mods", "Modifications"),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="maintenance"
    )

    def __str__(self):
        return f"{self.part_name} ({self.get_category_display()})"
