data = ["a", "b", "c", "d", "e", "f"]

for i, k in zip(data[0::2], data[1::2]):
    print(str(i), "<>", str(k))

if len(data) % 2 != 0:
    print(str(data[-1]), "<>", "*")
