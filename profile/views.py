from django.shortcuts import render_to_response, redirect

from django.contrib.auth.decorators import login_required

@login_required
def view_profile(request):

    user = request.user

    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }
    return render_to_response("/profile/view.html", context)
