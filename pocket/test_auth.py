import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pocket.settings')
django.setup()

from vehicles.forms import LoginForm
from django.contrib.auth import authenticate

print("Testing Login Form")
data = {
    'username': 'testuser2',
    'password': 'StrongPass123!'
}
form = LoginForm(None, data=data)
if form.is_valid():
    print("Login form valid")
    u = form.cleaned_data.get('username')
    p = form.cleaned_data.get('password')
    print("Auth inside form:", form.get_user())
    print("Auth authenticate:", authenticate(username=u, password=p))
else:
    print("Login form invalid", form.errors)
