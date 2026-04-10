from django.shortcuts import render

from apps.users.selectors.user_selectors import get_all_users


def user_list_view(request):
    users = get_all_users()

    return render(
        request,
        "users/user_list.html",
        {"users": users}
    )
