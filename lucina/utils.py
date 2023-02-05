def ordered_enum(enum_cls):
    for i, value in enumerate(enum_cls):
        value.rank = i
    return enum_cls
