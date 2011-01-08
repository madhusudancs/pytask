from pytask.profile.models import Profile
from pytask.profile.forms import CreateProfileForm

from registration.signals import user_registered

def user_created(sender, user, request, **kwargs):

    data = request.POST
    data.update({"user": user, "uniq_key": make_key(Profile)})
    form = CreateProfileForm(data)
    form.is_valid()
    form.save()

user_registered.connect(user_created)

