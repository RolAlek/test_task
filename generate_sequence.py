def generate_sequence(number: int) -> list[int]:
    return [
        str(i) for i in range(1, number + 1) for _ in range(i)
    ][:number]

n = int(input('How many numbers do you want to generate? '))
result = generate_sequence(n)
print(''.join(result))
