from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Part
import requests
import os
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import Count
from django.views.decorators.http import require_POST
from .forms import CreateUserForm, LoginForm

# Securely load API key from .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
_local_key = None
if env_path.exists():
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("SERPAPI_KEY="):
                _local_key = line.strip().split("=")[1]
                break

SERPAPI_KEY = os.environ.get("SERPAPI_KEY", _local_key)


def get_serpapi_key():
    key = os.environ.get("SERPAPI_KEY")
    if not key and env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.strip().startswith("SERPAPI_KEY="):
                    return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return key


def search_parts_with_serpapi(car, query):
    api_key = get_serpapi_key()
    search_query = f"{car.year} {car.make} {car.model} {query}"

    if api_key:
        params = {
            "api_key": api_key,
            "engine": "google",
            "q": search_query,
            "num": 6,
        }

        try:
            response = requests.get("https://serpapi.com/search.json", params=params, timeout=12)
            if response.status_code == 200:
                data = response.json()
                results = []

                # Check organic results
                for item in data.get("organic_results", [])[:6]:
                    title = item.get("title")
                    link = item.get("link")
                    if title and link:
                        results.append({"title": title, "link": link})

                # Check shopping / immersive results if organic was sparse
                if len(results) < 3:
                    for item in data.get("shopping_results", [])[:4]:
                        title = item.get("title")
                        link = item.get("link")
                        if title and link and not any(r["link"] == link for r in results):
                            results.append({"title": title, "link": link})

                if results:
                    return results[:6]
        except Exception:
            pass

    # Reliable automotive parts fallback links if API call fails or limits are exceeded
    encoded_q = requests.utils.quote(search_query)
    return [
        {
            "title": f"AutoZone - {car.year} {car.make} {car.model} {query}",
            "link": f"https://www.autozone.com/searchresult?searchText={encoded_q}",
        },
        {
            "title": f"RockAuto Catalog - {car.year} {car.make} {car.model} {query}",
            "link": f"https://www.rockauto.com/en/catalog/{car.make.lower()},{car.year},{car.model.lower()}",
        },
        {
            "title": f"Amazon Automotive - {car.year} {car.make} {car.model} {query}",
            "link": f"https://www.amazon.com/s?k={encoded_q}",
        },
        {
            "title": f"Advance Auto Parts - {car.year} {car.make} {car.model} {query}",
            "link": f"https://shop.advanceautoparts.com/c4/search?searchTerm={encoded_q}",
        },
    ]

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")

    context = {"registerForm": form}
    return render(request, "register.html", context)


def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")

    context = {"loginForm": form}
    return render(request, "my-login.html", context)


def user_logout(request):
    logout(request)
    return redirect("my-login")

def validate_car(data):
    errors = {}
    year = data.get("year", "").strip()
    if not (year.isdigit() and 1900 <= int(year) <= 2099):
        errors["year"] = "Enter a four-digit year between 1900 and 2099."
    if not data.get("make", "").strip():
        errors["make"] = "Enter the manufacturer."
    if not data.get("model", "").strip():
        errors["model"] = "Enter the model."
    return errors


def validate_part(data, user):
    errors = {}
    car_id = data.get("car_id", "")
    if not (car_id.isdigit() and Car.objects.filter(id=car_id, owner=user).exists()):
        errors["car_id"] = "Choose a vehicle from your garage."
    if not data.get("part_name", "").strip():
        errors["part_name"] = "Enter the part name."
    if data.get("category") not in dict(Part.CATEGORY_CHOICES):
        errors["category"] = "Choose a category."
    link = data.get("part_link", "").strip()
    if link:
        try:
            URLValidator()(link)
        except ValidationError:
            errors["part_link"] = "Enter a full link starting with https://"
    return errors


@login_required(login_url="my-login")
def home(request):
    cars = Car.objects.filter(owner=request.user).annotate(part_count=Count("part")).order_by("-id")
    ai_results = []
    searched = False
    selected_car_id = None
    query = ""
    car_errors, part_errors = {}, {}
    car_values, part_values = {}, {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "car":
            car_values = request.POST
            car_errors = validate_car(request.POST)
            if not car_errors:
                car = Car.objects.create(
                    owner=request.user,
                    nickname=request.POST.get("nickname", "").strip(),
                    year=request.POST["year"].strip(),
                    make=request.POST["make"].strip(),
                    model=request.POST["model"].strip(),
                )
                messages.success(request, f"{car} is in your garage.")
                return redirect("home")

        if form_type == "part":
            part_values = request.POST
            part_errors = validate_part(request.POST, request.user)
            if not part_errors:
                part = Part.objects.create(
                    car_id=request.POST["car_id"],
                    part_name=request.POST["part_name"].strip(),
                    category=request.POST["category"],
                    part_link=request.POST.get("part_link", "").strip(),
                )
                messages.success(request, f"Saved {part.part_name} to {part.get_category_display().lower()}.")
                return redirect("home")

    if request.GET.get("ai_search"):
        raw_car_id = request.GET.get("search_car_id")
        query = request.GET.get("query", "").strip()

        selected_car_id = None
        if raw_car_id:
            try:
                selected_car_id = int(raw_car_id)
            except ValueError:
                selected_car_id = None

        if selected_car_id and query:
            searched = True
            try:
                car = Car.objects.get(id=selected_car_id, owner=request.user)
                ai_results = search_parts_with_serpapi(car, query)
            except Car.DoesNotExist:
                ai_results = []

    context = {
        "cars": cars,
        "total_parts": Part.objects.filter(car__owner=request.user).count(),
        "ai_results": ai_results,
        "searched": searched,
        "selected_car_id": selected_car_id,
        "query": query,
        "car_errors": car_errors,
        "part_errors": part_errors,
        "car_values": car_values,
        "part_values": part_values,
        "categories": Part.CATEGORY_CHOICES,
    }

    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")

@login_required(login_url="my-login")
def contact(request):
    return render(request, "contact.html")

@login_required(login_url="my-login")
def saved(request):
    parts = Part.objects.select_related("car").filter(car__owner=request.user).order_by("-id")
    groups = [
        {"key": key, "label": label, "parts": [p for p in parts if p.category == key]}
        for key, label in Part.CATEGORY_CHOICES
    ]
    context = {"groups": groups, "total": len(parts)}
    return render(request, "saved.html", context)

@require_POST
@login_required(login_url="my-login")
def delete_part(request, part_id):
    part = get_object_or_404(Part, id=part_id, car__owner=request.user)
    part.delete()
    messages.success(request, f"Removed {part.part_name}.")
    return redirect("saved")
