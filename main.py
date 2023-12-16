import random

default_block_len = 8
default_input_data = "Example data"


def add_check_bits(data, block_len):
    indexes = [i for i in range(1, block_len + 1) if not i & (i - 1)]

    for index in indexes:
        data = data[:index - 1] + "0" + data[index - 1:]

    res_data_len = len(data)
    for index in indexes:
        sum = 0
        for i in range(index - 1, res_data_len, index * 2):
            for _ in range(index):
                if i + _ >= res_data_len:
                    break
                sum += int(data[i + _])

        if sum % 2 != 0:
            data = data[:index - 1] + "1" + data[index:]

    return data


def data_to_bin(data):
    return ''.join(format(ord(_), '08b') for _ in data)


def blocks_iterator(data, block_len):
    for _ in range(0, len(data), block_len):
        yield data[_: _ + block_len]


def remove_check_bites(data, indexes):
    data_list = list(data)
    result = ''
    for i in range(len(data)):
        if (i + 1) in indexes:
            continue
        result += data_list[i]

    return result


def get_check_bits(data, indexes):
    check_bits = {}
    for i in range(1, len(data) + 1):
        if i in indexes:
            check_bits[i] = int(data[i - 1])
    return check_bits


def make_error(data, block_len):
    data_with_errors = ''
    for block in blocks_iterator(data, block_len):
        err_bit = random.randint(1, len(block))
        block = (block[:err_bit - 1] +
                 str((int(block[err_bit - 1]) + 1) % 2) +
                 block[err_bit:])
        data_with_errors += block
    return data_with_errors


def find_and_fix_errors(data, indexes, block_len):
    check_bits_dict = get_check_bits(data, indexes)
    cleaned_data = remove_check_bites(data, indexes)
    encoded_again_data = add_check_bits(cleaned_data, block_len)
    real_check_bits_dict = get_check_bits(encoded_again_data, indexes)

    if check_bits_dict != real_check_bits_dict:
        error_bit_position = 0
        for index, value in check_bits_dict.items():
            if real_check_bits_dict[index] != value:
                error_bit_position += index
        fixed_data = (data[:error_bit_position - 1] +
                      str((int(data[error_bit_position - 1]) + 1) % 2) +
                      data[error_bit_position:])
        return fixed_data

    return data


def encode(data, block_len):
    encoded_data = ''
    data_bin = data_to_bin(data)

    for block in blocks_iterator(data_bin, block_len):
        block_with_check_bits = add_check_bits(block, block_len)
        encoded_data += block_with_check_bits

    return encoded_data


def decode(data, block_len, add_errors=0):
    indexes = [i for i in range(1, block_len + 1) if not i & (i - 1)]
    decoded_data = ''

    if add_errors:
        data = make_error(data, block_len + len(indexes))
        print("\nДобавляем помехи в закодированное значение: " + data)

    fixed_blocks = []
    for block in blocks_iterator(data, block_len + len(indexes)):
        fixed_block = find_and_fix_errors(block, indexes, block_len)
        fixed_blocks.append(fixed_block)

    decoded_blocks = []
    for block in fixed_blocks:
        decoded_block = remove_check_bites(block, indexes)
        decoded_blocks.append(decoded_block)

    for b in decoded_blocks:
        for c in [b[i:i + 8] for i in range(len(b)) if not i % 8]:
            decoded_data += chr(int(c, 2))
    return decoded_data


if __name__ == '__main__':
    print("Нажимайте Enter для подставления дефолтных значений")
    input_data = input("Введите данные (текст) для кодирования: ")
    if input_data == "":
        input_data = default_input_data

    block_l = input("Введите длину блока кодирования: ")
    if block_l == "":
        block_l = default_block_len
    block_l = int(block_l)

    encode_line = encode(input_data, block_l)
    print("\nЗакодированное значение: " + encode_line)

    decode_line = decode(encode_line, block_l)
    print("Декодированное обратно: " + decode_line)

    answers = {0: "Неверно", 1: "Верно"}
    print("Результат декодировки - " + answers[input_data == decode_line])

    # Добавляем помехи
    decode_with_errors_line = decode(encode_line, block_l, 1)
    print("Декодированное обратно: " + decode_with_errors_line)
    print("Результат декодировки - " + answers[input_data == decode_line])