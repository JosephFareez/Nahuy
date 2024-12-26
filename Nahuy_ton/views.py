import hashlib
import hmac
import time
from django.shortcuts import render, redirect
from django.conf import settings
from .models import UserProfile, Task

def validate_telegram_auth(data, bot_token):
    check_hash = data.pop("hash")
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return check_hash == calculated_hash and (time.time() - int(data.get("auth_date", 0))) < 86400

def telegram_login(request):
    telegram_data = request.GET.dict()
    if not validate_telegram_auth(telegram_data, settings.BOT_TOKEN):
        return render(request, "error.html", {"message": "Telegram authentication failed."})

    telegram_id = telegram_data["id"]
    username = telegram_data.get("username", None)

    user_profile, _ = UserProfile.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={"username": username}
    )
    request.session["user_id"] = user_profile.id
    return redirect("index")

def index(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("telegram_login")
    user = UserProfile.objects.get(id=user_id)
    tasks = Task.objects.filter(assigned_user=user)
    context = {
        "user": user,
        "tasks": tasks,
        "site_link": "https://nahuy.online"
    }
    return render(request, "index.html", context)

def user_profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("telegram_login")
    user = UserProfile.objects.get(id=user_id)
    return render(request, "user_profile.html", {"user": user})
