from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class AdminEmployeeCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    role = forms.ChoiceField(choices=User.Role.choices, required=True, initial=User.Role.EMPLOYEE)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].help_text = self.fields['username'].help_text.replace('Required. ', '')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            from .models import EmployeeProfile
            if not hasattr(user, 'profile'):
                EmployeeProfile.objects.create(user=user)
        return user

class AdminEmployeeUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

from .models import EmployeeDocument

class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500'}),
            'file': forms.ClearableFileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'})
        }

from .models import PerformanceFeedback

class PerformanceFeedbackForm(forms.ModelForm):
    class Meta:
        model = PerformanceFeedback
        fields = ['employee', 'comment', 'rating']
        widgets = {
            'employee': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition',
                'rows': 4,
                'placeholder': 'Share your feedback for this colleague or self-evaluation...'
            }),
            'rating': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Optionally limit to other employees or include self
            from accounts.models import User
            self.fields['employee'].queryset = User.objects.exclude(is_superuser=True)
            self.fields['employee'].label = "Review Recipient"

class HRPerformanceFeedbackForm(forms.ModelForm):
    class Meta:
        model = PerformanceFeedback
        fields = ['employee', 'comment', 'rating']
        widgets = {
            'employee': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition'}),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition',
                'rows': 4,
                'placeholder': 'Provide professional review for this employee...'
            }),
            'rating': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 transition'})
        }
