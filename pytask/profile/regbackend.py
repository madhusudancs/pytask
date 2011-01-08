from pytask.profile.models import Profile
from pytask.profile.forms import CreateProfileForm
from pytask.utils import make_key

from registration.signals import user_registered

def user_created(sender, user, request, **kwargs):

    data = request.POST.copy()
    data.update({"user": user.id, "uniq_key": make_key(Profile)})
    form = CreateProfileForm(data)
    form.save()

user_registered.connect(user_created)

