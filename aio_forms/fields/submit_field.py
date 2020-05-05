from aio_forms.fields.base_field import Field


class SubmitField(Field):
    type = input_type = 'submit'

    def __init__(self, key=None, label=None, params=None):
        super().__init__(key=key, label=label, params=params)
