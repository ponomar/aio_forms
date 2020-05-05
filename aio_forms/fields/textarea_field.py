from aio_forms.fields.string_field import StringField


class TextAreaField(StringField):
    type = 'text'
    input_type = 'textarea'
