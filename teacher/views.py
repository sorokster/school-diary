from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from SchoolDiary.decorators import group_required
from common.models import Subject, Lesson, SchoolClass, Room, Homework, HomeworkSubmission, Grade


# ====================
# Rooms
# ====================
class RoomView(View):
    @staticmethod
    @group_required('teacher')
    def get(request):
        all_rooms = Room.objects.all()
        return render(request, 'teacher/rooms.html', {'rooms': all_rooms})

    @staticmethod
    @group_required('teacher')
    def post(request):
        number = request.POST.get('number')
        if number:
            created_room = Room.objects.create(number=number)
            return redirect(f'/teacher/rooms/#room_{created_room.pk}/')
        return redirect('/teacher/rooms/')


class RoomDetailView(View):
    @staticmethod
    @group_required('teacher')
    def get(request, room_id):
        current_room = get_object_or_404(Room, pk=room_id)
        return render(request, 'teacher/room.html', {'room': current_room})


# ====================
# Classes
# ====================
class ClassView(View):
    @staticmethod
    @group_required('teacher')
    def get(request):
        all_classes = SchoolClass.objects.prefetch_related('students').all()
        all_students = User.objects.filter(groups__name='student')
        return render(request, 'teacher/classes.html', {
            'classes': all_classes,
            'students': all_students,
        })

    @staticmethod
    @group_required('teacher')
    def post(request):
        name = request.POST.get('name')
        student_ids = request.POST.getlist('students')
        if not name:
            return redirect('/teacher/classes/')

        all_students = User.objects.filter(id__in=[int(i) for i in student_ids])

        created_class = SchoolClass.objects.create(name=name)
        created_class.students.set(all_students)
        return redirect(f'/teacher/classes/#class_{created_class.pk}/')


class ClassDetailView(View):
    @staticmethod
    @group_required('teacher')
    def get(request, class_id):
        current_class = get_object_or_404(SchoolClass, pk=class_id)
        all_lessons = Lesson.objects.filter(school_class_id=class_id)
        return render(request, 'teacher/class.html', {
            'class': current_class,
            'lessons': all_lessons
        })


# ====================
# Subjects
# ====================
class SubjectView(View):
    @staticmethod
    @group_required('teacher')
    def get(request):
        all_subjects = Subject.objects.all()
        return render(request, 'teacher/subjects.html', {'subjects': all_subjects})

    @staticmethod
    @group_required('teacher')
    def post(request):
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        if not name:
            return redirect('/teacher/subjects/')

        created_subject = Subject.objects.create(name=name, description=description)
        return redirect(f'/teacher/subjects/#subject_{created_subject.pk}/')


class SubjectDetailView(View):
    @staticmethod
    @group_required('teacher')
    def get(request, subject_id):
        current_subject = get_object_or_404(Subject, pk=subject_id)
        return render(request, 'teacher/subject.html', {'subject': current_subject})


# ====================
# Lessons
# ====================
class LessonView(View):
    @staticmethod
    @group_required('teacher')
    def get(request):
        all_subjects = Subject.objects.all()
        current_subject = Subject.objects.filter(pk=request.GET.get('subject')).first()
        lessons = Lesson.objects.filter(teacher=request.user).select_related('subject', 'school_class', 'room')
        all_classes = SchoolClass.objects.all()
        all_rooms = Room.objects.all()

        return render(request, 'teacher/lessons.html', {
            'subject': current_subject,
            'subjects': all_subjects,
            'classes': all_classes,
            'lessons': lessons,
            'rooms': all_rooms,
        })

    @staticmethod
    @group_required('teacher')
    def post(request):
        try:
            school_class = SchoolClass.objects.get(pk=request.POST['class'])
            subject = Subject.objects.get(pk=request.POST['subject'])
            room = Room.objects.get(pk=request.POST['room'])
        except (SchoolClass.DoesNotExist, Subject.DoesNotExist, Room.DoesNotExist):
            return redirect('/teacher/lessons/')

        created_lesson = Lesson.objects.create(
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            subject=subject,
            teacher=request.user,
            school_class=school_class,
            room=room,
            date=request.POST.get('date'),
        )

        return redirect(f'/teacher/lessons/#lesson_{created_lesson.pk}/')


class LessonDetailView(View):
    @staticmethod
    @group_required('teacher')
    def get(request, lesson_id):
        lesson = get_object_or_404(Lesson.objects.select_related('subject', 'school_class'), pk=lesson_id)
        return render(request, 'teacher/lesson.html', {
            'lesson': lesson,
            'subject': lesson.subject,
            'class': lesson.school_class
        })


class LessonsBySubjectView(View):
    @staticmethod
    @group_required('teacher')
    def get(request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        all_lessons = Lesson.objects.filter(subject=subject)
        return render(request, 'teacher/lessons.html', {'lessons': all_lessons})


# ====================
# Homeworks
# ====================
class HomeworkView(View):
    @staticmethod
    @group_required('teacher')
    def get(request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id, teacher=request.user)
        homeworks = Homework.objects.filter(lesson=lesson)
        return render(request, 'teacher/homeworks.html', {
            'lesson': lesson,
            'homeworks': homeworks,
        })

    @staticmethod
    @group_required('teacher')
    def post(request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        if not description:
            return redirect(f'/teacher/lessons/{lesson_id}/homeworks/')

        created_homework = Homework.objects.create(
            lesson=lesson,
            title=title,
            description=description,
        )

        return redirect(f'/teacher/lessons/{lesson_id}/homeworks/#homework_{created_homework.pk}/')


class HomeworkDetailView(View):
    @staticmethod
    @group_required('teacher')
    def get(request, lesson_id, homework_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id, teacher=request.user)
        homework = get_object_or_404(Homework, pk=homework_id)
        all_students = lesson.school_class.students.all()

        submissions = HomeworkSubmission.objects.filter(homework=homework).select_related('student').prefetch_related(
            'grade')
        submissions_map = {s.student_id: s for s in submissions}

        for student in all_students:
            submission = submissions_map.get(student.id)
            student.submission = submission
            student.grade = submission.grade if submission and hasattr(submission, 'grade') else None

        return render(request, 'teacher/homework.html', {
            'lesson': lesson,
            'homework': homework,
            'students': list(all_students),
            'grades_range': range(1, 13),
        })


# ====================
# Grades
# ====================
class GradeView(View):
    @staticmethod
    @group_required('teacher')
    def post(request, homework_id):
        try:
            submission = HomeworkSubmission.objects.get(
                homework_id=homework_id,
                student_id=request.POST['student'],
            )
        except HomeworkSubmission.DoesNotExist:
            return redirect(f'/teacher/homeworks/{homework_id}/')

        grade_value = request.POST.get('grade')
        if not grade_value or not grade_value.isdigit():
            return redirect(f'/teacher/homeworks/{homework_id}/')

        created_grade = Grade(
            grade=int(grade_value),
            feedback=request.POST.get('feedback', ''),
            submission=submission,
            teacher=request.user,
        )
        created_grade.save()

        return redirect(f'/teacher/homeworks/{homework_id}/')