from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Simulation

# Форма для создания симуляции
class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['type', 'level', 'stack', 'duration_minutes']
        widgets = {
            'type': forms.RadioSelect(),
            'level': forms.RadioSelect(),
        }

    # Делаем duration_minutes динамическим
    duration_minutes = forms.ChoiceField(
        label="Длительность симуляции (минут)",
        widget=forms.Select(attrs={
            'class': 'w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-4 text-white focus:outline-none focus:border-emerald-500'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Дефолтные варианты (для Live Coding и System Design)
        self.fields['duration_minutes'].choices = [
            (30, '30 минут'),
            (35, '35 минут'),
            (40, '40 минут'),
            (45, '45 минут'),
            (50, '50 минут'),
            (55, '55 минут'),
            (60, '60 минут'),
        ]


# Форма регистрации
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user


# Форма редактирования профиля
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'experience_level', 'main_stack', 'target_position']
        widgets = {
            'experience_level': forms.RadioSelect(),
            'main_stack': forms.Select(),
        }