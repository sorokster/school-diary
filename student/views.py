from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from SchoolDiary.decorators import group_required
from common.models import Homework, Lesson, SchoolClass, Subject, Grade, HomeworkSubmission


# ====================
# Classes
# ====================
class ClassView(View):
    @staticmethod
    @group_required('student')
    def get(request):
        try:
            current_school_class = SchoolClass.objects.filter(students=request.user).first()
        except Exception as e:
            current_school_class = None
            print(f"Error fetching class: {e}")

        return render(request, 'student/class.html', {
            'class': current_school_class,
        })


# ====================
# Subjects
# ====================
class SubjectView(View):
    @staticmethod
    @group_required('student')
    def get(request):
        try:
            current_student_class = SchoolClass.objects.filter(students__id=request.user.id).first()
            if not current_student_class:
                all_subjects = Subject.objects.none()
            else:
                all_subjects = Subject.objects.filter(lesson__school_class=current_student_class).distinct()
        except Exception as e:
            all_subjects = Subject.objects.none()
            print(f"Error fetching subjects: {e}")

        return render(request, 'student/subjects.html', {
            'subjects': all_subjects
        })


class SubjectDetailView(View):
    @staticmethod
    @group_required('student')
    def get(request, subject_id):
        try:
            current_subject = Subject.objects.get(pk=subject_id)
        except ObjectDoesNotExist:
            current_subject = None

        try:
            current_student_class = SchoolClass.objects.filter(students__id=request.user.id).first()
            if not current_student_class or not current_subject:
                all_lessons = Lesson.objects.none()
            else:
                all_lessons = Lesson.objects.filter(
                    school_class=current_student_class,
                    subject=current_subject
                ).distinct()
        except Exception as e:
            all_lessons = Lesson.objects.none()
            print(f"Error fetching lessons: {e}")

        return render(request, 'student/subject.html', {
            'subject': current_subject,
            'lessons': all_lessons,
        })


# ====================
# Lessons
# ====================
class LessonView(View):
    @staticmethod
    @group_required('student')
    def get(request, subject_id):
        try:
            current_subject = Subject.objects.get(pk=subject_id)
        except ObjectDoesNotExist:
            current_subject = None

        try:
            current_school_class = SchoolClass.objects.filter(students=request.user).first()
            if not current_school_class or not current_subject:
                all_lessons = Lesson.objects.none()
            else:
                all_lessons = Lesson.objects.filter(
                    school_class=current_school_class,
                    subject_id=subject_id
                ).select_related('subject', 'room', 'teacher')
        except Exception as e:
            all_lessons = Lesson.objects.none()
            print(f"Error fetching lessons: {e}")

        return render(request, 'student/lessons.html', {
            'lessons': all_lessons,
            'subject': current_subject,
        })


class LessonDetailView(View):
    @staticmethod
    @group_required('student')
    def get(request, subject_id, lesson_id):
        try:
            current_subject = Subject.objects.get(pk=subject_id)
        except ObjectDoesNotExist:
            current_subject = None

        try:
            current_lesson = Lesson.objects.get(pk=lesson_id)
        except ObjectDoesNotExist:
            current_lesson = None

        return render(request, 'student/lesson.html', {
            'lesson': current_lesson,
            'subject': current_subject,
        })


# ====================
# Homeworks
# ====================
class HomeworkView(View):
    @staticmethod
    @group_required('student')
    def get(request, lesson_id):
        try:
            current_lesson = Lesson.objects.select_related('school_class').get(pk=lesson_id)
        except ObjectDoesNotExist:
            current_lesson = None

        if not current_lesson:
            current_homeworks = Homework.objects.none()
        else:
            try:
                if not current_lesson.school_class.students.filter(id=request.user.id).exists():
                    current_homeworks = Homework.objects.none()
                else:
                    current_homeworks = Homework.objects.filter(lesson=current_lesson)
            except Exception as e:
                current_homeworks = Homework.objects.none()
                print(f"Error fetching homeworks: {e}")

        return render(request, 'student/homeworks.html', {
            'lesson': current_lesson,
            'homeworks': current_homeworks,
        })


class HomeworkDetailView(View):
    @staticmethod
    @group_required('student')
    def get(request, lesson_id, homework_id):
        current_lesson = Lesson.objects.get(pk=lesson_id)
        current_homework = Homework.objects.get(pk=homework_id, lesson=current_lesson)

        current_homework_submission = HomeworkSubmission.objects.filter(
            homework=current_homework,
            student=request.user
        ).select_related('homework').prefetch_related('grade').first()

        grade = current_homework_submission.grade if current_homework_submission and hasattr(current_homework_submission, 'grade') else None

        return render(request, 'student/homework.html', {
            'lesson': current_lesson,
            'homework': current_homework,
            'homework_submission': current_homework_submission,
            'grade': grade,
        })


class HomeworkSubmissionView(View):
    @staticmethod
    @group_required('student')
    def post(request, homework_id):
        current_homework = Homework.objects.get(pk=homework_id)
        current_lesson_id = current_homework.lesson.id

        submission = HomeworkSubmission(
            content=request.POST.get('content'),
            student=request.user,
            homework=current_homework
        )
        submission.save()

        return redirect(f'/student/lessons/{current_lesson_id}/homeworks/{homework_id}/')
