from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Choice, Course, Enrollment, Lesson, Question, Submission


class OnlineCourseExamTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('student1', password='test-password-9876')
        self.other = User.objects.create_user('student2', password='test-password-9876')
        self.course = Course.objects.create(name='Test Django', description='Sample course')
        self.lesson = Lesson.objects.create(title='Basics', course=self.course, content='Basics')
        self.question = Question.objects.create(lesson=self.lesson, question_text='Correct?', grade=10)
        self.correct = Choice.objects.create(question=self.question, choice_text='Yes', is_correct=True)
        self.wrong = Choice.objects.create(question=self.question, choice_text='No', is_correct=False)
        Enrollment.objects.create(user=self.user, course=self.course)

    def test_admin_models_and_exam_page(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse('onlinecourse:course_details', args=[self.course.id]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Course exam')
        self.assertContains(r, 'Correct?')

    def test_pass_and_selected_answer(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse('onlinecourse:submit', args=[self.course.id]),
                             {f'choice_{self.correct.id}': str(self.correct.id)})
        self.assertEqual(r.status_code, 302)
        s = Submission.objects.get()
        self.assertEqual(s.choices.count(), 1)
        result = self.client.get(r.url)
        self.assertContains(result, 'Congratulations!')
        self.assertContains(result, '100.0%')

    def test_wrong_answer_and_another_user_cannot_read_results(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse('onlinecourse:submit', args=[self.course.id]),
                             {f'choice_{self.wrong.id}': str(self.wrong.id)})
        self.assertContains(self.client.get(r.url), 'Keep practicing!')
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(r.url).status_code, 404)

    def test_unenrolled_user_cannot_submit(self):
        self.client.force_login(self.other)
        r = self.client.post(reverse('onlinecourse:submit', args=[self.course.id]),
                             {f'choice_{self.correct.id}': str(self.correct.id)})
        self.assertEqual(r.status_code, 404)

    def test_ignores_other_course_choices(self):
        another = Course.objects.create(name='Other', description='Other course')
        lesson2 = Lesson.objects.create(title='Other lesson', course=another, content='...')
        q2 = Question.objects.create(lesson=lesson2, question_text='Other?')
        outsider = Choice.objects.create(question=q2, choice_text='Illegal', is_correct=True)
        self.client.force_login(self.user)
        self.client.post(reverse('onlinecourse:submit', args=[self.course.id]),
                         {f'choice_{outsider.id}': str(outsider.id)})
        self.assertEqual(Submission.objects.get().choices.count(), 0)
