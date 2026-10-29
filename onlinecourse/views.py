from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-total_enrollment')[:10]


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not request.user.is_authenticated:
        return redirect('onlinecourse:login')

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'mode': 'audit'}
    )
    if created:
        course.total_enrollment += 1
        course.save()
    return redirect('onlinecourse:course_details', course_id=course.id)


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not request.user.is_authenticated:
        return redirect('onlinecourse:login')

    # Get or create enrollment
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)

    if request.method == 'POST':
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                try:
                    selected_choice_ids.append(int(value))
                except (ValueError, TypeError):
                    pass
            elif key == 'choice':
                choice_list = request.POST.getlist('choice')
                for c in choice_list:
                    try:
                        selected_choice_ids.append(int(c))
                    except (ValueError, TypeError):
                        pass

        for c in request.POST.getlist('selected_choices'):
            try:
                selected_choice_ids.append(int(c))
            except (ValueError, TypeError):
                pass

        # Remove duplicates
        selected_choice_ids = list(set(selected_choice_ids))

        # Create submission
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_choice_ids:
            try:
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
            except Choice.DoesNotExist:
                pass
        submission.save()

        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

    return redirect('onlinecourse:course_details', course_id=course.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_choices = submission.choices.all()
    selected_ids = [c.id for c in selected_choices]

    # Retrieve all questions related to this course
    questions = Question.objects.filter(course=course).distinct()
    if not questions.exists():
        questions = Question.objects.filter(lesson__course=course).distinct()
    if not questions.exists():
        questions = Question.objects.all()

    total_score = 0
    possible = 0
    question_results = []

    for question in questions:
        possible += question.grade
        is_correct = question.is_get_score(selected_ids)
        if is_correct:
            total_score += question.grade

        question_results.append({
            'question': question,
            'is_correct': is_correct,
            'grade': question.grade if is_correct else 0,
            'choices': question.choice_set.all(),
        })

    grade = int((total_score / possible) * 100) if possible > 0 else 100
    passed = grade >= 60

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'total_score': total_score,
        'possible': possible,
        'max_score': possible,
        'grade': grade,
        'score': grade,
        'passed': passed,
        'question_results': question_results,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('onlinecourse:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'onlinecourse/login.html', {'form': form})


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def registration_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'onlinecourse/registration.html', {'form': form})
