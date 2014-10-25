from .models import Sortable


def get_is_sortable(objects):
    if objects:
        if issubclass(type(objects[0]), Sortable):
            if objects.count() > 1:
                return True
    return False


def check_model_is_sortable(cls):
    if cls:
        if issubclass(type(cls), Sortable):
            if cls.objects.count() > 1:
                return True
    return False
