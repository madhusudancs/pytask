import string,random

def get_key():
    """ return a 10 character random key.
    """
    
    return ''.join([ random.choice(string.uppercase+string.digits) for i in range(10)])

