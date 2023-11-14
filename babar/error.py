class BabarError(Exception):
    pass


class ModelError(BabarError):
    pass


class NoTypeHintsDetected(BabarError):
    pass


class CannotConvertToPostgresException(BabarError):
    """Raise when the given Python object can't be directly transformed into a Postgres one, with the same semantics"""

    pass


class CannotTransformToPostgresType(BabarError):
    pass
