import random
import PrimalityTest


def generate_random_prime(bits):
    """Generate a random prime number with the specified number of bits."""
    while True:
        # Generate a random number with the specified number of bits
        num = random.getrandbits(bits)

        # Ensure the number is odd (to improve chances of primality)
        num |= 1

        # Check if the number is prime
        if PrimalityTest.is_prime(num):
            print("Generated random number: {}".format(num))
            return num

# Example: Generate a random prime number with 32 bits
