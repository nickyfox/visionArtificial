def label_to_int(string_label):
    if string_label == 'circulo': return 1
    if string_label == 'estrella': return 2
    if string_label == 'rayo': return 3
    else: raise Exception('unkown class_label')


def int_to_label(string_label):
    if string_label == 1: return 'circulo'
    if string_label == 2: return 'estrella'
    if string_label == 3: return 'rayo'
    if string_label == 4: return 'rectangle'
    else: raise Exception('unkown class_label')