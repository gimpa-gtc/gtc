# GTC Core (gtccore) — Codebase Documentation

Generated: 2026-01-06

## 1) Project Overview

This repository is a Django 4.2 project for GIMPA Training & Consulting (GTC). It provides:

- A **public-facing website** (landing, courses, enrollments, application status, contact/FAQs, payment receipt upload).
- A **staff dashboard** for managing courses, categories, cohorts, applications, admissions, payments, content, support messages, gallery, teams, and access control.
- A **custom accounts app** with a custom `User` model and simple login/logout views.

The project currently uses **SQLite** (`db.sqlite3`) as its database.

---

## 2) High-Level Architecture

### Django Project Layout

- **Project package**: `gtccore/` (settings, root URL routing, WSGI/ASGI entrypoints, shared “library” helpers)
- **Apps**:
  - `website/` — public pages and enrollment/application flows
  - `dashboard/` — staff/admin dashboard with extensive CRUD and download/export functionality
  - `accounts/` — custom user model + authentication views

### Request Flow

1. Incoming requests hit the root URL config in `gtccore/urls.py`.
2. URLs are routed to app URL modules:
   - `website.urls` at `/`
   - `dashboard.urls` at `/dashboard/`
   - `accounts.urls` at `/` (login/logout)
3. Templates are resolved from each app’s `templates/` directory (Django `APP_DIRS=True`).
4. Static and media files are served by Django only when `DEBUG=True`.

---

## 3) Running the Project (Local Development)

### Prerequisites

- Python (compatible with Django 4.2)
- Dependencies installed from `requirements.txt`

### Common Commands

- Install deps: `pip install -r requirements.txt`
- Migrate DB: `python manage.py migrate`
- Run dev server: `python manage.py runserver`

---

## 4) Repository Root

### Key Files

- `manage.py`
  - Standard Django management entrypoint.

- `requirements.txt`
  - Pinned dependencies. Notable packages:
    - `Django==4.2.7`
    - `requests` (used for SMS integration)
    - `Pillow` (ImageField support)
    - `fpdf2` (For PDF generation / mostly used in the admission letter generations)

- `db.sqlite3`
  - SQLite database file (development/local data).

### Key Directories

- `gtccore/` — Django project settings, URLs, deployment entrypoints, shared helpers.
- `accounts/` — custom authentication + user model.
- `dashboard/` — staff dashboard and core business models.
- `website/` — public site and enrollment flow.
- `static/` — static assets for dashboard and website.
- `media/` — uploaded files (courses, receipts, gallery images, etc.).
- `venv/` — local virtual environment (typically should not be committed).

---

## 5) Django Project Package: `gtccore/`

### 5.1 `gtccore/settings.py`

Defines settings including:

- `INSTALLED_APPS`: `website`, `dashboard`, `accounts` plus Django defaults.
- `MIDDLEWARE`: includes a custom middleware `dashboard.middleware.error.CustomErrorMiddleware`.
- `AUTH_USER_MODEL = 'accounts.User'` (custom user model).
- Static/media configuration:
  - `STATIC_URL = '/static/'`, `STATICFILES_DIRS = [BASE_DIR / 'static']`, `STATIC_ROOT = BASE_DIR / 'staticfiles/'`
  - `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`
- Email settings (SMTP Gmail) wired through `gtccore.cred.GtcCred`.
- SMS settings wired through `gtccore.cred.GtcCred`.

Important operational detail:
- `DEBUG` is currently set to `True`.
- `ALLOWED_HOSTS = ['*', 'gtc.gimpa.edu.gh']`.

### 5.2 `gtccore/urls.py`

Root URL routes:

- `/admin/` → Django admin
- `/` → `website.urls`
- `/dashboard/` → `dashboard.urls`
- `/login/` and `/logout/` → `accounts.urls` (included at root)

In `DEBUG` mode, Django serves static and media routes.

### 5.3 `gtccore/asgi.py` and `gtccore/wsgi.py`

Deployment entrypoints for ASGI and WSGI servers.

### 5.4 `gtccore/cred.py`

This file contains credentials/config helper class used by the main settings file of the project.


### 5.5 Shared Library: `gtccore/library/`

- `constants.py`
  - This contains Enums (contant values) for payment modes/status and application status.

- `services.py`
  - This file contains extra services and 3rd-party Integrations:
    - `send_sms(...)` uses Arkesel API (`https://sms.arkesel.com/api/v2/sms/send`) via `requests`.
    - `send_mail(...)` sends HTML email using Django `EmailMultiAlternatives` and template `dashboard/notifications/application_notification.html`.

- `context_processors.py`
  - Injects `all_categories` into template context (queries `dashboard.models.CourseCategory`).

