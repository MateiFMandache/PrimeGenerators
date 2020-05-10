import math
from random import randint
from heapq import *


def prime_ish_generator(start=2):
    """
    A generator that generates all numbers greater than or equal
    to the start value which are not divisible by 2, 3 or 5.
    """
    i = (start - 2) // 30
    for j in [7, 11, 13, 17, 19, 23, 29, 31]:
        if 30 * i + j >= start:
            yield 30 * i + j
    i += 1
    while True:
        for j in [7, 11, 13, 17, 19, 23, 29, 31]:
            yield 30 * i + j
        i += 1


def is_prime_trialdiv(number, try235=True):
    """
    Tests if the number is prime using trial division.
    We use the prime-ish generator to generate our trial divisors.
    The optional parameter try235 indicates whether to try dividing by
    2, 3 and 5. This can be set to false to save time if the number is
    already known to be prime-ish
    """
    if number <= 1:
        return False
    if try235:
        if number in [2, 3, 5]:
            return True
        for trial_divisor in [2, 3, 5]:
            if number % trial_divisor == 0:
                return False
    cut_off = math.floor(math.sqrt(number))
    for trial_divisor in prime_ish_generator():
        if trial_divisor > cut_off:
            return True
        if number % trial_divisor == 0:
            return False


def generator_trialdiv():
    """
    Generates the prime numbers by using trial division
    to check if each of the prime-ish numbers are prime.
    """
    yield 2
    yield 3
    yield 5
    for p_ish in prime_ish_generator():
        # already know 2, 3 and 5 don't divide
        # number, so set try235 parameter to False
        if is_prime_trialdiv(p_ish, try235=False):
            yield p_ish


def efficient_exponential(base, exponent, modulus):
    """
    An efficient algorithm to compute powers modulo some number,
    using the square and multiply method.
    """
    if not isinstance(exponent, int) or not exponent >= 0:
        raise ValueError("exponent must be a non-negative integer")
    result = 1
    while exponent:
        if exponent % 2 == 1:
            result *= base
            result %= modulus
        exponent //= 2
        base = base**2
        base %= modulus
    return result


def is_prime_mr(number, tries=3):
    """
    Returns whether or not a number is prime, by applying the
    Miller-Rabin primality test. NB: this test is probabilistic.
    There is a small chance some composite numbers will pass the test.
    The parameter tries is the number of times we test a number before
    deeming it prime.
    """
    if number < 2:
        return False
    if number == 2:
        return True
    # write p-1 as 2**s * t where t is odd
    s = 0
    t = number - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    for i in range(tries):
        # Choose a random base b and compute b**t mod number
        b = randint(1, number - 1)
        q = efficient_exponential(b, t, number)
        good = False
        for j in range(s):
            # repeatedly square q:= b**t mod number and see if it
            # becomes -1 mod number
            if q == number - 1 or (q == 1 and j == 0):
                good = True
                break
            q = q ** 2
            q = q % number
        if not good:
            return False
    return True


def generator_mr(tries=3):
    """
    Generates the prime numbers by using the Miller-Rabin test
    to check if each of the prime-ish numbers are prime. Note that this
    is a probabilistic method. The parameter tries is the number of times
    the Miller-Rabin test is applied before a number is deemed prime.
    Higher values of tries reduce the chance of error at the cost of a
    longer runtime.
    """
    yield 2
    yield 3
    yield 5
    for p_ish in prime_ish_generator():
        if is_prime_mr(p_ish, tries):
            yield p_ish


def generator_compheap():
    """
    Generates the prime numbers by skipping any numbers which are
    composite in the stream given by prime_ish_generator. For each
    prime up to the square root of the number we've got to,
    we have a generator generating all the prime-ish multiples
    of that prime, so we know to skip over them. We also have a
    generator that gives us the squares of primes, so we know when to
    start worrying about a new prime factor. The next composite number,
    for each of the primes, and the next prime square, are all
    stored in a heap, hence the name compheap
    (short for composite heap)
    """
    yield 2
    yield 3
    yield 5
    # In the heap, squares are given as (square, prime, 1)
    # while other composites are given as (composite, prime, 0)
    heap = [(49, 7, 1)]
    # A dict that will contain, for each prime, a generator generating
    # prime-ish numbers to multiply the prime by.
    composite_generators = {}
    # Finally, a generator generating all primes, starting with 11.
    # Used for generating the squares. We will throw away the first
    # four primes generated later, due to constraints involving
    # recursion.
    gen_for_squares = generator_compheap()
    next_composite = heap[0][0]
    for p_ish in prime_ish_generator():
        if p_ish != next_composite:
            yield p_ish
        else:
            while p_ish == next_composite:
                replaced_tuple = heap[0]
                p = replaced_tuple[1]
                if replaced_tuple[2] == 0:
                    # This is the non-square case
                    next_tuple = (next(composite_generators[p]) * p, p, 0)
                    heappushpop(heap, next_tuple)
                    next_composite = heap[0][0]
                else:
                    # This is the square case
                    if p == 7:
                        for i in range(4):
                            # throw away first four primes, to get to 11
                            next(gen_for_squares)
                    # Add next square in
                    prime_for_square = next(gen_for_squares)
                    heappushpop(heap, (prime_for_square ** 2, prime_for_square, 1))
                    # Initialise new generator
                    composite_generators[p] = prime_ish_generator(start=p+1)
                    # Add in the next composite value associated with p
                    next_tuple = (next(composite_generators[p]) * p, p, 0)
                    heappush(heap, next_tuple)
                    next_composite = heap[0][0]

