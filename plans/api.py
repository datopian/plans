from .models import get_user, UserPlan, Plan, get_plan


def get_permissions(service, userid):
    u_ = get_user(userid)
    user = next(u_)
    if user is None:
        p_ = get_plan('default')
        plan = next(p_)
    else:
        plan = user.plan
    if plan is None:
        return {
            'max_private_storage_mb': 100,
            'max_public_storage_mb': 100,
            'max_dataset_num': 100
        }

    if service == 'rawstore':
        token = {
            'max_private_storage_mb': plan.max_private_storage_mb,
            'max_public_storage_mb': plan.max_public_storage_mb
        }
    elif service=='source':
        token = {
            'max_dataset_num': plan.max_dataset_num
        }
    else:
        token = {}
    return token