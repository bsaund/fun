import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
# Cloud Run terminates TLS; trust its forwarded headers so redirect URIs are https
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

ALLOWED_EMAILS = {
    e.strip().lower()
    for e in os.environ.get("ALLOWED_EMAILS", "").split(",")
    if e.strip()
}

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "unset"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "unset"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email"},
)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Secrets</title>
<style>
  body { margin: 0; min-height: 100vh; display: flex; flex-direction: column;
         align-items: center; justify-content: center;
         font-family: system-ui, sans-serif; background: #111; color: #eee; }
  .number { font-size: 8rem; font-weight: 700; letter-spacing: 0.05em; }
  .caption { color: #888; margin-top: 1rem; }
  a { color: #6af; }
</style>
</head>
<body>
  <div class="number">1989</div>
  <div class="caption">Logged in as EMAIL &middot; <a href="/logout">log out</a></div>
</body>
</html>
"""


@app.route("/")
def index():
    email = session.get("email")
    if not email or email not in ALLOWED_EMAILS:
        return redirect(url_for("login"))
    return PAGE.replace("EMAIL", email)


@app.route("/login")
def login():
    return oauth.google.authorize_redirect(url_for("auth_callback", _external=True))


@app.route("/auth/callback")
def auth_callback():
    token = oauth.google.authorize_access_token()
    info = token.get("userinfo") or {}
    email = (info.get("email") or "").lower()
    if not info.get("email_verified") or email not in ALLOWED_EMAILS:
        session.clear()
        return ("Access denied for %s." % (email or "unknown account"), 403)
    session["email"] = email
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
