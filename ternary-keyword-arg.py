def test(n=42):
    print(n)

check = False
test(n=100 if check else -2)
