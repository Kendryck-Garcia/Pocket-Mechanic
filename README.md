# 🚗 Pocket Mechanic

**Pocket Mechanic** is a clean, lightweight digital garage web app built to help everyday drivers and car enthusiasts track maintenance history, upcoming service schedules, and repair costs.

🌐 **Live Demo**: [kendryckgarcia.pythonanywhere.com](https://kendryckgarcia.pythonanywhere.com)

---

## ✨ Features

- 🚙 **Vehicle Management** — Add and manage your personal fleet in a centralized garage.
- 🔧 **Maintenance Tracking** — Log completed services, repair dates, and total costs.
- 📊 **Service Reminders** — Stay ahead of routine oil changes, tire rotations, and scheduled maintenance.
- 🔍 **Live Parts Search** — Real-time automotive parts and price search powered by SerpAPI.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Django 4.2
- **Frontend**: HTML5, Vanilla CSS
- **API**: SerpAPI (Google Search for automotive parts)
- **Deployment**: PythonAnywhere, WhiteNoise, Gunicorn

---

## 🚀 Quickstart (Run Locally)

### 1. Clone the repository
```bash
git clone https://github.com/Kendryck-Garcia/Pocket-Mechanic.git
cd Pocket-Mechanic
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
SERPAPI_KEY=your-serpapi-key-optional
```

### 5. Run migrations & start server
```bash
cd pocket
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## ⚙️ Environment Variables

| Variable | Description |
|:---|:---|
| `DEBUG` | Set to `True` for development, `False` for production |
| `SECRET_KEY` | Django secret key for security |
| `ALLOWED_HOSTS` | Comma-separated list of permitted hostnames |
| `SERPAPI_KEY` | *(Optional)* SerpAPI key for live parts search |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

