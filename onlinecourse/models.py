import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an issue importing models from django.db")

from django.conf import settings

# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username + "," + self.occupation


# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=100, default='online course')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True, blank=True)
    instructors = models.ManyToManyField(Instructor, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment', blank=True)
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title


# Enrollment model
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'beta'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=10, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return f"Enrollment: {self.user.username} in {self.course.name}"


# Question model
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return f"Question: {self.question_text}"

    # Method that calculates whether selected choices are all correct choices
    def is_get_score(self, selected_ids):
        all_answers = set(self.choice_set.filter(is_correct=True).values_list('id', flat=True))
        selected_ids_set = set(int(i) for i in selected_ids)
        selected_correct = set(self.choice_set.filter(is_correct=True, id__in=selected_ids_set).values_list('id', flat=True))
        selected_wrong = set(self.choice_set.filter(is_correct=False, id__in=selected_ids_set).values_list('id', flat=True))

        if all_answers == selected_correct and len(selected_wrong) == 0:
            return True
        return False


# Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.choice_text} (Correct: {self.is_correct})"


# Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.enrollment.user.username} on {self.enrollment.course.name}"
