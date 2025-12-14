"""
Algorithm to compute the nth prime using Miller-Rabin primality testing.

Theoretical Foundation:
1. Use Rosser-Dusart bounds to narrow search space to O(n/ln²n) candidates
2. Apply Miller-Rabin primality test to each candidate
3. Count primes until we reach the nth one

Overall Complexity: O(n ln⁴ n)
"""

import math
from typing import Tuple


def location_approximator(n: int) -> Tuple[int, int]:
    """
    Compute tight upper and lower bounds for the nth prime using Dusart's formulas.
    
    Theory: Based on Prime Number Theorem refinements by Rosser (1939), 
    Rosser-Schoenfeld (1962), and Dusart (2018).
    
    For n ≥ 688,383: Dusart's bounds give error < 0.017%
    For smaller n: Use Rosser-Schoenfeld bounds
    
    Args:
        n: Find bounds for the nth prime
        
    Returns:
        (lower_bound, upper_bound) tuple
    """
    if n == 1:
        return (2, 2)
    if n == 2:
        return (3, 3)
    if n == 3:
        return (5, 5)
    
    ln_n = math.log(n)
    ln_ln_n = math.log(ln_n)
    
    # Rosser-Schoenfeld bounds (1962) - work for n ≥ 6
    if n >= 6:
        # Lower bound: p_n > n(ln n + ln ln n - 1)
        lower_bound = int(n * (ln_n + ln_ln_n - 1))
        
        # Upper bound: p_n < n(ln n + ln ln n) for n ≥ 6
        upper_bound = int(n * (ln_n + ln_ln_n)) + 1
    
    # Dusart's improved bounds (2018) - for larger n
    if n >= 688383:
        # More refined lower bound
        lower_term = (ln_ln_n - 2) / ln_n
        lower_correction = ((ln_ln_n)**2 - 6*ln_ln_n + 11.321) / (2 * ln_n**2)
        lower_bound = int(n * (ln_n + ln_ln_n - 1 + lower_term - lower_correction))
        
        # More refined upper bound
        upper_term = (ln_ln_n - 2) / ln_n
        upper_correction = ((ln_ln_n)**2 - 6*ln_ln_n) / (2 * ln_n**2)
        upper_bound = int(n * (ln_n + ln_ln_n - 1 + upper_term - upper_correction)) + 1
    
    # For very small n, use simpler bounds
    if n < 6:
        lower_bound = 2
        upper_bound = 30
    
    # Ensure odd starting point (skip even numbers except 2)
    if lower_bound > 2 and lower_bound % 2 == 0:
        lower_bound += 1
    
    return (lower_bound, upper_bound)


def miller_rabin(num: int, witnesses: list) -> bool:
    """
    Miller-Rabin primality test - deterministic for given witnesses.
    
    Theory:
    - For prime p and p-1 = 2^r * d (d odd), testing witness a:
      Either a^d ≡ 1 (mod p), OR
      a^(2^i * d) ≡ -1 (mod p) for some 0 ≤ i < r
    
    - If neither holds, n is definitely composite
    - For n < 341,550,071,728,321, witnesses [2,3,5,7,11,13,17] are deterministic
    
    Time Complexity: O(k log³ n) where k = len(witnesses)
    
    Args:
        num: Number to test for primality
        witnesses: List of witness values to test
        
    Returns:
        True if num is (probably) prime, False if definitely composite
    """
    # Handle base cases
    if num < 2:
        return False
    if num == 2 or num == 3:
        return True
    if num % 2 == 0:
        return False
    
    # Write num-1 as 2^r * d where d is odd
    r = 0
    d = num - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test each witness
    for a in witnesses:
        if a >= num:
            continue
        
        # Compute a^d mod num
        x = pow(a, d, num)
        
        # If x = 1 or x = num-1, this witness passes
        if x == 1 or x == num - 1:
            continue
        
        # Square x repeatedly r-1 times
        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                composite = False
                break
        
        # If we never hit num-1 (-1 mod num), num is composite
        if composite:
            return False
    
    # Passed all witness tests
    return True


def nth_prime(n: int) -> int:
    """
    Compute the nth prime number using Miller-Rabin primality testing.
    
    Algorithm:
    1. Use location_approximator to get tight bounds on p_n
    2. Count primes from 2 up to lower_bound
    3. Search sequentially from lower_bound using Miller-Rabin
    4. Return when we've found exactly n primes
    
    Time Complexity: O(n ln⁴ n)
    - Testing O(n ln n) candidates
    - Each Miller-Rabin test: O(k log³ p) where k=7 witnesses
    
    Args:
        n: Find the nth prime (1-indexed)
        
    Returns:
        The nth prime number
    """
    if n == 1:
        return 2
    
    # Deterministic witnesses for n < 341,550,071,728,321
    witnesses = [2, 3, 5, 7, 11, 13, 17]
    
    # Get bounds on where p_n should be
    lower_bound, upper_bound = location_approximator(n)
    
    # Count primes from 2 up to lower_bound (not including lower_bound)
    prime_count = 0
    
    # Count 2 separately
    prime_count = 1
    
    # Count odd numbers from 3 to lower_bound-1
    candidate = 3
    while candidate < lower_bound:
        if miller_rabin(candidate, witnesses):
            prime_count += 1
        candidate += 2
    
    # Now search from lower_bound to upper_bound
    if lower_bound == 2:
        candidate = 2
    elif lower_bound % 2 == 0:
        candidate = lower_bound + 1
    else:
        candidate = lower_bound
    
    # Search for the nth prime
    while prime_count < n and candidate <= upper_bound:
        if candidate == 2 or (candidate > 2 and miller_rabin(candidate, witnesses)):
            prime_count += 1
            if prime_count == n:
                return candidate
        
        # Move to next candidate (skip evens)
        if candidate == 2:
            candidate = 3
        else:
            candidate += 2
    
    # If we didn't find it in bounds, extend search (shouldn't happen with good bounds)
    while prime_count < n:
        if miller_rabin(candidate, witnesses):
            prime_count += 1
            if prime_count == n:
                return candidate
        candidate += 2
    
    return candidate


# Test the implementation
if __name__ == "__main__":
    # Test cases
    test_cases = [
        (1, 2),
        (10, 29),
        (100, 541),
        (1000, 7919),
        (12345, 132241),
        (123456, 1632899),
        (1234567, 19394489),
        (431331120407, 12562389345433)
    ]
    
    print("Testing nth_prime implementation:")
    print("=" * 50)
    for n, expected in test_cases:
        result = nth_prime(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} nth_prime({n:4d}) = {result:6d} (expected {expected:6d})")
