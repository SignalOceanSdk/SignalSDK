class IterableConstants(type):
    def __iter__(cls):
        return iter(
            [value for (key, value) in cls.__dict__.items()
                if not key.startswith('_') and key.isupper()])


def contains_caseless(pattern: str, target: str) -> bool:
    return bool(
        pattern is not None
        and target is not None
        and pattern.casefold() in target.casefold()
    )
