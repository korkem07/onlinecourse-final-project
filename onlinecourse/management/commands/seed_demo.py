"""Create sample data for a REAL working exam and screenshots."""
from datetime import date
from django.core.management.base import BaseCommand
from onlinecourse.models import Choice, Course, Lesson, Question


class Command(BaseCommand):
    help = 'Create one demonstration course with two questions'

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name='Introduction to Django',
            defaults={'description': 'Learn models, views, templates and Django basics.', 'pub_date': date.today()},
        )
        lesson, _ = Lesson.objects.get_or_create(
            course=course, order=0, title='Django basics',
            defaults={'content': 'Django is a Python web framework. An ORM maps Python models to database tables.'},
        )
        q1, _ = Question.objects.get_or_create(
            lesson=lesson, question_text='What is Django?', defaults={'grade': 50}
        )
        Choice.objects.get_or_create(question=q1, choice_text='A JavaScript library', defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q1, choice_text='A Python web framework', defaults={'is_correct': True})
        q2, _ = Question.objects.get_or_create(
            lesson=lesson, question_text='What does ORM help you do?', defaults={'grade': 50}
        )
        Choice.objects.get_or_create(question=q2, choice_text='Work with a database using Python objects', defaults={'is_correct': True})
        Choice.objects.get_or_create(question=q2, choice_text='Design electrical circuits', defaults={'is_correct': False})
        self.stdout.write(self.style.SUCCESS(f'Demo course ready (ID={course.id}).'))
        self.stdout.write('Correct answers: A Python web framework; Work with a database using Python objects.')
