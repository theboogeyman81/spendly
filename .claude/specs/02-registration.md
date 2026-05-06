# Spec: Registration

## Overview
Wire the existing `register.html` form to a real POST handler so visitors can create a Spendly account. The route validates input server-side, hashes the password with werkzeug, inserts the user into the `users` table, and starts a Flask session. This is the first step that introduces server-side session state and is the foundation for login/logout in Step 03.

## Depends on
- Step 01 — Database Setup (`users` table must exist)

## Routes
- `GET /register` — render registration form — public (already exists; extend to accept POST)
- `POST /register` — validate form, create user, set session, redirect — public

## Database changes
No new tables or columns. Two new helper functions needed in `database/db.py`:
- `create_user(name, email, password_hash)` — inserts a new user, returns the new user row or `None` on duplicate email
- `get_user_by_email(email)` — returns the user row for a given email or `None`

## Templates
- **Modify:** `templates/register.html` — already contains the form and `{% if error %}` block; add `value="{{ name or '' }}"` and `value="{{ email or '' }}"` to preserve field values on validation error

## Files to change
- `app.py` — convert `/register` to accept GET and POST; import `request`, `redirect`, `session` from Flask; import `generate_password_hash` from `werkzeug.security`; import `create_user`, `get_user_by_email` from `database.db`; set `app.secret_key`
- `database/db.py` — add `create_user()` and `get_user_by_email()`
- `templates/register.html` — preserve field values on error (see Templates above)

## Files to create
None

## New dependencies
No new dependencies

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set via `os.environ.get("SECRET_KEY", "dev-secret-change-me")`
- Validate server-side: name non-empty, email non-empty, password ≥ 8 characters
- On duplicate email re-render the form with a clear error message; do not leak whether the email is already registered beyond "An account with that email already exists."
- After successful registration set `session["user_id"] = user["id"]` and redirect to `url_for("landing")`

## Definition of done
- [ ] `GET /register` renders the registration form without errors
- [ ] Submitting an empty form re-renders with a validation error
- [ ] Submitting a password shorter than 8 characters shows an error
- [ ] Submitting a duplicate email shows an error without crashing
- [ ] Submitting valid data inserts a new row in the `users` table
- [ ] The stored password is a hash, not plaintext
- [ ] `session["user_id"]` is set after successful registration
- [ ] User is redirected to the landing page after successful registration
- [ ] Name and email fields retain their values when the form re-renders on error
