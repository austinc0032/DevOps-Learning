#This is a README file for the project. It provides an overview of the project, its purpose, and how to use it.
#Learning how to load a repository and push the file to GitHub.

# DevOps Learning Path

## Current Progress
- [x] Git basics
- [ ] Programming languages (Python basics)
- [ ] Docker fundamentals
- [ ] Kubernetes intro

## Learning Goals
- Understand containerization
- Master CI/CD pipelines
- Deploy applications

## Resources
- [https://github.com/milanm/DevOps-Roadmap/tree/master]

## Ticketing System Web App
This workspace now includes a Flask-based ticketing system in `TicketingSystem.py`.

### Install
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run locally
```bash
python TicketingSystem.py
```

### Configuration
Optional environment variables:
- `TICKET_SECRET_KEY` - secret key for session security.
- `TICKET_DATABASE_URI` - database URI (default: `sqlite:///tickets.db`).
- `ADMIN_EMAIL` and `ADMIN_PASSWORD` - create a default admin account on first run.
- `ADMIN_NOTIFICATION_EMAILS` - comma-separated emails to notify when a new ticket is created.
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USE_SSL`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER` for email notifications.

### Features
- User registration and login
- Per-user ticket history
- Admin dashboard with all tickets
- Ticket status updates and comments
- Email notifications when tickets are created or status changes
