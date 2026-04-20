from django.contrib import admin
from .models import (
    User, Simulation, SimulationResult, Feedback,
    Roadmap, RoadmapTask, InterviewQuestion
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'experience_level', 'main_stack', 'created_at')
    search_fields = ('email', 'full_name')
    list_filter = ('experience_level', 'main_stack')


# ====================== СИМУЛЯЦИИ ======================
@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('simulation_id', 'user', 'type', 'level', 'stack', 'status', 'overall_score', 'started_at')
    list_filter = ('status', 'type', 'level')
    search_fields = ('user__email', 'stack')
    actions = ['delete_all']

    def delete_all(self, request, queryset):
        Simulation.objects.all().delete()
        self.message_user(request, "Все симуляции успешно удалены.")
    delete_all.short_description = "Удалить ВСЕ симуляции"


# ====================== РЕЗУЛЬТАТЫ СИМУЛЯЦИЙ ======================
@admin.register(SimulationResult)
class SimulationResultAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'simulation', 'overall_score', 'created_at')
    search_fields = ('simulation__user__email',)
    actions = ['delete_all']

    def delete_all(self, request, queryset):
        SimulationResult.objects.all().delete()
        self.message_user(request, "Все результаты симуляций успешно удалены.")
    delete_all.short_description = "Удалить ВСЕ результаты"


# ====================== ОБРАТНАЯ СВЯЗЬ ======================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'result', 'created_at')
    search_fields = ('result__simulation__user__email',)
    actions = ['delete_all']

    def delete_all(self, request, queryset):
        Feedback.objects.all().delete()
        self.message_user(request, "Все отзывы успешно удалены.")
    delete_all.short_description = "Удалить ВСЕ отзывы"


# ====================== ВОПРОСЫ ======================
@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_type_display', 'get_level_display', 'get_stack_display',
                    'difficulty', 'correct_answer', 'created_at')
    list_filter = ('type', 'level', 'stack', 'difficulty')
    search_fields = ('title', 'description')
    ordering = ('type', 'level', 'stack', '-difficulty')
    actions = ['delete_all']

    def delete_all(self, request, queryset):
        InterviewQuestion.objects.all().delete()
        self.message_user(request, "Все вопросы успешно удалены.")
    delete_all.short_description = "Удалить ВСЕ вопросы"

    fieldsets = [
        ('Основная информация', {
            'fields': ('type', 'level', 'stack', 'title', 'description')
        }),
        ('Варианты ответов', {
            'fields': ('options', 'correct_answer'),
        }),
        ('Дополнительно', {
            'fields': ('difficulty',),
            'classes': ('collapse',),
        }),
    ]

    def get_type_display(self, obj):
        return obj.get_type_display()
    get_type_display.short_description = 'Тип'

    def get_level_display(self, obj):
        return obj.get_level_display()
    get_level_display.short_description = 'Уровень'

    def get_stack_display(self, obj):
        return obj.get_stack_display()
    get_stack_display.short_description = 'Стек'


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('roadmap_id', 'user', 'start_date', 'end_date', 'status')
    list_filter = ('status',)


@admin.register(RoadmapTask)
class RoadmapTaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'roadmap', 'title', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)