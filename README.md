# PrimeGenerators
Three algorithms for generating the prime numbers are implemented in python. These are then tested and compared for speed and accuracy.

Rough descriptions are as follows:
 - Algorithm 1 is Trial Division. We test if each number is prime by dividing it by numbers up to its square root
 - Algorithm 2 is Miller-Rabin test. We run the Miller-Rabin test on each number to test if it is prime. For more info, see https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test. Note that this is a probabilistic method.
 - Algorithm 3 is Composite Heap algorithm. Upcoming composite numbers are stored in a heap, so that they can be skipped, and only prime numbers are output. This is similar to Eratosthenes' sieve, but requires far less memory.
