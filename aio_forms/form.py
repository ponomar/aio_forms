from copy import copy

from aio_forms.fields.base_field import Field, check_params
from aio_forms.fields.password_field import PasswordField


def _get_fields(form):
    fields, fields_keys = [], []
    for key in dir(form):
        value = getattr(form, key)
        if isinstance(value, Field):
            # We need to copy fields in form not to share their states between
            # different requests.
            value = copy(value)
            setattr(form, key, value)  # replace with copied one

            if not value.fld_key:
                value._set_key(key)

            fields.append(value)

            if value.key in fields_keys:
                raise ValueError(
                    'field with key `%s` already defined in %s '
                    'or it\'s parents' % (value.key, form)
                )

            fields_keys.append(value.key)

    fields.sort(key=lambda x: x._creation_counter)
    return tuple(fields)


class Form(object):
    fields = ()
    errors = None

    def __init__(self, formdata=None, object=None, params=None):
        check_params(params)

        self.object = object
        self.params = params
        self.fields = _get_fields(self)

        if formdata is not None:  # must be after fields assigning
            self.set_formdata(formdata)
        elif self.object:
            self.set_object_data()

    def set_formdata(self, formdata):
        for field in self.fields:
            field.set_value(formdata.get(field.key))

    def set_object_data(self):
        if (
            hasattr(self.object, 'get')
            and hasattr(self.object, 'keys')
            and hasattr(self.object, 'values')
            and hasattr(self.object, 'items')
        ):
            get_value = lambda x: self.object.get(x)
        else:
            get_value = lambda x: getattr(self.object, x, None)

        for field in self.fields:
            if not isinstance(field, PasswordField):
                field.set_value_from_object(get_value(field.key))

    async def validate(self):
        errors = {}
        for field in self.fields:
            valid = await field.validate(self)
            if not valid:
                errors[field.key] = field.error

        if not errors:
            errors = None

        self.errors = errors
        return not bool(self.errors)

    def schema(self):
        fields = [fld.schema() for fld in self.fields]

        result = dict(
            fields={f_['key']: f_ for f_ in fields},
            fields_keys=[f_['key'] for f_ in fields],
        )

        if self.params:
            params = dict()
            for k_, v_ in self.params.items():
                if callable(v_):
                    v_ = v_()

                params[k_] = v_

            result['params'] = params

        if self.errors:
            result['errors'] = self.errors

        return result
