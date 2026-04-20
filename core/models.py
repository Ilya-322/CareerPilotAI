from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid


# ====================== 1. USER ======================
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="ФИО")

    EXPERIENCE_CHOICES = [
        ('junior', 'Junior'),
        ('junior_plus', 'Junior+'),
        ('middle', 'Middle'),
    ]
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, verbose_name="Уровень разработчика")

    STACK_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript / TypeScript'),
        ('go', 'Go'),
        ('csharp', 'C#'),
        ('other', 'Другой'),
    ]
    main_stack = models.CharField(max_length=50, choices=STACK_CHOICES, verbose_name="Основной стек")

    target_position = models.CharField(max_length=150, blank=True, null=True, verbose_name="Целевая должность")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


# ====================== 2. SIMULATION ======================
class Simulation(models.Model):
    simulation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations')

    TYPE_CHOICES = [
        ('full', 'Полное интервью'),
        ('live_coding', 'Только Live-coding'),
        ('system_design', 'System Design'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип симуляции")

    duration_minutes = models.IntegerField(default=45, verbose_name="Длительность (мин)")
    stack = models.CharField(max_length=100, verbose_name="Стек технологий")

    LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('junior_plus', 'Junior+'),
        ('middle', 'Middle'),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Уровень сложности")

    started_at = models.DateTimeField(default=now, verbose_name="Время начала")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Время завершения")

    STATUS_CHOICES = [
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
        ('aborted', 'Прервана'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name="Статус")

    overall_score = models.IntegerField(null=True, blank=True, verbose_name="Общая оценка (%)")

    class Meta:
        verbose_name = "Симуляция"
        verbose_name_plural = "Симуляции"
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.email} — {self.get_type_display()} ({self.level})"


# ====================== 3. SIMULATION RESULT ======================
class SimulationResult(models.Model):
    result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE, related_name='result')

    overall_score = models.IntegerField(verbose_name="Общая оценка (%)")
    category_scores = models.JSONField(verbose_name="Оценки по категориям")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Результат симуляции"
        verbose_name_plural = "Результаты симуляций"

    def __str__(self):
        return f"Результат {self.simulation}"


# ====================== 4. FEEDBACK ======================
class Feedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    result = models.ForeignKey(SimulationResult, on_delete=models.CASCADE, related_name='feedbacks')

    weak_points = models.JSONField(verbose_name="Слабые места")
    recommendations = models.JSONField(verbose_name="Рекомендации")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратные связи"

    def __str__(self):
        return f"Feedback для {self.result}"


# ====================== 5. ROADMAP ======================
class Roadmap(models.Model):
    roadmap_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmaps')

    start_date = models.DateField(verbose_name="Дата начала плана")
    end_date = models.DateField(verbose_name="Дата окончания плана")

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус плана")

    class Meta:
        verbose_name = "Персональный план"
        verbose_name_plural = "Персональные планы"

    def __str__(self):
        return f"Roadmap для {self.user.email} ({self.start_date} — {self.end_date})"


# ====================== 6. ROADMAP TASK ======================
class RoadmapTask(models.Model):
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='tasks')

    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание задачи")
    is_completed = models.BooleanField(default=False, verbose_name="Выполнена ли задача")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата выполнения")

    class Meta:
        verbose_name = "Задача в плане"
        verbose_name_plural = "Задачи в плане"

    def __str__(self):
        return self.title


# ====================== 7. INTERVIEW QUESTION ======================
class InterviewQuestion(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    TYPE_CHOICES = [
        ('full', 'Полное интервью'),
        ('live_coding', 'Только Live-coding'),
        ('system_design', 'System Design'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип симуляции")

    LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('junior_plus', 'Junior+'),
        ('middle', 'Middle'),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Уровень")

    STACK_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript / TypeScript'),
        ('go', 'Go'),
        ('csharp', 'C#'),
        ('other', 'Другой'),
    ]
    stack = models.CharField(max_length=50, choices=STACK_CHOICES, verbose_name="Стек технологий")

    title = models.CharField(max_length=300, verbose_name="Заголовок вопроса")
    description = models.TextField(verbose_name="Текст вопроса / задача")

    # Новые поля для множественного выбора
    options = models.JSONField(default=list, verbose_name="Варианты ответов (A, B, C, D)")
    correct_answer = models.CharField(max_length=10, verbose_name="Правильный вариант (A, B, C или D)")

    difficulty = models.IntegerField(default=5, verbose_name="Сложность (1-10)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Вопрос для интервью"
        verbose_name_plural = "Вопросы для интервью"
        ordering = ['type', 'level', 'stack', 'difficulty']

    def __str__(self):
        return f"{self.get_type_display()} | {self.get_level_display()} | {self.get_stack_display()} | {self.title[:60]}..."