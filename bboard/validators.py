import re

from django.core.exceptions import ValidationError


# class NoForbiddenCharsValidator:
#     def __init__(self, forbidden_chars=(' ',)):
#         self.forbidden_chars = forbidden_chars

#     def validate(self, password, user=None):
#         for fc in self.forbidden_chars:
#             if fc in password:
#                 raise ValidationError(
#                     f'Пароль не должен содержать недопустимые символы'
#                     f'{", ".join(self.forbidden_chars)}',
#                     code='forbiden_chars_present')

#     def get_help_text(self):
#         return (f"Пароль не должен содержать недопустимые символы"
#             f'{", ".join(self.forbidden_chars)}')


class CustomPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"Пароль должен быть не менее {self.min_length} символов.",
                code="password_too_short",
            )
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну заглавную букву.",
                code="password_no_uppercase",
            )
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну строчную букву.",
                code="password_no_lowercase",
            )
        if not re.search(r"\d", password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну цифру.",
                code="password_no_number",
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "Пароль должен содержать хотя бы один специальный символ.",
                code="password_no_special",
            )

    def get_help_text(self):
        return (
            "Ваш пароль должен содержать минимум 8 символов, включая "
            "заглавную букву, строчную букву, цифру и специальный символ."
        )
