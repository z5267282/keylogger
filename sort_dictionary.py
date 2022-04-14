def test_sort():
    x = {
        'hello': 10,
        'fish': 19,
        'dog': 12,
        'boat': 190,
        'number': 60
    }

    attempt = sorted(x.items(), key=lambda pair: pair[1], reverse=True)
    print(attempt)

def lambda_dict():
    x = {
        'hello': 10,
        'fish': 19,
        'dog': 12,
        'boat': 190,
        'number': 60
    }

    for x, v in x.items():
        print(f'{x} | {v}')

def main():
    test_sort()
    # lambda_dict()

if __name__ == '__main__':
    main()
