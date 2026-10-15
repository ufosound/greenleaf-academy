from django.shortcuts import render, get_object_or_404, redirect
from .models import Lesson, Question, Answer, UserProgress
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lesson_list')
        else:
            return render(request, 'courses/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'courses/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'courses/register.html', {'error': 'Такой логин уже занят'})
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name)
        login(request, user)
        return redirect('lesson_list')
        
    return render(request, 'courses/register.html')


@login_required
def lesson_list(request):
    lessons = Lesson.objects.filter(is_active=True).order_by('order')
    total_lessons = lessons.count()
    
    completed_lessons_ids = UserProgress.objects.filter(
        user=request.user, 
        is_completed=True
    ).values_list('lesson_id', flat=True)
    
    completed_count = len(completed_lessons_ids)
    progress_percent = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0

    lessons_data = []
    next_available = True 
    
    for lesson in lessons:
        is_completed = lesson.id in completed_lessons_ids
        is_accessible = next_available or is_completed
        
        if is_completed:
            next_available = True
        elif is_accessible:
            next_available = False 
        else:
            next_available = False

        lessons_data.append({
            'lesson': lesson,
            'is_completed': is_completed,
            'is_accessible': is_accessible
        })

    return render(request, 'courses/lesson_list.html', {
        'lessons_data': lessons_data,
        'total_lessons': total_lessons,
        'completed_count': completed_count,
        'progress_percent': progress_percent
    })


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})


@login_required
def take_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()

        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                try:
                    selected_answer = Answer.objects.get(id=selected_answer_id)
                    if selected_answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass

        passed = (score / total_questions) >= 0.8 if total_questions > 0 else False

        if passed:
            UserProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={'is_completed': True}
            )
            return render(request, 'courses/success.html', {
                'lesson': lesson,
                'score': score,
                'total': total_questions
            })
        else:
            return render(request, 'courses/quiz.html', {
                'lesson': lesson,
                'questions': questions,
                'error': 'Вы допустили ошибки. Пожалуйста, повторите учебный материал и попробуйте снова.'
            })

    return render(request, 'courses/quiz.html', {
        'lesson': lesson,
        'questions': questions
    })


@login_required
def final_exam(request):
    lessons = Lesson.objects.filter(is_active=True).count()
    completed = UserProgress.objects.filter(user=request.user, is_completed=True).count()
    
    is_finished = (completed >= lessons) and lessons > 0
    
    return render(request, 'courses/final.html', {
        'is_finished': is_finished,
        'total': lessons,
        'completed': completed
    })


def contact_methodist(request):
    return render(request, 'courses/contact.html')


def logout_view(request):
    logout(request)
    return redirect('login')