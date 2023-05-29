import re

from django.core.exceptions import ValidationError


def unique_number_validator(value):
    pattern = r'^\d{4}[A-Z]$'

    if not re.match(pattern, value):
        raise ValidationError(
            'Unique number should consist of 4 digits between 1000 and 9999 followed by a Latin uppercase '
            'letter. '
        )

    digits = int(value[:4])
    if digits < 1000 or digits > 9999:
        raise ValidationError(
            'Unique number should be between 1000 and 9999.'
        )
