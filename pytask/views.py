from django.shortcuts import render_to_response

def show_msg(user, message, redirect_url=None, url_desc=None):
    """ simply redirect to homepage """

    return render_to_response('show_msg.html',{'user': user,
                                               'message': message,
                                               'redirect_url': redirect_url,
                                               'url_desc': url_desc})
