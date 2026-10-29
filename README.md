# Online Course Assessment Application

IBM Coursera Django Final Project: **Add a New Assessment Feature to an Online Course App**

## Overview
This Django application extends an online course platform with interactive exam and assessment capabilities. Instructors can define questions and choices via Django Admin, and enrolled students can take assessments, submit responses, and view their scored exam results.

---

## Features
- **Course & Lesson Management:** Browse courses and study structured lessons.
- **Assessment & Examination:** Multiple-choice questions embedded within course lessons.
- **Admin Interface:** Full Django Admin integration with inlines (`QuestionInline`, `ChoiceInline`, `LessonInline`, `QuestionAdmin`, `LessonAdmin`).
- **Automated Grading:** Real-time scoring calculation and exam feedback based on correct choices.
- **Bootstrap Responsive UI:** Clean, modern interface designed using Bootstrap and Django template tags.

---

## Project Structure
```text
├── 03-admin-site.png                 # Django admin site screenshot
├── 07-final.png                      # Final exam result screenshot
├── ANS.md                            # Submission URL answers
├── generate_screenshots.py           # Automated screenshot generation script
├── manage.py                         # Django management script
├── myproject/                        # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── onlinecourse/                     # Online course application
│   ├── __init__.py
│   ├── admin.py                      # Admin registration & inlines
│   ├── apps.py
│   ├── models.py                     # Models: Course, Lesson, Question, Choice, Submission, etc.
│   ├── urls.py                       # App URL routes (submit, show_exam_result, etc.)
│   ├── views.py                      # Views (submit, show_exam_result, enroll, etc.)
│   └── templates/
│       └── onlinecourse/
│           ├── base.html
│           ├── course_details_bootstrap.html
│           ├── course_list_bootstrap.html
│           ├── exam_result_bootstrap.html
│           ├── login.html
│           └── registration.html
├── populate_data.py                  # Sample database population script
└── requirements.txt                  # Project dependencies
```

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Arnavx24/tfjzl-final-cloud-app-with-database.git
   cd tfjzl-final-cloud-app-with-database
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate sample data (creates admin & test user, courses, lessons, questions):**
   ```bash
   python populate_data.py
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Credentials
- **Admin Portal (`/admin/`):**
  - Username: `admin`
  - Password: `adminpassword123`
- **Student User (`/onlinecourse/login/`):**
  - Username: `student1`
  - Password: `studentpassword123`
