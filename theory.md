#Theoretical Construction

We can transform a **Prime Detector** (a primality test) into a **Prime Computer** (an algorithm that finds the $n$-th prime) using the following logical framework:

### 1. Prime Detector
Let $I(k)$ be an indicator function defined as:
$$
I(k) = 
\begin{cases} 
1 & \text{if } k \text{ is prime} \\
0 & \text{if } k \text{ is composite}
\end{cases}
$$
For computational efficiency, we implement $I(k)$ using the **Miller-Rabin primality test**, which serves as our fast "detector."

### 2. Prime Counting Function
Using the detector, we construct the prime-counting function $\pi(x)$, which counts the number of primes less than or equal to $x$:
$$
\pi(x) = \sum_{k=2}^{x} I(k)
$$

### 3. Inversion to Nth Prime
The $n$-th prime, denoted $p_n$, is mathematically defined as the smallest integer $x$ such that the prime count reaches $n$:
$$
p_n = \min \{ x \in \mathbb{Z}^+ \mid \pi(x) = n \}
$$

### Algorithmic Implementation
Instead of using Willans' formula—which computes this inversion using inefficient closed-form summations of factorials—we implement the inversion algorithmically:

1.  **Upper Bound Guarantee**: We utilize **Rosser's Theorem** to establish a search limit, ensuring our algorithm terminates within a known finite range.
    > **Theorem (Rosser, 1939):** For $n \ge 6$, the $n$-th prime satisfies:
    > $$ p_n < n(\ln n + \ln \ln n) $$

2.  **Search & Count**: We iterate through integers $k = 2, 3, \dots$, applying the Miller-Rabin test $I(k)$ to each candidate.

3.  **Stop Condition**: We maintain a running count of primes found. The algorithm terminates and returns $k$ exactly when the count equals $n$.
