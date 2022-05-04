def is_list(resource):
    return isinstance(resource, list)

def in_collection(value=None, collection=None, condition=True):
    return (value in string for string in collection if condition)

def in_text(value=None, text=None):
    return value in text

def resource_check(statement=None, target_value=None):
    try:
        if is_list(statement['Resource']):
            return (
                any(
                    in_collection(
                        value=target_value,
                        collection=statement['Resource']
                    )
                ) or (
                    in_text(value="*", text=statement['Resource']) and
                    (
                        in_collection(
                            value="s3:",
                            collection=statement['Action'],
                            condition=is_list(statement['Action']) else ("s3:" in statement['Action'])
                        )
                    )
                )
            )
        else:
            return (
                target_value in statement['Resource']
                or statement['Resource'] == "*"
            )
    except KeyError:
        if is_list(statement['NotResource']):
            return (
                any(
                    (
                        ("s3:" in item for item in statement['Action']) or
                        ( "*" in statement['Action'])
                    ) and (
                        target_value not in string for string in statement['NotResource']
                    )
                ) or (
                    ("*" in statement['NotResource']) and
                    ("s3:" not in item for item in statement['Action'])
                )
            )
        else:
            return (
                ("s3:" in item for item in statement['Action']) and
                (target_value not in statement['NotResource'])
            )