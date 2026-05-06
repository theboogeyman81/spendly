# Spec: Login and Logout

## Overview
Wire the existing `login.html` form to a real POST handler that authenticates users against the database, and implement the logout route that clears the session. This step introduces `check_password_hash`, proper credential validation, and session teardown — completing the full auth lifecycle started in Step 02 (Registration). After this step, users can sign in, stay signed in across requests, and explicitly sign out.

## Depends on
- Step 01 — Database Setup (`users` table and `get_db()` must exist)
- Step 02 — Registration (`get_user_by_email()` must exist in `database/db.py`)

## Routes
- `GET /login` — render login form — public (already exists; extend to accept POST)
- `POST /login` — validate credentials, set session, redirect to landing — public
- `POST /logout` — clear session, redirect to landing — logged-in (change from existing GET stub)

## Database changes
No new tables or columns. No new DB helper functions needed — `get_user_by_email()` already exists.

## Templates
- **Modify:** `templates/login.html` — preserve the `email` field value on validation error (add `value="{{ email or '' }}"` to the email input)
- **Modify:** `templates/base.html` — update the `nav-links` block to show "Sign out" (POST form button) when `session.user_id` is set, and show "Sign in" / "Get started" links only when the user is not logged in

## Files to change
- `app.py` — convert `/login` to accept GET and POST; import `check_password_hash` from `werkzeug.security`; implement credential check and session set on POST; convert `/logout` from GET stub to POST route that calls `session.clear()` and redirects to `url_for("landing")`
- `templates/login.html` — add `value="{{ email or '' }}"` to the email input
- `templates/base.html` — add Jinja conditional in `nav-links` to show auth-aware navigation

## Files to create
None

## New dependencies
No new dependencies

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On failed login (wrong email or wrong password) render a **single generic error** — "Invalid email or password." — do not reveal which field is wrong
- On successful login set `session["user_id"] = user["id"]` and redirect to `url_for("landing")`
- Logout must use `session.clear()`, not `session.pop()`
- Logout route must be POST (use a `<form method="POST">` with a button in the nav) to prevent CSRF via link
- The logout form in `base.html` must include no visible page transition — just a button styled as a nav link

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting an unknown email shows "Invalid email or password." without crashing
- [ ] Submitting a correct email with a wrong password shows "Invalid email or password."
- [ ] Submitting valid credentials sets `session["user_id"]` and redirects to the landing page
- [ ] The email field retains its value when the form re-renders on error
- [ ] `POST /logout` clears the session and redirects to the landing page
- [ ] After logout, `session["user_id"]` is no longer set
- [ ] The navbar shows "Sign in" and "Get started" when no user is logged in
- [ ] The navbar shows a "Sign out" button (and hides "Sign in"/"Get started") when a user is logged in
- [ ] Visiting `/logout` via GET does not work (405 or redirect)
