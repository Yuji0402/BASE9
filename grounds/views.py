from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Ground, GroundReservation
from accounts.models import PREFECTURE_CHOICES


def _get_ground_form():
    from django import forms
    from .models import Ground

    class GroundForm(forms.ModelForm):
        class Meta:
            model = Ground
            fields = ('name', 'address', 'prefecture', 'city', 'lat', 'lng',
                      'description', 'surface', 'capacity', 'fee', 'phone', 'website')
            labels = {
                'name': 'グラウンド名', 'address': '住所', 'prefecture': '都道府県',
                'city': '市区町村', 'lat': '緯度', 'lng': '経度',
                'description': '説明・備考', 'surface': '種別', 'capacity': '収容人数',
                'fee': '使用料', 'phone': '電話番号', 'website': '公式サイト',
            }
            widgets = {
                'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for name, field in self.fields.items():
                if name != 'description':
                    if isinstance(field.widget, __import__('django').forms.Select):
                        field.widget.attrs.update({'class': 'form-select'})
                    else:
                        field.widget.attrs.update({'class': 'form-control'})
    return GroundForm


def _get_reservation_form():
    from django import forms
    from .models import GroundReservation

    class ReservationForm(forms.ModelForm):
        class Meta:
            model = GroundReservation
            fields = ('date', 'start_time', 'end_time', 'is_shared', 'note')
            labels = {
                'date': '予約日', 'start_time': '開始時間', 'end_time': '終了時間',
                'is_shared': 'グラウンドシェア可能', 'note': '備考',
            }
            widgets = {
                'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
                'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
                'note': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for name, field in self.fields.items():
                if name not in ('date', 'start_time', 'end_time', 'note'):
                    field.widget.attrs.update({'class': 'form-check-input'})
    return ReservationForm


def ground_list_view(request):
    grounds = Ground.objects.all()
    prefecture = request.GET.get('prefecture', '')
    q = request.GET.get('q', '')
    if prefecture:
        grounds = grounds.filter(prefecture=prefecture)
    if q:
        grounds = grounds.filter(Q(name__icontains=q) | Q(address__icontains=q))
    grounds_with_coords = grounds.exclude(lat=None).exclude(lng=None)
    grounds_geo = [
        {
            'id': g.id, 'name': g.name, 'lat': float(g.lat), 'lng': float(g.lng),
            'address': g.address, 'surface': g.surface, 'url': f'/grounds/{g.id}/'
        }
        for g in grounds_with_coords
    ]
    import json
    return render(request, 'grounds/ground_list.html', {
        'grounds': grounds,
        'grounds_geo_json': json.dumps(grounds_geo, ensure_ascii=False),
        'prefecture_choices': PREFECTURE_CHOICES,
        'selected_prefecture': prefecture,
        'q': q,
    })


def ground_detail_view(request, pk):
    ground = get_object_or_404(Ground, pk=pk)
    reservations = ground.reservations.filter(is_shared=True).order_by('date')
    ResForm = _get_reservation_form()
    form = ResForm()
    return render(request, 'grounds/ground_detail.html', {
        'ground': ground,
        'reservations': reservations,
        'form': form,
    })


@login_required
def ground_create_view(request):
    GroundForm = _get_ground_form()
    form = GroundForm(request.POST or None)
    if form.is_valid():
        ground = form.save(commit=False)
        ground.added_by = request.user
        ground.save()
        messages.success(request, 'グラウンドを登録しました！')
        return redirect('ground-detail', pk=ground.pk)
    return render(request, 'grounds/ground_form.html', {'form': form})


@login_required
def reservation_create_view(request, ground_pk):
    ground = get_object_or_404(Ground, pk=ground_pk)
    user_team = request.user.get_team()
    if not user_team:
        messages.warning(request, 'チームに所属してから予約を登録できます。')
        return redirect('ground-detail', pk=ground_pk)
    ResForm = _get_reservation_form()
    if request.method == 'POST':
        form = ResForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.ground = ground
            res.team = user_team
            res.save()
            messages.success(request, '予約情報を登録しました。')
            return redirect('ground-detail', pk=ground_pk)
    return redirect('ground-detail', pk=ground_pk)
