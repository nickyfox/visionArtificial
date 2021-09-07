def label_to_int(string_label):
    if string_label == '1': return 1
    if string_label == '2': return 2
    if string_label == '3': return 3
    else: return 'unknown'


def int_to_label(string_label):
    if string_label == 1: return '1'
    if string_label == 2: return '2'
    if string_label == 3: return '3'
    else: return 'unknown'