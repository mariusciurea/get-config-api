def generate_numbers(numbers: list):
    """Generate numbers from a list of numbers"""
    for number in numbers:
        yield number


if __name__ == '__main__':
    numbers = [1, 20, 33, 4, 5]
    generator = generate_numbers(numbers)
    print(next(generator))
    print(next(generator))
    numbers = (item for item in [100, 20, 23123, 342, 2342, 343])
    print(next(numbers))
    print(next(numbers))