def get_is_sortable(objects):
    if objects:
        if objects.count() > 1:
            return True
    return False
