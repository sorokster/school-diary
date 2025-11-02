from django.urls import path

from teacher.views import (SubjectView, SubjectDetailView, LessonView, LessonDetailView,
                           HomeworkView, HomeworkDetailView,
                           ClassView, ClassDetailView, RoomView, RoomDetailView, GradeView)

urlpatterns = [
    # Rooms
    path('rooms/', RoomView.as_view(), name='teacher-room-list'),
    path('rooms/<int:room_id>/', RoomDetailView.as_view(), name='teacher-room-detail'),

    # Classes
    path('classes/', ClassView.as_view(), name='teacher-class-list'),
    path('classes/<int:class_id>/', ClassDetailView.as_view(), name='teacher-class-detail'),

    # Subjects
    path('subjects/', SubjectView.as_view(), name='teacher-subject-list'),
    path('subjects/<int:subject_id>/', SubjectDetailView.as_view(), name='teacher-subject-detail'),

    # Lessons
    path('lessons/', LessonView.as_view(), name='teacher-lesson-list'),
    path('lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='teacher-lesson-detail'),

    # Homeworks
    path('lessons/<int:lesson_id>/homeworks/', HomeworkView.as_view(), name='teacher-lesson-homework-list'),
    path('lessons/<int:lesson_id>/homeworks/<int:homework_id>/', HomeworkDetailView.as_view(), name='teacher-lesson-homework-detail'),

    # Grade
    path('homeworks/<int:homework_id>/grade/', GradeView.as_view(), name='teacher-set-homework-grade'),
]
