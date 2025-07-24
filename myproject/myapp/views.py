import string
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from myapp.models import User, InviteActivation
import random


def get_ref():
    while True:
        ref = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not User.objects.filter(ref_code=ref).exists():
            return ref

def get_key(request):
    chars = string.digits
    result = []
    for _ in range(4):
        result.append(random.choice(chars))
    print(f'🗝️ Юзер-ключ: {"".join(result)}')
    return JsonResponse({
        'status': 'success',
        'key': ''.join(result)
    })

def auth_form(request):
    if 'user_id' in request.session:
        return redirect('index')
    return render(request, 'auth.html')

@require_POST
def unified_auth(request):

    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        number_phone = request.POST.get('number_phone')
        user_key = request.POST.get('user_key', '').strip()
        right_key = request.POST.get('right_key', '').strip()

        print(f"""
        {'~' * 25}
        👤 Юзернейм:   {username}
        🔑 Пароль:     {password}
        📞 Телефон:    {number_phone}
        🗝️ Юзер-ключ:  {user_key}
        ✅ Верный ключ: {right_key}
        {'~' * 25}
        """)
        if not all([username, password, number_phone]):
            return JsonResponse({'status': 'error', 'message': 'Не все поля заполнены'}, status=400)

        if user_key != right_key:
            return JsonResponse({'status': 'error', 'message': 'Неверный код'}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            user.number_phone = number_phone
            user.save(update_fields=['number_phone'])
            login(request, user)
            return JsonResponse({'status': 'success'})

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                number_phone=number_phone,
                ref_code=get_ref()
            )
            login(request, user)
            return JsonResponse({'status': 'success'})

        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'Пользователь уже существует'}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': 'Системная ошибка'}, status=500)


def profile_page(request):
    context = {
        'phone': request.user.number_phone,
        'my_invite_code': request.user.ref_code,
        'invited_users': User.objects.filter(
            invited__inviter=request.user
        ).values_list('number_phone', flat=True)
    }

    try:
        context['inviter'] = InviteActivation.objects.get(
            invited=request.user
        ).inviter.number_phone
    except InviteActivation.DoesNotExist:
        context['inviter'] = None

    return render(request, 'profile.html', context)


@login_required
@require_POST
def add_inviter(request):
    inviter_code = request.POST.get('inviter', '').strip()
    print(f'{inviter_code} инвайт код')
    if not inviter_code:
        return JsonResponse({
            'status': 'error',
            'message': 'Введите инвайт-код'
        }, status=400)

    if len(inviter_code) != 6:
        return JsonResponse({
            'status': 'error',
            'message': 'Код должен содержать 6 символов'
        }, status=400)

    try:

        inviter = User.objects.get(ref_code=inviter_code)
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Инвайт-код не найден'
        }, status=404)

    if inviter.id == request.user.id:
        return JsonResponse({
            'status': 'error',
            'message': 'Нельзя использовать свой собственный код'
        }, status=400)

    if InviteActivation.objects.filter(invited=request.user).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Вы уже активировали инвайт-код'
        }, status=400)

    InviteActivation.objects.create(
        inviter=inviter,
        invited=request.user
    )

    request.user.inviter = inviter
    request.user.save()

    return JsonResponse({
        'status': 'success',
        'message': f'Вы успешно активировали код пользователя {inviter.username}!',
        'inviter_username': inviter.username,
        'inviter_phone': inviter.number_phone or ''
    })

