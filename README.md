# Struggle of Student (SS)

A student community website built with Flask. It includes community information pages, a registration form, SQLite storage, and a password-protected admin dashboard.

## Pages and features

- Home, About, Opportunities, Talent, Skills, Learning, Campus Ambassador, Roles, Events, Gallery, Career, and Contact pages
- Responsive navigation and the SS red and black visual theme
- Student registration form backed by SQLite
- Admin dashboard at `/admin`, protected with HTTP Basic Authentication
- Custom 404 page

## Run locally

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SS_ADMIN_USERNAME="admin"
export SS_ADMIN_PASSWORD="choose-a-long-private-password"
python app.py
```

Open `http://127.0.0.1:5000`. The database is created automatically in the project directory. On Windows PowerShell, set the two admin variables with `$env:SS_ADMIN_USERNAME="admin"` and `$env:SS_ADMIN_PASSWORD="choose-a-long-private-password"` before running the app.

The admin dashboard is at `http://127.0.0.1:5000/admin`. Set both admin environment variables before visiting it. Do not put a real password in source code or commit it to GitHub.

## Publish the source on GitHub

Create an empty repository on GitHub, then run these commands from this folder, replacing the URL with your repository URL:

```bash
git init
git add .
git commit -m "Prepare SS community website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

The `.gitignore` file excludes the local database, virtual environment, Python cache, and local environment files. Do not remove those exclusions before publishing: the database can contain student contact information.

## Deploy the working website

GitHub Pages only serves static files; it cannot run this Flask app or its SQLite database. To make the form and admin dashboard work online, publish the repository to a Flask-capable host. This project includes `render.yaml` for Render Blueprint deployment:

1. Push the repository to GitHub.
2. In Render, create a new Blueprint and connect the GitHub repository.
3. Enter private values for `SS_ADMIN_USERNAME` and `SS_ADMIN_PASSWORD` when prompted.
4. Deploy the service and open the generated `onrender.com` URL.

The Blueprint attaches persistent storage for SQLite registrations. That storage requires a Render service plan that supports persistent disks. Keep the admin password private and use a unique, strong password.
