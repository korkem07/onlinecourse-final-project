"""Tasks 5 and 6: exam submission and results, integrated with IBM views."""
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_POST

from .models import Choice, Course, Enrollment, Question, Submission

logger = logging.getLogger(__name__)


def registration_request(request):
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html')
    if request.method != 'POST':
        return HttpResponseBadRequest('Unsupported method')
    username = request.POST.get('username', '').strip()
    password = request.POST.get('psw', '')
    first_name = request.POST.get('firstname', '').strip()
    last_name = request.POST.get('lastname', '').strip()
    if not username or not password:
        return render(request, 'onlinecourse/user_registration_bootstrap.html',
                      {'message': 'Username and password are required.'}, status=400)
    if User.objects.filter(username=username).exists():
        return render(request, 'onlinecourse/user_registration_bootstrap.html',
                      {'message': 'User already exists.'}, status=409)
    user = User.objects.create_user(username=username, first_name=first_name,
                                    last_name=last_name, password=password)
    login(request, user)
    return redirect('onlinecourse:index')


def login_request(request):
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_login_bootstrap.html')
    if request.method != 'POST':
        return HttpResponseBadRequest('Unsupported method')
    user = authenticate(username=request.POST.get('username', ''),
                        password=request.POST.get('psw', ''))
    if user is not None:
        login(request, user)
        return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/user_login_bootstrap.html',
                  {'message': 'Invalid username or password.'}, status=401)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    return user.is_authenticated and Enrollment.objects.filter(user=user, course=course).exists()


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        courses = list(Course.objects.order_by('-total_enrollment')[:10])
        for course in courses:
            course.is_enrolled = check_if_enrolled(self.request.user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_enrolled'] = check_if_enrolled(self.request.user, self.object)
        return context


@login_required(login_url='/onlinecourse/login/')
@require_POST
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course, defaults={'mode': Enrollment.HONOR}
    )
    if created:
        course.total_enrollment = Enrollment.objects.filter(course=course).count()
        course.save(update_fields=['total_enrollment'])
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=[course.id]))


def extract_answers(request):
    """Collect choice IDs from checkbox inputs named 'choice_<id>'."""
    values = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            try:
                values.append(int(value))
            except (TypeError, ValueError):
                pass
    return values


@login_required(login_url='/onlinecourse/login/')
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    submitted_ids = extract_answers(request)
    # Ignore injected choice IDs belonging to other courses.
    allowed = Choice.objects.filter(pk__in=submitted_ids, question__lesson__course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(allowed)
    return redirect('onlinecourse:show_exam_result', course_id=course.id,
                    submission_id=submission.id)


@login_required(login_url='/onlinecourse/login/')
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission, pk=submission_id,
        enrollment__course=course, enrollment__user=request.user,
    )
    selected = set(submission.choices.values_list('id', flat=True))
    questions = Question.objects.filter(lesson__course=course).select_related('lesson').prefetch_related('choice_set')
    results = []
    score = 0
    max_score = 0
    for question in questions:
        question_choices = list(question.choice_set.all())
        selected_ids = {choice.id for choice in question_choices if choice.id in selected}
        is_correct = question.is_get_score(selected_ids)
        points = question.grade if is_correct else 0
        score += points
        max_score += question.grade
        results.append({
            'question': question,
            'choices': question_choices,
            'selected_ids': selected_ids,
            'correct': is_correct,
            'points': points,
        })
    grade = round((score / max_score) * 100, 1) if max_score else 0
    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course,
        'submission': submission,
        'grade': grade,
        'score': score,
        'max_score': max_score,
        'passed': bool(max_score) and grade >= 80,
        'results': results,
    })
