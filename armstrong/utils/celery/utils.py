from django.db.models.loading import get_model


def model_to_tuple(model):
    return (model._meta.app_label, model._meta.module_name)


def tuple_to_model(t):
    return get_model(t[0], t[1])