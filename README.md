# 🚗 Pocket Mechanic

**Pocket Mechanic** is a web application designed to help everyday drivers and auto enthusiasts manage their vehicles. It provides a simple digital garage where you can easily keep track of your car's maintenance history, upcoming service schedules, and parts costs.


### Built With:
- **Backend**: Python, Django
- **Frontend**: HTML5, custom Vanilla CSS
- **API**: SerpAPI (Google Search for live part fetching)

## Features

- 🚙 **Vehicle Management** - Add and manage multiple vehicles
- 🔧 **Maintenance Tracking** - Log maintenance history and costs
- 📊 **Service Reminders** - Track upcoming maintenance
- 🔍 **Live Parts Search** - Search for automotive parts in real-time with SerpAPI

## Getting Started

### Prerequisites
- Python 3.9+
- pip
- Django 4.2+

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Kendryck-Garcia/Pocket-Mechanic.git
cd Pocket-Mechanic
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
SERPAPI_KEY=your-serpapi-key
```

5. **Run migrations**
```bash
cd pocket
python manage.py migrate
```

6. **Start the development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` or `http://127.0.0.1:8000` in your browser.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DEBUG` | Set to `False` in production |
| `SECRET_KEY` | Django secret key (auto-generated on Render) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed domains |
| `SERPAPI_KEY` | Your SerpAPI key for live parts search |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support & Contributions

Found a bug or have a feature request? Feel free to open an issue!

Contributions are welcome! Please fork the repository and submit a pull request.

---

**Happy tracking! Keep your vehicles in top shape with Pocket Mechanic.** 🔧
