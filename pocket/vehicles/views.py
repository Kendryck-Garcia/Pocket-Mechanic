from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Part
import requests


SERPAPI_KEY = "09d2287ae9bbea48cfe3d2aa5f4488c47dc481e1448797758839625c0b465057"


def search_parts_with_serpapi(car, query):
    search_query = f"{car.year} {car.make} {car.model} {query} auto parts"

    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "q": search_query,
        "num": 5,
    }

    try:
        response = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
        if response.status_code != 200:
            return []

        data = response.json()
        results = []

        for item in data.get("organic_results", [])[:5]:
            title = item.get("title")
            link = item.get("link")
            if title and link:
                results.append({"title": title, "link": link})

        return results
    except Exception:
        return []


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


def contact(request):
    return render(request, "contact.html")


def saved(request):
    parts = Part.objects.select_related("car").all()
    return render(request, "saved.html", {"parts": parts})


def delete_part(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    part.delete()
    return redirect("saved")
