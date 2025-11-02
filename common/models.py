from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    number = models.CharField(max_length=10)

    def __str__(self):
        return f'Room {self.number}'


class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name='classes')

    def __str__(self):
        return f'School Class {self.name}'


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Subject {self.name}'


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return f'Lesson {self.name}'


class Homework(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='homeworks')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_homeworks')

    def __str__(self):
        return f'Homework: {self.name or "(no name)"}'


class HomeworkSubmission(models.Model):
    content = models.TextField(blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_submissions')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('homework', 'student')

    def __str__(self):
        return f'Submission by {self.student.username} for {self.homework.name}'


class Grade(models.Model):
    grade = models.IntegerField()
    feedback = models.TextField(blank=True)
    submission = models.OneToOneField(HomeworkSubmission, on_delete=models.CASCADE, related_name='grade', null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades_given')
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Grade {self.grade} for {self.submission.student.username}'