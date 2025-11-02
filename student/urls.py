from django.urls import path

from student.views import ClassView, SubjectView, SubjectDetailView, LessonView, LessonDetailView, HomeworkView, \
    HomeworkDetailView, HomeworkSubmissionView

urlpatterns = [
    # Class
    path('class/', ClassView.as_view(), name='student-class-detail'),

    # Subjects
    path('subjects/', SubjectView.as_view(), name='student-subject-list'),
    path('subjects/<int:subject_id>/', SubjectDetailView.as_view(), name='student-subject-detail'),

    # Lessons
    path('subjects/<int:subject_id>/lessons/', LessonView.as_view(), name='student-lesson-list'),
    path('subjects/<int:subject_id>/lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='student-lesson-detail'),

    # Homeworks
    path('lessons/<int:lesson_id>/homeworks/', HomeworkView.as_view(), name='student-homework-list'),
    path('lessons/<int:lesson_id>/homeworks/<int:homework_id>/', HomeworkDetailView.as_view(), name='student-homework-detail'),

    # Submission
    path('homeworks/<int:homework_id>/submission/', HomeworkSubmissionView.as_view(), name='student-submit-homework'),
]