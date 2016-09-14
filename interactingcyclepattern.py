def cycle_notation_to_one_line_notation(cycle_perm):
    '''
    Takes a permutation in cycle notation as input and returns the permutation in one-line notation.
    Cycle notation is represented by a list of list of integers.
    One-line notation is represented as a list of integers.

    >>> cycle_notation_to_one_line_notation([[0],[1,3,2]])
    [0,3,1,2]
    '''
    # get all the integers in one list to perform validity checks
    tmp = [inner_element for lis in cycle_perm for inner_element in lis]
    assert(len(set(tmp)) == len(tmp)), "For a permutation of length n, all elements in range(n) need to be present exactly once."
    assert(set(tmp) == set(range(len(tmp)))), "For a permutation of length n, all elements in range(n) need to be present."

    res = [None] * len(tmp)
    # walk through each cycle adding one mapping at a time
    for cycle in cycle_perm:
        for i,el in enumerate(cycle):
            res[el] = cycle[(i+1) % len(cycle)]
    return res

def one_line_notation_to_cycle_notation(one_perm):
    '''
    Takes a permutation in one-line notation as input and returns the permutation in cycle notation.
    One-line notation is represented as a list of integers.
    Cycle notation is represented by a list of list of integers.

    >>> one_line_notation_to_cycle_notation([0,3,1,2])
    [[0],[1,3,2]].
    '''
    assert(len(set(one_perm)) == len(one_perm)), "For a permutation of length n, all elements in range(n) need to be present exactly once."
    assert(set(one_perm) == set(range(len(one_perm)))), "For a permutation of length n, all elements in range(n) need to be present."

    res = []
    tmp_set = set(one_perm)
    while len(tmp_set) != 0:
        popped = tmp_set.pop()
        cur = popped
        cycle=[]
        # find a cycle by starting at popped
        while 1:
            nxt = one_perm[cur]
            cycle.append(cur)
            if popped == nxt:
                break
            cur = nxt
        res.append(cycle)
        tmp_set.difference_update(cycle)
    return res

class InteractingCyclePattern:
    '''
    InceractingCyclePattern(patt, adjlis)

    patt should be a list of tuples, where the first element is a list of integers(a cycle in the pattern) and the second element is a boolean variable (True meaning that the cycle is in braces not brackets), and adjlis should be a list of integers.

    For example the following interacting cycle patterns are initialized like so:
    # [0 2][1 3], {}
    >>> InteractingCyclePattern([([0,2],False),([1,3],False)],[])
    # [0 2][1 3], {0,2}
    >>> InteractingCyclePattern([([0,2],False),([1,3],False)],[0,2])
    # [0 2](1 3), {}
    >>> InteractingCyclePattern([([0,2],False),([1,3],True)],[])
    '''
    def __init__(self, patt, adjlis):
        # check if elements are legal
        assert(type(patt) is list), "patt needs to be a list."
        assert(all(type(double) is tuple for double in patt)), "patt needs to be a list of tuples." 
        assert(all(type(cycle) is list and type(boolean) is bool for cycle,boolean in patt)), "The first element of each tuple in patt needs to be a list and the second element needs to be a boolean."
        assert(all(type(element) is int for cycle,_ in patt for element in cycle)), "The first element of each tuple in patt needs to be a list of integers."
        assert(type(adjlis) is list), "adjlis needs to be a list."
        assert(all(type(elem) is int) for elem in adjlis), "adjlis needs to be a list of integers."

        # copy the lists when we assign them to the variables
        self.patt = [(list(a),b) for a,b in patt]
        self.adjlis = list(adjlis)

        # list of the length of each cycle
        self.lengths = [len(a) for a,_ in patt]
        # total length of the pattern
        self.length = sum(self.lengths)
        # number of cycles in the pattern
        self.numcycles = len(self.lengths)

    # getter functions
    def number_of_cycles(self):
        '''
        Returns the number of cycles in the pattern.
        '''
        return self.numcycles
    def get_pattern_cycle_pair(self,i):
        '''
        Returns the i-th cycle and boolean in the pattern.
        '''
        return self.patt[i] if 0 <= i < self.numcycles else None
    def get_adjacency_set(self):
        '''
        Returns the adjacency set of the pattern.
        '''
        return self.adjlis
    def __len__(self):
        return self.length
    def __str__(self):
        patt_str = ''.join([('({})' if whole else '[{}]').format(' '.join(str(item) for item in substr)) for substr,whole in self.patt])
        adj_str = ", ".join(str(item) for item in self.adjlis)
        return "({}, {{{}}})".format(patt_str, adj_str)

    def occurrences_in(self, perm):
        '''
        Generator that yields one occurence at a time of the pattern in the permutation perm.
        '''
        for m in match(perm,self):
            yield m
        return
    def avoided_by(self, perm):
        '''
        Returns true if the permutation perm avoids the pattern.
        '''
        for occ in self.occurrences_in(perm):
            # if we find an occurrence we stop
            return False
        # otherwise we know the permutation avoids the pattern
        return True
    def contained_in(self, perm):
        '''
        Returns true if the permutation contains the pattern.
        '''
        return not self.avoided_by(perm)



