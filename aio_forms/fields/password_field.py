from aio_forms.fields.string_field import StringField


class PasswordField(StringField):
    type = input_type = 'password'
