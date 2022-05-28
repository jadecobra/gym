def encode(a_string):
    if not a_string:
        return []
    count = 1
    previous = ""
    result = []
    for character in a_string:
        if character != previous:
            if previous:
                entry = (previous, count)
                result.append(entry)
            count = 1
            previous = character
        else:
            count += 1
    result.append((character, count))
    return result

def decode(a_list):
    result = ""
    for character, count in a_list:
        result += character * count
    return result