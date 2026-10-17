import sys
from copy import copy
from unittest import mock

from django.contrib.auth.models import User
from django.template.context import BaseContext
from django.test import TestCase
from django.urls import reverse

from .models import Car, Part

# Django 4.2 predates Python 3.14, where BaseContext.__copy__'s copy(super())
# breaks and the test client crashes on every rendered template. Mirror the
# fix Django shipped in 5.x until the project moves off 4.2.
if sys.version_info >= (3, 14):
    def _base_context_copy(self):
        duplicate = BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.__dict__ = copy(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    BaseContext.__copy__ = _base_context_copy


class OwnerIsolationTests(TestCase):
    """A signed-in user only ever sees and changes their own garage."""

    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create_user("alice", password="pw-alice-123")
        cls.bob = User.objects.create_user("bob", password="pw-bob-123")
        cls.alice_car = Car.objects.create(owner=cls.alice, year="2015", make="Mazda", model="Miata")
        cls.bob_car = Car.objects.create(owner=cls.bob, year="2008", make="Subaru", model="Forester")
        cls.alice_part = Part.objects.create(car=cls.alice_car, part_name="Alice oil filter")
        cls.bob_part = Part.objects.create(car=cls.bob_car, part_name="Bob brake pads")

    def setUp(self):
        self.client.force_login(self.alice)

    def test_home_lists_only_own_cars(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(list(response.context["cars"]), [self.alice_car])
        self.assertEqual(response.context["total_parts"], 1)
        self.assertNotContains(response, "Forester")

    def test_saved_lists_only_own_parts(self):
        response = self.client.get(reverse("saved"))
        self.assertEqual(response.context["total"], 1)
        self.assertContains(response, "Alice oil filter")
        self.assertNotContains(response, "Bob brake pads")

    def test_new_car_is_owned_by_creator(self):
        self.client.post(reverse("home"), {
            "form_type": "car", "year": "2020", "make": "Honda", "model": "Civic",
        })
        self.assertEqual(Car.objects.get(model="Civic").owner, self.alice)

    def test_cannot_log_part_against_other_users_car(self):
        response = self.client.post(reverse("home"), {
            "form_type": "part",
            "car_id": self.bob_car.id,
            "part_name": "Sneaky spoiler",
            "category": "mods",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_id", response.context["part_errors"])
        self.assertFalse(Part.objects.filter(part_name="Sneaky spoiler").exists())

    def test_can_log_part_against_own_car(self):
        response = self.client.post(reverse("home"), {
            "form_type": "part",
            "car_id": self.alice_car.id,
            "part_name": "Air filter",
            "category": "maintenance",
        })
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Part.objects.filter(car=self.alice_car, part_name="Air filter").exists())

    def test_cannot_delete_other_users_part(self):
        response = self.client.post(reverse("delete_part", args=[self.bob_part.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Part.objects.filter(id=self.bob_part.id).exists())

    def test_can_delete_own_part(self):
        response = self.client.post(reverse("delete_part", args=[self.alice_part.id]))
        self.assertRedirects(response, reverse("saved"))
        self.assertFalse(Part.objects.filter(id=self.alice_part.id).exists())

    @mock.patch("vehicles.views.search_parts_with_serpapi", return_value=[])
    def test_search_ignores_other_users_car(self, search):
        self.client.get(reverse("home"), {
            "ai_search": "1", "search_car_id": self.bob_car.id, "query": "brakes",
        })
        search.assert_not_called()

        self.client.get(reverse("home"), {
            "ai_search": "1", "search_car_id": self.alice_car.id, "query": "brakes",
        })
        search.assert_called_once_with(self.alice_car, "brakes")
