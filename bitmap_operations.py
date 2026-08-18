# from time_debug import timer

def sum_bits(bitmap: int) -> int:
    sum = 0
    while bitmap > 0:
        sum += bitmap % 2
        bitmap //= 2
    return sum