def normalize_set_of_substrings(substrings):
    '''
    Takes a list of lists as an argument and returns a list of lists where each element has been normalized.
    >>> normalize_set_of_substrings([[1,4],[3,6]])
    [[0, 2], [1, 3]]
    '''
    flattened_substrings = sorted([elem for substring in substrings for elem in substring])
    res = []
    for substring in substrings:
        res.append([])
        for elem in substring:
            res[-1].append(flattened_substrings.index(elem))
    return res

def available_substrings(perm, patt):
    '''
    Generator that yields all substrings from the permutation perm that will match the cycles in the interacting cycle pattern patt.
    '''
    ind = 0
    k = patt.number_of_cycles()
    iter_lis = [None] * k
    res = [None] * k
    # sort the cycles by increasing length along with doubling each list for easier use
    perm_cycles = [lis*2 for lis in sorted(perm.get_cycles(), key=lambda cycle:len(cycle))]

    # helper function that gives us the substrings we can use from cycle number ind in patt given we have already picked some substrings stored in res
    def calc_iter(ind):
        res2 = []
        for perm_cycle in perm_cycles:
            # whole tracks whether we have a cycle in braces or not (need the whole cycle or not)
            substr,whole = patt.get_pattern_cycle_pair(ind)
            len_cycle = len(perm_cycle)//2
            len_patt  = len(substr)
            # see if the substring is of a legal size
            if len_patt <= len_cycle and (not whole or len_patt == len_cycle):
                for i in range(len_cycle):
                    tmp = perm_cycle[i:i+len_patt]
                    # we add the substring to our result if the elements have not appeared in our result before
                    if all(elem not in [a for lis in res[:ind] for a in lis] for elem in tmp):
                        res2.append(tmp)
        return iter(res2)
    iter_lis[ind] = calc_iter(ind)

    #alphabetic order with cutoffs
    while ind != -1:
        if iter_lis[ind] is None:
            iter_lis[ind] = calc_iter(ind)
        else:
            # see if we can get another element from the iterator
            try:
                res[ind] = next(iter_lis[ind])
                ind += 1
                if ind == k:
                    yield list(res)
                    ind -= 1
            # when we empty an iterator go back one level
            except StopIteration:
                iter_lis[ind] = None
                ind -= 1

def match(perm,patt):
    '''
    Generator that yields all matches of the interacting cycle pattern patt in the permutation perm.
    '''
    count = 0
    for substrings in available_substrings(perm,patt):
        norm = normalize_set_of_substrings(substrings)
        # first see if the cycles match
        for i,substring in enumerate(substrings):
            cycle = patt.get_pattern_cycle_pair(i)[0]
            if any(a!=b for a,b in zip(cycle,norm[i])):
                break
        # if they do see if the adjacencies match too
        else:
            for adj in patt.get_adjacency_set():
                for i,norm_substring in enumerate(norm):
                    for j,elem in enumerate(norm_substring):
                        if elem == adj:
                            a = substrings[i][j]
                        if elem == (adj+1)%len(patt):
                            b = substrings[i][j]
                # if the elements indicated by the adjacency aren't adjacent in value we break
                if (a + 1) % len(perm) != b:
                    break
            else:
                yield substrings


class Permutation:
    """
A permutation object can either be initialized using one-line notation, as a list of integers, or in cycle notation, as a list of list of integers.
This means the following are equivalent:
    perm = Permutation([0,3,1,2])
    perm = Permutation([[0],[1,3,2]])
Furthermore a permutation object of length n must be initialized using each integer in range(n) exactly once.
    """
    def __init__(self, data):
        assert(type(data) is list), "Invalid argument, Permutation requires a list as an argument"
        # check if all elements
        if all(type(d) is int for d in data):
            self.perm = list(data)
            self.cycles = one_line_notation_to_cycle_notation(self.perm)
        elif all(type(d) is list for d in data) and all(type(d) is int for lis in data for d in lis):
            self.cycles = [list(d) for d in data]
            self.perm = cycle_notation_to_one_line_notation(self.cycles)
        else:
            assert(), "Invalid argument, Permutation requires list of integers or a list of list of integers as an argument"
        # check if elements are legal
    def __len__(self):
        return len(self.perm)
    def __eq__(self,other):
        return len(self) == len(other) and all(a == b for a,b in zip(self.perm,other.perm))
    def __str__(self):
        return ''.join(['({})'.format(' '.join(str(elem) for elem in cycle)) for cycle in self.cycles])

    def get_cycles(self):
        '''
        Returns the cycles in the permutation.
        '''
        return self.cycles
    def occurrences(self, patt):
        '''
        Returns generator that yields each occurence of the interaction cycle pattern patt in the permutation.
        '''
        return patt.occurrences_in(self)
    def avoids(self, patt):
        '''
        Returns true if the permutation avoids the interacting cycle pattern patt.
        '''
        return patt.avoided_by(self)
    def contains(self, patt):
        '''
        Returns true if the permutation contains the interacting cycle pattern patt.
        '''
        return not patt.contained_in(self)


def set_avoids(perm, patts):
    '''
    Returns true if the permutation perm avoids all the interacting cycle patterns in the collection patts.
    '''
    return all(patt.avoided_by(perm) for patt in patts)
