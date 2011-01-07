import string,random

def make_key(model_name):
    """ return a 10 character random key.
    """

    while True:
        key = ''.join([ random.choice(string.uppercase+string.digits) for i in range(10)])
        try:
            model_name.objects.get(uniq_key=key)
        except model_name.DoesNotExist:
            return key

