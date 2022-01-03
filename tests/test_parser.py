def test_parse_sequence():
    ps = ParserString("x(55, cat:-22.3)kskks(-9)")
    print(f"input:               '{ps.input_string}'")

    result = parse_sequence(ps)
    print(f"result, remaining:   {result}, '{ps.remaining}'")


def test_parse_event():
    ps = ParserString("x(55, 22, -9.66, dog:33, cat:55)")
    print(f"input:               '{ps.input_string}'")

    result = parse_event(ps)
    print(f"result, remaining:   {result}, '{ps.remaining}'")


def test_parse_parameters():
    ps = ParserString("(55, 22, -9.66, dog:33, cat:55)")
    print(f"input:               '{ps.input_string}'")

    result = parse_parameters(ps)
    print(f"result, remaining:   {result}, '{ps.remaining}'")


def test_parse_args():
    ps = ParserString("10.77, -99, 3.2")
    print(f"input:               '{ps.input_string}'")

    result = parse_args(ps)
    print(f"result, remaining:   {result}, '{ps.remaining}'")


def test_parse_number():
    ps = ParserString("10.77bobob")
    print(f"input:               '{ps.input_string}'")

    result = parse_number(ps)
    print(f"result, remaining:   {result}, '{ps.remaining}'")

    ps = ParserString("-1120.002")
    print(f"input:               '{ps.input_string}'")

    result = parse_number(ps)
    print(f"result, remaining:   {result}, '{ps.remaining}'")


def test_parse_chars():
    ps = ParserString("kskshk")
    print(f"input:               '{ps.input_string}'")

    result = parse_chars(ps, 'ks')
    print(f"result, remaining:   '{result}', '{ps.remaining}'")


def test_parse_char():
    ps = ParserString("kskshk")
    print(f"input:               '{ps.input_string}'")

    result = parse_char(ps, 'ks')
    print(f"result, remaining:   '{result}', '{ps.remaining}'")


def test_ps():
    ps = ParserString("kskshk")
    print(ps.input_string)
    print(ps.remaining)

    print(ps.consume())
    print(ps.peek())

    print(ps.input_string)
    print(ps.remaining)
    print(ps._remaining)



if __name__ == '__main__':
    # test_ps()
    # test_parse_char()
    # test_parse_chars()
    # test_parse_number()
    # test_parse_args()
    # test_parse_parameters()
    # test_parse_event()
    test_parse_sequence()