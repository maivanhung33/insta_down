def to_dict(data, owner, count=None):
    return dict(
        data=data,
        count=count,
        owner=owner)

def to_dict(username, password):
    return dict(
        username=username,
        password=password)
