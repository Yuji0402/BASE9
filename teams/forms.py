from django import forms
from .models import Team

ACTIVITY_DAY_OPTIONS = [
    '月曜', '火曜', '水曜', '木曜', '金曜', '土曜', '日曜', '祝日', '不定期'
]


class TeamForm(forms.ModelForm):
    activity_days = forms.MultipleChoiceField(
        label='活動曜日',
        choices=[(d, d) for d in ACTIVITY_DAY_OPTIONS],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Team
        fields = ('name', 'description', 'prefecture', 'city', 'level',
                  'activity_days', 'members_count', 'image', 'is_recruiting')
        labels = {
            'name': 'チーム名',
            'description': 'チーム紹介',
            'prefecture': '都道府県',
            'city': '市区町村',
            'level': 'レベル',
            'members_count': '現在のメンバー数',
            'image': 'チーム画像',
            'is_recruiting': 'メンバー募集中',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.activity_days:
            self.initial['activity_days'] = self.instance.activity_days.split(',')
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.CheckboxInput)):
                pass
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_activity_days(self):
        days = self.cleaned_data.get('activity_days', [])
        return ','.join(days)
