def get_index(items, item):
    try:
        return items.index(item)
    except ValueError:
        return None
