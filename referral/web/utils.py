import random

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

User = get_user_model()


def generate_auth_code():
    return str(random.randint(1000, 9999))


def paginate_queryset(queryset, page_number, per_page=5):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def get_page_number(request):
    return request.GET.get('page', 1)


def activate_invite_code(user, invite_code):
    if invite_code == user.invite_code:
        return 'Нельзя активировать свой собственный инвайт-код'

    referred_user = User.objects.filter(invite_code=invite_code).first()
    if referred_user:
        user.referred_by = referred_user
        user.save()
        return 'Инвайт-код активирован!'
    return 'Инвайт-код неверный'
