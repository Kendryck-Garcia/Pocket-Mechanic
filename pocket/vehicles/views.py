from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Part
import requests
import os
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

@login_required(login_url="my-login")
def home(request):
    cars = Car.objects.all()
    ai_results = []
    selected_car_id = None
    query = ""


    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "car":
            Car.objects.create(
                nickname=request.POST.get("nickname"),
                year=request.POST.get("year"),
                make=request.POST.get("make"),
                model=request.POST.get("model"),
            )
            return redirect("home")

        if form_type == "part":
            Part.objects.create(
                car_id=request.POST.get("car_id"),
                part_name=request.POST.get("part_name"),
                category=request.POST.get("category", "maintenance"),
                part_link=request.POST.get("part_link"),
            )
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
            try:
                car = Car.objects.get(id=selected_car_id)
                ai_results = search_parts_with_serpapi(car, query)
            except Car.DoesNotExist:
                ai_results = []

    context = {
        "cars": cars,
        "ai_results": ai_results,
        "selected_car_id": selected_car_id,
        "query": query,
    }

    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")

@login_required(login_url="my-login")
def contact(request):
    return render(request, "contact.html")

@login_required(login_url="my-login")
def saved(request):
    parts = Part.objects.select_related("car").all()
    return render(request, "saved.html", {"parts": parts})

@login_required(login_url="my-login")
def delete_part(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    part.delete()
    return redirect("saved")
