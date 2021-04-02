def decode_line(line):
    from decoder import mi_enb_decoder
    return [mi_enb_decoder(line).get_type_id()]


def message_count(m):
    return m, 1


def update_count(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)
