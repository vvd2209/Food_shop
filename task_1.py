def generate_sequence(n):
    sequence = ""
    for i in range(1, n + 1):
        sequence += str(i) * i
        if len(sequence) >= n:
            break
    return sequence[:n]

n = int(input("Введите количество элементов последовательности: "))
result = generate_sequence(n)
print(result)
