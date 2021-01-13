# 4474630975855204960

def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s

def digital_root(n, initial_call=True):
    if n > 9:
        print()
        print(n)
        print("%.1f" % (n*0.1))
        print("%.1f" % (n/10))
        print("%.1f" % (n//10))
        print(int(n/10))
        sum = digital_root(int(n/10), False) + (n%10)
        if initial_call:
            return digital_root(sum)
        else:
            return sum
    else:
        return n

print(4+4+7+4+6+3+0+9+7+5+8+5+5+2+0+4+9+6+0)

print(digital_root(4474630975855204960))