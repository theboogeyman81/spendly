# Spec: Profile Page Design

## Overview
Implement the `/profile` route as a fully designed, logged-in-only page that displays the authenticated user's account information (name, email, member since) and provides a form to update their display name and change their password. This step replaces the stub string response and establishes the authenticated-user page pattern that expense-management screens will follow.

## Depends on
- Step 01 — Database Setup (`users` table and `get_db()` must exist)
- Step 02 — Registration (`create_user`, `get_user_by_email` must exist)
- Step 03 — Login and Logout (session and nav must be wired up)

## Routes
- `GET /profile` — render the profile page with current user data — logged-in only (redirect to `/login` if not authenticated)
- `POST /profile/name` — update display name — logged-in only
- `POST /profile/password` — change password (requires current password confirmation) — logged-in only

## Database changes
Two new helper functions needed in `database/db.py` (no schema changes):
- `get_user_by_id(user_id)` — returns the user row for a given id or `None`
- `update_user_name(user_id, name)` — updates the `name` field for the given user
- `update_user_password(user_id, password_hash)` — updates `password_hash` for the given user

## Templates
- **Create:** `templates/profile.html` — full profile page extending `base.html`

  Layout:
  - Page header: "Your Profile" heading with a short subline
  - **Account card** (read-only info):
    - Avatar placeholder (initials circle using CSS, no images)
    - Name (large), email (muted), "Member since \<created_at formatted as Month YYYY\>"
  - **Update name form** (inline card):
    - Single text input pre-filled with current name
    - Submit button "Save name"
    - Success/error flash rendered via `{{ name_msg }}` and `{{ name_error }}`
  - **Change password form** (separate card):
    - Current password input
    - New password input (min 8 chars)
    - Confirm new password input
    - Submit button "Change password"
    - Success/error flash rendered via `{{ pw_msg }}` and `{{ pw_error }}`

## Files to change
- `app.py` — replace the `/profile` stub; add `POST /profile/name` and `POST /profile/password` routes; import `get_user_by_id`, `update_user_name`, `update_user_password`; add `login_required` guard (inline check, not a decorator) to all three routes
- `database/db.py` — add `get_user_by_id()`, `update_user_name()`, `update_user_password()`

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with `werkzeug.security.generate_password_hash`; verified with `check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Auth guard: if `session.get("user_id")` is falsy, `redirect(url_for("login"))`; apply to all three routes
- After a successful name update, re-render the profile page with `name_msg="Name updated successfully."`
- After a failed name update (empty string), re-render with `name_error="Name cannot be empty."`
- Password change must verify the current password before hashing and saving the new one; on mismatch render `pw_error="Current password is incorrect."`
- New password must be ≥ 8 characters; on short password render `pw_error="Password must be at least 8 characters."`
- New password and confirm must match; on mismatch render `pw_error="Passwords do not match."`
- Avatar initials: take the first letter of the user's name (uppercased); display in a circular `div.avatar` using CSS only
- `created_at` is stored as `YYYY-MM-DD HH:MM:SS`; format it as `"May 2026"` in Python before passing to template (use `datetime.strptime` + `strftime`)
- The two forms POST to different URLs so they can be validated independently without entangling state
- Do not store flash messages in the session — pass them directly as template variables on re-render

## Definition of done
- [ ] `GET /profile` when not logged in redirects to `/login`
- [ ] `GET /profile` when logged in renders the page without errors
- [ ] Avatar circle shows the first letter of the user's name
- [ ] Name, email, and formatted member-since date are all visible
- [ ] Submitting an empty name shows an inline error on the name form
- [ ] Submitting a valid name updates the `users` table and shows a success message
- [ ] The name input is pre-filled with the current (or just-updated) name after re-render
- [ ] Submitting a wrong current password shows an error on the password form
- [ ] Submitting mismatched new/confirm passwords shows an error
- [ ] Submitting a new password shorter than 8 characters shows an error
- [ ] A valid password change updates `password_hash` in the database and shows a success message
- [ ] After a password change the user can log in with the new password
- [ ] Page is styled consistently with `base.html` and uses only CSS variables (no hardcoded hex)
