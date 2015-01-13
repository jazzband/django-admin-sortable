from .models import Sortable, SortableForeignKey


def check_inheritance(obj):
    return issubclass(type(obj), Sortable)


def get_is_sortable(objects):
    if objects:
        if check_inheritance(objects[0]):
            if objects.count() > 1:
                return True
    return False


def is_self_referential(cls):
    cls_type = type(cls)
    sortable_subclass = check_inheritance(cls_type)
    # sortable_subclass = issubclass(cls_type, Sortable)
    sortable_foreign_key_subclass = issubclass(cls_type, SortableForeignKey)
    if sortable_foreign_key_subclass and not sortable_subclass:
        return True
    return False


def check_model_is_sortable(cls):
    if cls:
        if check_inheritance(cls):
            if is_self_referential(cls):
                objects = cls.model.objects
            else:
                objects = cls.objects
            return get_is_sortable(objects.all())
    return False
