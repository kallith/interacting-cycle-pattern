#!/usr/bin/env python3
from interactingcyclepattern import Permutation
from interactingcyclepattern import InteractingCyclePattern

if __name__ == "__main__":
    # initialize permutation in one-line notation
    perm1 = Permutation([4,5,6,7,0,1,3,2])
    # initialize the same permutation using cyclic notation
    perm2 = Permutation([[0,4],[1,5],[2,6,3,7]])
    assert(perm1 == perm2)

    # We initialize 3 similar patterns
    patts = [
                # [0 2][1 3], {}
                InteractingCyclePattern([([0,2],False),([1,3],False)],[]),
                # [0 2][1 3], {0,2}
                InteractingCyclePattern([([0,2],False),([1,3],False)],[0,2]),
                # [0 2](1 3), {}
                InteractingCyclePattern([([0,2],False),([1,3],True)],[])
            ]
    # When we print out all occurrences of the patterns in the permutation initialized above
    for patt in patts:
        print("All occurrences of {} in {}".format(patt,perm1))
        for m in perm1.occurrences(patt):
            print(m)
        print()

    # Given a interacting cycle pattern we can count how many permutations of lenght n avoid that pattern
    import itertools
    import math
    patt = InteractingCyclePattern([([0,2],False),([1,3],False)], [])
    print("How many permutations of length n avoid/contain the interacting cycle pattern {}?".format(patt))
    for n in range(1,7):
        perm_gen = itertools.permutations(range(n))
        count = sum(Permutation(list(perm)).avoids(patt) for perm in perm_gen)
        print("When n={} then {} avoid, while {} contain.".format(n, count, math.factorial(n)-count))

