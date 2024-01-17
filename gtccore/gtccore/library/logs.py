from django.forms.models import model_to_dict
from accounts.models import User, UserLog

def log_user_activity(user: User, action: str, pre_object = None, post_object = None):
    """Log user activity."""
    UserLog.objects.create(
        user=user,
        action=action,
        pre_object= model_to_dict(pre_object) if pre_object else {},
        post_object= model_to_dict(post_object) if post_object else {},
    )
