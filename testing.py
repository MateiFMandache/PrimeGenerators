from prime_generators import *


# testing code for prime_ish_generator

for p_ish in prime_ish_generator():
    if p_ish > 100:
        break
    print(p_ish, end=" ")
print()

for p_ish in prime_ish_generator(49):
    if p_ish > 100:
        break
    print(p_ish, end=" ")
print()


# testing code for is_prime_trialdiv and generator_trialdiv

for n in range(-10, 100):
    if is_prime_trialdiv(n):
        print(n, end=" ")
print()

for n in generator_trialdiv():
    if n > 10_000:
        break
    print(n, end=" ")
print()


# testing code for is_prime_mr and generator_mr

for n in range(-10, 100):
    if is_prime_mr(n):
        print(n, end=" ")
print()

for n in generator_mr():
    if n > 10_000:
        break
    print(n, end=" ")
print()


# Testing code for generator_compheap

for n in generator_compheap():
    if n > 100:
        break
    print(n, end=" ")
print()

for n in generator_compheap():
    if n > 10_000:
        break
    print(n, end=" ")
print()
