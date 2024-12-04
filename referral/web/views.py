from django.contrib.auth import get_user_model, login
from django.db.models import Count, Prefetch
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CodeForm, InviteCodeForm, PhoneForm
from .utils import (
    activate_invite_code,
    generate_auth_code,
    get_page_number,
    paginate_queryset
)

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        referrals_queryset = User.objects.all()
        users_invite_count = User.objects.prefetch_related(
            Prefetch('referrals', queryset=referrals_queryset)
        ).annotate(
            activated_invites_count=Count('referrals')
        )

        users_with_invites = [
            {
                'user': user,
                'invite_code': user.invite_code,
                'activated_invites_count': user.activated_invites_count,
            }
            for user in users_invite_count
        ]

        page_number = get_page_number(request)
        page_obj = paginate_queryset(
            users_with_invites, page_number, per_page=5
        )

        return render(request, 'index.html', {'page_obj': page_obj})

    return render(request, 'index.html')


@require_http_methods(['GET', 'POST'])
def auth_view(request):
    form = PhoneForm(request.POST or None)

    if form.is_valid():
        phone = form.cleaned_data['phone']
        request.session['phone'] = phone
        request.session['code'] = generate_auth_code()
        request.session.set_expiry(180)
        return redirect('verify')

    return render(request, 'auth.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def verify_view(request):

    if not all(key in request.session for key in ('phone', 'code')):
        return redirect('auth')

    form = CodeForm(request.POST or None)
    code = request.session.get('code')

    if form.is_valid():
        if form.cleaned_data['code'] == code:
            phone = request.session.pop('phone')
            request.session.pop('code')
            user, _ = User.objects.get_or_create(phone_number=phone)
            login(request, user)
            return redirect('profile')
        else:
            form.add_error('code', 'Неверный код, пробуйте еще')

    return render(request, 'verify.html', {'form': form, 'code': code})


@require_http_methods(['GET', 'POST'])
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    user = request.user
    form = InviteCodeForm(request.POST or None)
    invite_code_activated = bool(user.referred_by)
    activated_invite_code = (
        user.referred_by.invite_code if user.referred_by else None
    )
    message = None

    if request.method == 'POST':
        if 'remove_invite_code' in request.POST:
            user.referred_by = None
            user.save()
            invite_code_activated = False
            activated_invite_code = None
            form = InviteCodeForm()
            message = 'Инвайт-код удалён. Теперь можно ввести новый'
        elif form.is_valid():
            message = activate_invite_code(
                user, form.cleaned_data['invite_code']
            )
            if message == 'Инвайт-код активирован!':
                invite_code_activated = True
                activated_invite_code = form.cleaned_data['invite_code']
                form = None

    if user.referred_by:
        activated_invite_code = user.referred_by.invite_code

    referrals = user.referrals.select_related('referred_by').all()
    page_number = get_page_number(request)
    page_obj = paginate_queryset(referrals, page_number)

    context = {
        'user': user,
        'referrals_count': referrals.count(),
        'page_obj': page_obj,
        'invite_code_activated': invite_code_activated,
        'activated_invite_code': activated_invite_code,
        'form': form,
        'message': message,
    }

    return render(request, 'profile.html', context)