- `decorators.py`
  - `StaffLoginRequired`: a callable wrapper enforcing authenticated + staff/superuser access.

- `logs.py`
  - `log_user_activity(user, action, pre_object, post_object)` writing to `accounts.UserLog`.

- Image assets: `gimpa-round-logo.jpg`, `signature.png`. These files are used for the site header image/logo and the signature on the generated admission letter.

---

## 6) App: `accounts/`

### Purpose

Provides a custom user model (`accounts.User`) and basic authentication views (login/logout). The dashboard relies on this user model for staff access and logging.

### Key Files

- `accounts/models.py`
  - `User` extends `AbstractBaseUser` and `PermissionsMixin`.
    - Primary login field: `email` (`USERNAME_FIELD = 'email'`).
    - Fields include `name`, `phone`, notification preferences, profile picture, staff flags, and `failed_login_attempt` counter.
  - `UserLog` records user actions, storing “before/after” snapshots.

- `accounts/manager.py`
  - `AccountManager` implements `create_user` and `create_superuser`.

- `accounts/views.py`
  - `LoginView`
    - Authenticates using `authenticate()` and logs users in.
    - Suspends accounts after 3 failed attempts (`is_active=False`).
  - `LogoutView`

- `accounts/urls.py`
  - `/login/` and `/logout/`

- `accounts/admin.py`
  - Registers `User` and `UserLog` in Django admin.

- `accounts/templates/accounts/`
  - Login template(s) and account-related templates.

- `accounts/migrations/`
  - Custom user model, user log, and login attempt tracking.

---

## 7) App: `dashboard/`

### Purpose

Implements the staff dashboard and most business-domain models:

- Courses + categories + cohorts
- Applications + admissions
- Payments and receipt uploads
- Applicants extracted from applications
- Notifications + FAQs + testimonials + teams/facilitators
- Contact messages and custom course requests
- Gallery (image categories and images)
- Groups/permissions management

### Key Files

#### 7.1 `dashboard/models.py`

Contains the core domain models. High-level:

- `CourseCategory`
  - Name, coordinator contact details.
  - Utility methods: course and application/admission counts.

- `Course`
  - Title/description/details, cohort/category, schedule, pricing (local and foreign), capacity, requirements/syllabus, thumbnail.
  - Supports optional certificate uploads and flags for part payment.

- `Application`
  - Generates `application_id` (e.g., `GTC-AP-XXXXXXX`).
  - Tracks applicant details, course, certificate, status fields (application/payment mode/payment status).
  - Payment history helpers: `get_payment_status()`, `get_total_payments()`, etc.

- `Admission`
  - One-to-one with application.

- `Payment`
  - Generates `transaction_id` (e.g., `GTC-TR-XXXXXXXX`).
  - Stores amount, network, number, receipt image, status codes and messages.
  - Provides `approve()`/`disapprove()` helpers.

- `Applicant`
  - Extracted from `Application` by signal.

- Content/support and misc:
  - `Notification`, `Faq`, `Contact`, `CustomCourseRequest`, `Cohort`, `Testimonial`, `Comment`, `Facilitator`, `ImageCategory`, `Image`.

#### 7.2 `dashboard/signals.py`

Uses Django signals to automate behavior:

- On `Application` save:
  - Extracts/creates `Applicant`.
  - Sends applicant SMS confirmation.
  - Notifies course coordinator (SMS and/or email).
  - Notifies the team email.
  - Auto-creates or deletes `Admission` depending on approval status.

- On `Admission` creation:
  - Sends applicant SMS with admission link.

- On `CustomCourseRequest` creation:
  - Sends requester confirmation SMS.
  - Notifies admins via SMS.

- On `User` creation:
  - Generates a random numeric password and sends it via SMS.

#### 7.3 `dashboard/forms.py`

Model forms used by website and dashboard views:

- `ApplicationForm`, `PaymentForm`, `CourseForm`, `CohortForm`, `CourseCategoryForm`
- `ContactUsForm`, `CustomCourseReguestForm`
- `FacilitatorForm`, `ImageCategoryForm`, `NotificationForm`

#### 7.4 `dashboard/middleware/error.py`

`CustomErrorMiddleware`:

- Restricts `/admin/` access to superusers.
- Renders custom templates for `403`, `404`, and `500`.

#### 7.5 `dashboard/urls.py`

Large route surface under `/dashboard/` including:

- Dashboard home, user profile, and settings
- Users + groups/permissions
- Applications/admissions/applicants
- Course management (courses/categories/cohorts)
- Payments
- Support (contacts, course requests)
- Notifications broadcast
- Content management (FAQs, testimonials, teams)
- Gallery
- Download/export endpoints for many entities

#### 7.6 `dashboard/views/` (modular view implementation)

Views are split into multiple modules, then re-exported via `dashboard/views/__init__.py`.

