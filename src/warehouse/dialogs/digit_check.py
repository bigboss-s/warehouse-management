def digit_input_check(action, char):
    if action == '1':
        return char.isdigit()
    return True

def digit_dot_input_check(action, char):
    if action == '1':
        return char.isdigit() or char == '.'
    return True