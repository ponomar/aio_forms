from aio_forms.fields.string_field import StringField


class HiddenField(StringField):
    type = input_type = 'hidden'