Modules:

- `dashboard.py` — dashboard landing/home
- `settings.py` — settings, preferences, profile pic changes, password reset
- `profile.py` — staff profile page
- `users.py` — staff users CRUD, details, profile pics, group/permission assignments, downloads
- `groups.py` — group CRUD and permission management
- `applications.py` — application list/create, admissions, applicants, delete endpoints, downloads
- `courses.py` — courses CRUD/delete and downloads
- `category.py` — categories and cohorts CRUD/delete and downloads
- `payments.py` — payments list/create, approve/disapprove, downloads
- `contact_messages.py` — inbound contacts + reply + downloads
- `course_requests.py` — custom course requests + reply/delete + downloads
- `notifications.py` — notification CRUD/broadcast + downloads
- `faqs.py` — FAQ CRUD + delete
- `testimonials.py` — testimonial CRUD + delete
- `teams.py` — team CRUD + delete + download
- `facilitators.py` — facilitator CRUD + download
- `gallery.py` — image categories + images CRUD/delete
- `error.py` — (additional error-related views if any)

Note: many of these views use `PermissionRequiredMixin` for access control.

#### 7.7 `dashboard/admin.py`

Registers most dashboard models in Django admin.

#### 7.8 `dashboard/management/commands/deploy.py`

A custom management command that runs a deployment script:

- `git pull origin main`
- `makemigrations`, `migrate`, `collectstatic --noinput`
- restarts nginx and gunicorn via `sudo`

This is environment-specific and assumes Linux services.

#### 7.9 `dashboard/templates/`

Template structure:

- `dashboard/templates/base/` — base layouts
- `dashboard/templates/dashboard/` — dashboard pages
- `dashboard/templates/includes/` — shared fragments

#### 7.10 `dashboard/migrations/`

Contains a long migration history for:

- Course details, thumbnails, cohorts, comments
- Payments and receipts
- Notifications broadcast flag
- Coordinators on categories
- Gallery models
- Facilitator precedence

---

## 8) App: `website/`

### Purpose

Public-facing site and student/applicant workflows.

### Key Files

- `website/views.py`
  - `HomeView`: shows popular courses, team, testimonials, gallery.
  - `ContactView`: renders contact page and saves contact messages.
  - `FaqsView`: displays FAQs.
  - `CoursesView`: course browsing/filtering/search.
  - `CourseDetailsView`: course details + comments; posts custom course requests.
  - `EnrollView`: creates an application (with duplicate enrollment check).
  - `ApplicationStatusView`: checks application by application ID.
  - `UploadPaymentReceiptView`: uploads a payment receipt (creates `dashboard.Payment`).
  - `DownloadAdmissionLetterView`: renders admission letter template.

- `website/urls.py`
  - `/` home
  - `/contact/`, `/faqs/`
  - `/courses/`, `/courses-details/`
  - `/enroll/`, `/enroll/success`
  - `/application/`, `/application/status/`, `/application/download/`
  - `/make-payment/` and `/upload-receipt/`

- `website/models.py`
  - Currently empty (website uses dashboard models/forms).

- `website/templates/`
  - `website/templates/base/`, `website/templates/includes/`, `website/templates/website/`

---

## 9) Static & Media

### `static/`

- `static/dashboard/` — dashboard UI assets
- `static/website/` — website UI assets (CSS/fonts/images/JS, color-switcher)

### `media/`

Uploads organized by Django `ImageField/FileField` paths:

- `certificates/`, `courses/`, `facilitators/`, `gallery/`, `profile/`, `receipts/`, `testimonials/`

---

## 10) Security & Secrets (Important)

The repository currently contains sensitive values hard-coded in source.

- `gtccore/settings.py` contains a Django `SECRET_KEY` literal. This is needed (and was automatically generated by Django) by Django.
- `gtccore/cred.py` contains hard-coded credentials (SMS API key and SMTP username/password).
- `gtccore/library/services.py` sends SMS using `settings.ARKESEL_API_KEY`, which is ultimately sourced from `gtccore/cred.py`.

Recommended minimum remediation:

- You can and should replace the hard-coded values with environment variables (e.g., `os.environ.get(...)`).

---

## 11) Notes / Observations

- There are placeholder `tests.py` files in each app for when you need to write or implement unit tests.
- `website` relies heavily on `dashboard` models and forms.
- `dashboard.middleware.error.CustomErrorMiddleware` enforces admin restrictions even when `DEBUG=True`.

---

## 12) Quick Reference: URL Routing

- Root router: `gtccore/urls.py`
  - `/` → `website`
  - `/dashboard/` → `dashboard`
  - `/login/`, `/logout/` → `accounts`
  - `/admin/` → Django admin (but restricted by middleware)
