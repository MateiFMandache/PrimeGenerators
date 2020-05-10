from prime_generators import *
import time


EVALUATE_ACCURACY = True
EVALUATE_SPEED = True

# accuracy evaluation for generator_mr:

# how many trials to put generator_mr through
TRIALS = 100

# get sum of first 10_000 primes
sum_10_000 = 0
for prime in generator_trialdiv():
    if prime > 10_000:
        break
    sum_10_000 += prime

if EVALUATE_ACCURACY:
    for tries in [1, 2, 3, 4]:
        successes = 0
        for _ in range(TRIALS):
            trial_sum = 0
            for prime in generator_mr(tries):
                if prime > 10_000:
                    break
                trial_sum += prime
            if trial_sum == sum_10_000:
                successes += 1
        accuracy_percentage = 100 * successes / TRIALS
        print(f"accuracy with {tries} tries: {accuracy_percentage}% ({TRIALS:,} trials)")


# speed comparison

# Up to what limit we should generate primes
LIMIT = 1_000_000
# What values of tries we should evaluate the Miller_Rabin method with
MR_TRIES = [4, 10]


def run(method, *args):
    for n in method(*args):
        if n > LIMIT:
            break


method_dict = {
    "Trial division": generator_trialdiv,
    "Miller-Rabin test": generator_mr,
    "Composite heap": generator_compheap
}


if EVALUATE_SPEED:
    for method_name in method_dict:
        print(f"Trying {method_name}, up to {LIMIT:,}")
        if method_name == "Miller-Rabin test":
            for tries in MR_TRIES:
                print(f"with {tries} tries")
                start = time.perf_counter()
                run(method_dict[method_name], tries)
                print(f"took {time.perf_counter() - start} seconds")
        else:
            start = time.perf_counter()
            run(method_dict[method_name])
            print(f"took {time.perf_counter()-start} seconds")
