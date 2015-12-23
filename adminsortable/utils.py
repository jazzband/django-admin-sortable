from .models import SortableMixin, SortableForeignKey


def check_inheritance(cls):
    return issubclass(type(cls), SortableMixin)


def get_is_sortable(objects):
    if objects.count() < 2:
        return False

    if not check_inheritance(objects[:1][0]):
        return False

    return True


def is_self_referential(cls):
    cls_type = type(cls)
    sortable_subclass = check_inheritance(cls_type)
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
