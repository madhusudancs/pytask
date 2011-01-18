from pytask.profile.forms import CreateProfileForm

from registration.signals import user_registered


def user_created(sender, user, request, **kwargs):
    data = request.POST.copy()
    data.update({
      "user": user.id,
      })
    form = CreateProfileForm(data)
    form.save()


user_registered.connect(user_created)
