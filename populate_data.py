import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from onlinecourse.models import (
    Course, Lesson, Instructor, Learner, Enrollment, Question, Choice, Submission
)
from datetime import date

def populate():
    print("Creating admin user...")
    admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
    admin_user.set_password('adminpassword123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()

    print("Creating student user...")
    student_user, _ = User.objects.get_or_create(username='student1', defaults={'email': 'student1@example.com', 'first_name': 'Arnav', 'last_name': 'Kulkarni'})
    student_user.set_password('studentpassword123')
    student_user.first_name = 'Arnav'
    student_user.last_name = 'Kulkarni'
    student_user.save()

    instructor_user, _ = User.objects.get_or_create(username='instructor1', defaults={'email': 'instructor1@example.com', 'first_name': 'Alex', 'last_name': 'Mercer'})
    instructor_user.set_password('instructorpass123')
    instructor_user.save()

    instructor, _ = Instructor.objects.get_or_create(user=instructor_user, defaults={'full_time': True, 'total_learners': 150})
    learner, _ = Learner.objects.get_or_create(user=student_user, defaults={'occupation': 'developer', 'social_link': 'https://github.com/Arnavx24'})

    print("Creating courses...")
    course1, _ = Course.objects.get_or_create(
        name="Cloud Application Development with Django",
        defaults={
            'description': "Learn how to build and deploy cloud-native web applications using Django framework, relational databases, and microservices architecture.",
            'pub_date': date.today(),
            'total_enrollment': 2
        }
    )
    course1.instructors.add(instructor)
    course1.save()

    course2, _ = Course.objects.get_or_create(
        name="Introduction to Web Development with HTML, CSS, and JavaScript",
        defaults={
            'description': "Master fundamental building blocks of modern responsive web design using Bootstrap, HTML5, and JavaScript.",
            'pub_date': date.today(),
            'total_enrollment': 1
        }
    )

    print("Creating lessons...")
    lesson1, _ = Lesson.objects.get_or_create(
        title="Django Architecture and Project Structure",
        course=course1,
        defaults={
            'order': 1,
            'content': "Django follows the Model-View-Template (MVT) design pattern. The models define your data structure, the views handle application logic and requests, and templates render the user interface."
        }
    )

    lesson2, _ = Lesson.objects.get_or_create(
        title="Models, Migrations, and Django Admin",
        course=course1,
        defaults={
            'order': 2,
            'content': "Django ORM automatically translates Python classes into SQL database tables. Django Admin provides an out-of-the-box management interface for your models."
        }
    )

    lesson3, _ = Lesson.objects.get_or_create(
        title="Views, Forms, and Assessment Features",
        course=course1,
        defaults={
            'order': 3,
            'content': "Learn how to implement interactive assessments, handle form submissions via POST requests, evaluate student responses, and calculate exam scores."
        }
    )

    print("Creating questions and choices...")
    # Clear existing questions for clean populate
    Question.objects.filter(course=course1).delete()

    # Question 1
    q1 = Question.objects.create(
        course=course1,
        lesson=lesson1,
        content="What architectural pattern does Django primarily follow?",
        grade=25
    )
    Choice.objects.create(question=q1, content="MVT (Model-View-Template)", is_correct=True)
    Choice.objects.create(question=q1, content="MVC (Model-View-Controller)", is_correct=False)
    Choice.objects.create(question=q1, content="MVVM (Model-View-ViewModel)", is_correct=False)

    # Question 2
    q2 = Question.objects.create(
        course=course1,
        lesson=lesson2,
        content="Which Django command executes database migrations?",
        grade=25
    )
    Choice.objects.create(question=q2, content="python manage.py makemigrations", is_correct=False)
    Choice.objects.create(question=q2, content="python manage.py migrate", is_correct=True)
    Choice.objects.create(question=q2, content="python manage.py runserver", is_correct=False)

    # Question 3
    q3 = Question.objects.create(
        course=course1,
        lesson=lesson2,
        content="Which model field represents many-to-many relationships in Django?",
        grade=25
    )
    Choice.objects.create(question=q3, content="models.ManyToManyField", is_correct=True)
    Choice.objects.create(question=q3, content="models.ForeignKey", is_correct=False)
    Choice.objects.create(question=q3, content="models.OneToOneField", is_correct=False)

    # Question 4
    q4 = Question.objects.create(
        course=course1,
        lesson=lesson3,
        content="Which template tag is essential inside POST forms for CSRF protection?",
        grade=25
    )
    Choice.objects.create(question=q4, content="{% csrf_token %}", is_correct=True)
    Choice.objects.create(question=q4, content="{{ csrf_protection }}", is_correct=False)
    Choice.objects.create(question=q4, content="{% security_token %}", is_correct=False)

    print("Enrolling student and creating sample submission...")
    enrollment, _ = Enrollment.objects.get_or_create(user=student_user, course=course1, defaults={'mode': 'honor'})
    enrollment_admin, _ = Enrollment.objects.get_or_create(user=admin_user, course=course1, defaults={'mode': 'honor'})

    Submission.objects.filter(enrollment=enrollment).delete()
    submission = Submission.objects.create(enrollment=enrollment)
    for q in [q1, q2, q3, q4]:
        correct_choice = q.choice_set.filter(is_correct=True).first()
        if correct_choice:
            submission.choices.add(correct_choice)
    submission.save()

    print(f"Sample data populated successfully! Submission ID: {submission.id}")

if __name__ == '__main__':
    populate()
