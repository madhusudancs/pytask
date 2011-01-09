from django.shortcuts import render_to_response

def show_msg(user, message, redirect_url=None, url_desc=None):
    """ simply redirect to homepage """

    return render_to_response('show_msg.html',{'user': user,
                                               'message': message,
                                               'redirect_url': redirect_url,
                                               'url_desc': url_desc})

def home_page(request):
    """ get the user and display info about the project if not logged in.
    if logged in, display info of their tasks.
    """

    user = request.user
    if not user.is_authenticated():
        return render_to_response("index.html")

    profile = user.get_profile()

    claimed_tasks = user.claimed_tasks.all()
    selected_tasks = user.selected_tasks.all()
    reviewing_tasks = user.reviewing_tasks.all()
    unpublished_tasks = user.created_tasks.filter(status="UP").all()
    can_create_task = True if profile.rights != "CT" else False

    context = {"user": user,
               "profile": profile,
               "claimed_tasks": claimed_tasks,
               "selected_tasks": selected_tasks,
               "reviewing_tasks": reviewing_tasks,
               "unpublished_tasks": unpublished_tasks,
               "can_create_task": can_create_task
              }

    return render_to_response("index.html", context)
