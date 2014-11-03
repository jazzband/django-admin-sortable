from .models import Sortable, SortableForeignKey


def get_is_sortable(objects):
    if objects:
        if issubclass(type(objects[0]), Sortable):
            if objects.count() > 1:
                return True
    return False


def is_self_referential(cls):
    cls_type = type(cls)
    sortable_subclass = issubclass(cls_type, Sortable)
    sortable_foreign_key_subclass = issubclass(cls_type, SortableForeignKey)
    if sortable_foreign_key_subclass and not sortable_subclass:
        return True
    return False


def check_model_is_sortable(cls):
    if cls:
        if is_self_referential(cls):
            objects = cls.model.objects
        else:
            objects = cls.objects

        if objects.count() > 1:
            return True
    return False
