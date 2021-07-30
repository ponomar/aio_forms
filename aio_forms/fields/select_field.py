from aio_forms.fields.base_field import Field, null


ERROR_NOT_IN_OPTIONS = 'Not a valid choice.'


class SelectField(Field):
    type = input_type = 'select'

    fld_options = None
    error_not_in_options = None

    def __init__(self, key=None, label=None, validators=None, default=None,
                 coerce=lambda x: x, required=False, required_error=None,
                 params=None, options=null, error_not_in_options=null):
        super().__init__(
            key=key,
            label=label,
            validators=validators,
            default=default,
            required=required,
            required_error=required_error,
            params=params,
            coerce=coerce,
        )

        self.set_options(options)

        if error_not_in_options is null:
            error_not_in_options = ERROR_NOT_IN_OPTIONS
        self.set_error_not_in_options(error_not_in_options)

    def set_error_not_in_options(self, value):
        self.error_not_in_options = value

    def set_options(self, value):
        self.fld_options = value

    def get_options_iterator(self):
        if callable(self.fld_options):
            result = self.fld_options()
        else:
            result = self.fld_options

        if result is null:
            result = ()

        return result

    @property
    def options(self):
        for key, label in self.get_options_iterator():
            selected = self.fld_coerce(key) == self.value
            yield [self.fld_coerce(key), label, selected]

    async def validate(self, form) -> bool:
        empty = self.value is None or self.value == []
        if empty and self.required:
            self.error = self.get_required_error()
            return False

        if not empty:
            if isinstance(self.value, list):
                value = set(self.value)
            else:
                value = {self.value}

            keys = {i[0] for i in self.options if i[0] is not None}
            if not (keys and keys.issuperset(value)):
                self.error = (
                    self.error_not_in_options()
                    if callable(self.error_not_in_options)
                    else self.error_not_in_options
                )
                return False

        return await super().validate(form)

    def schema(self) -> dict:
        result = super().schema()
        result['options'] = list(self.options)
        return result
