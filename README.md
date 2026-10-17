# 🚗 Pocket Mechanic

**Pocket Mechanic** is a lightweight digital garage for everyday drivers and car enthusiasts. Register your vehicles, log the parts you've bought or plan to buy for each one, and search for parts that fit your exact year, make and model.

🌐 **Live Demo**: [kendryckgarcia.pythonanywhere.com](https://kendryckgarcia.pythonanywhere.com)

---

## ✨ Features

- 🔐 **Private Garages** — Each account has its own vehicles and parts; nobody else can see or change them.
- 🚙 **Vehicle Records** — Year, make, model and an optional nickname, with a running count of parts per vehicle.
- 🔧 **Parts Log** — Save parts under Maintenance, Accessories or Modifications, with an optional purchase link.
- 🔍 **Parts Search** — Search by part or symptom for a specific vehicle using SerpAPI, then save any result straight to your log. Without an API key it falls back to search links for AutoZone, RockAuto, Amazon and Advance Auto Parts.
- 📁 **Saved Parts** — All your parts grouped by category, with one-click removal.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Django 5.2 LTS, SQLite
- **Frontend**: Django templates, vanilla CSS
- **API**: SerpAPI (Google results for automotive parts)
- **Deployment**: PythonAnywhere

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

Run the tests with:
```bash
python manage.py test vehicles
```

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

