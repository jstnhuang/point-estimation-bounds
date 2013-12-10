"""Find empirical bounds for coin flips.

Hoeffding's inequality gives us theoretical bounds on the number of coin flips
you need to estimate the probability of heads within some episilon, with some
probability 1-delta. However, it's a loose bound.

This simulates a bunch of coin flips to see how many are actually needed in
practice.
"""
import random

import numpy as np


def experiment(epsilon, delta, verbose=False):
    """Perform the coin-flipping experiment.

    Creates NUM_COINS biased coins (probability of heads is known as theta).
    Then, flips the coins repeatedly. Each time, we update our estimate of the
    thetas (our "guesses"). Then we see how many of the estimates are within
    epsilon of the true theta. If >= 1-delta of the estimates are close enough,
    then we stop.
    """
    NUM_COINS = 10000
    emp_delta = 1
    num_flips = 0
    thetas = np.random.rand(NUM_COINS)
    counts = np.zeros(NUM_COINS)
    deltas = []
    while emp_delta > delta:
        flips = [1 if random.random() < theta else 0 for theta in thetas]
        num_flips += 1
        counts += flips
        guesses = counts / num_flips
        diffs = np.abs(guesses - thetas)
        emp_delta = len(np.where(diffs > epsilon)[0]) / NUM_COINS
        deltas.append(emp_delta)
        if verbose:
            print('{}\t{}'.format(num_flips, emp_delta))
    return num_flips


def deltas_over_num_flips():
    experiment(0.1, 0.05, verbose=True)


def num_flips_over_epsilon():
    for epsilon in np.linspace(0.01, 0.25, num=25):
        num_flips = experiment(epsilon, 0.05) 
        print('{}\t{}\t{}'.format(epsilon, 0.05, num_flips))

    
def num_flips_over_delta():
    for delta in np.linspace(0.01, 0.25, num=25):
        num_flips = experiment(0.05, delta)
        print('{}\t{}\t{}'.format(0.05, delta, num_flips))


def main():
    deltas_over_num_flips()
#    num_flips_over_epsilon()
#    num_flips_over_delta()


if __name__ == '__main__':
    main()
