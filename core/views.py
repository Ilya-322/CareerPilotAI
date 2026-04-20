from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from .forms import SimulationForm, ProfileForm, RegisterForm
from .models import Simulation, InterviewQuestion, SimulationResult
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now, timedelta

@login_required
def dashboard_view(request):
    # Только завершённые симуляции пользователя
    user_simulations = Simulation.objects.filter(
        user=request.user,
        status='completed'
    ).order_by('-started_at')

    # Количество симуляций на этой неделе (только завершённых)
    week_ago = now() - timedelta(days=7)
    simulations_this_week = user_simulations.filter(started_at__gte=week_ago).count()

    # Последние 5 завершённых симуляций
    recent_simulations = user_simulations[:5]

    return render(request, 'dashboard.html', {
        'simulations_this_week': simulations_this_week,
        'recent_simulations': recent_simulations,
    })


# Создание новой симуляции
@login_required
def create_simulation(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save(commit=False)
            simulation.user = request.user
            simulation.status = 'in_progress'
            simulation.save()
            return redirect('simulation', simulation_id=simulation.simulation_id)
        else:
            print("Форма невалидна!")
            print(form.errors)
    else:
        form = SimulationForm()

    return render(request, 'create_simulation.html', {'form': form})


# Экран прохождения симуляции
@login_required
def simulation_view(request, simulation_id):
    simulation = get_object_or_404(Simulation, simulation_id=simulation_id, user=request.user)

    questions = InterviewQuestion.objects.filter(
        type=simulation.type,
        level=simulation.level,
        stack=simulation.stack
    ).order_by('difficulty')[:10]

    if not questions.exists():
        questions = InterviewQuestion.objects.filter(
            type=simulation.type,
            level=simulation.level
        ).order_by('difficulty')[:10]

    return render(request, 'simulation.html', {
        'simulation': simulation,
        'questions': questions,
    })


# Профиль пользователя
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


# Экран результатов симуляции
@login_required
def results_view(request, simulation_id):
    simulation = get_object_or_404(Simulation, simulation_id=simulation_id, user=request.user)

    # === ЖЁСТКОЕ ИСПРАВЛЕНИЕ: меняем статус ===
    if simulation.status != 'completed':
        simulation.status = 'completed'
        simulation.completed_at = now()
        simulation.overall_score = 0  # пока заглушка, позже посчитаем
        simulation.save()

    # Получаем вопросы
    questions = InterviewQuestion.objects.filter(
        type=simulation.type,
        level=simulation.level,
        stack=simulation.stack
    ).order_by('difficulty')[:10]

    if not questions.exists():
        questions = InterviewQuestion.objects.filter(
            type=simulation.type,
            level=simulation.level
        ).order_by('difficulty')[:10]

    answers = request.session.get(f'answers_{simulation_id}', {})

    correct_count = 0
    review = []

    for q in questions:
        user_answer = answers.get(str(q.question_id), None)
        is_correct = (user_answer == q.correct_answer)

        if is_correct:
            correct_count += 1

        review.append({
            'question': q.description,
            'user_answer': user_answer or '—',
            'correct_answer': q.correct_answer,
            'correct': is_correct
        })

    overall_score = int((correct_count / len(questions)) * 100) if questions else 0

    # Обновляем оценку
    SimulationResult.objects.update_or_create(
        simulation=simulation,
        defaults={
            'overall_score': overall_score,
            'category_scores': {"total": overall_score}
        }
    )

    return render(request, 'results.html', {
        'simulation': simulation,
        'review': review,
        'correct_count': correct_count,
        'total_questions': len(questions),
    })


@csrf_exempt
@login_required
def save_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            simulation_id = data.get('simulation_id')
            question_id = data.get('question_id')
            answer = data.get('answer')

            key = f'answers_{simulation_id}'
            answers = request.session.get(key, {})
            answers[question_id] = answer
            request.session[key] = answers
            request.session.modified = True

            return JsonResponse({'status': 'ok'})
        except:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)