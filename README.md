# DevTrack — Developer Internship Tracker

A full-stack web application to track internship and job applications. Built with Flask, PostgreSQL, and REST APIs.

🔗 **Live Demo:** https://devtrack-fjw4.onrender.com

---

## Features

- User authentication (register, login, logout)
- Add, edit, delete internship applications
- Track application status (Applied, Interview, Offer, Rejected)
- Dashboard with real-time stats
- Search and filter applications
- Pagination
- User profile management
- REST API with token-based authentication
- Custom error handling

---

## Tech Stack

**Backend:** Python, Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Migrate, Flask-WTF

**Database:** PostgreSQL (Neon), SQLite (development)

**Deployment:** Render

**API:** REST API with Bearer token authentication

---

## Project Structure
```
DevTrack/
├── app/
│   ├── __init__.py         # App factory, extensions
│   ├── models.py           # Database models
│   ├── auth/               # Authentication blueprint
│   ├── main/               # Core features blueprint
│   ├── api/                # REST API blueprint
│   ├── errors/             # Error handlers
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS files
├── config.py               # Configuration
├── run.py                  # Entry point
├── Procfile                # Render deployment
└── requirements.txt        # Dependencies
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/login | Get auth token |
| GET | /api/applications | Get all applications |
| POST | /api/applications | Create application |
| PUT | /api/applications/:id | Update application |
| DELETE | /api/applications/:id | Delete application |
| GET | /api/stats | Get dashboard stats |
| GET | /api/health | Health check |

---

## Local Setup
```bash
# Clone the repo
git clone https://github.com/yourusername/devtrack.git
cd devtrack

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run migrations
flask db upgrade

# Start the app
python run.py
```

---

## Environment Variables
```
SECRET_KEY=your-secret-key
DATABASE_URL=your-postgresql-url
```

---

## Future Plans

- ML-based placement predictor using scikit-learn
- Data visualization dashboard
- Email notifications for application updates
- Mobile-responsive UI

---

## Author

**Sahil Teltumde**
MCA Student | Backend Developer
```

---

### Step 2 — Create .env.example

Create `.env.example` file in root:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@host/dbname