def cycle_notation_to_one_line_notation(cycle_perm):
    tmp = [inner_element for lis in cycle_perm for inner_element in lis]
    assert(len(set(tmp)) == len(tmp))
    assert(set(tmp) == set(range(len(tmp))))
    res = [None] * len(tmp)
    for cycle in cycle_perm:
        for i,el in enumerate(cycle):
            res[el] = cycle[(i+1) % len(cycle)]
    return res

def one_line_notation_to_cycle_notation(one_perm):
    #add check for valididity
    assert(len(set(one_perm)) == len(one_perm))
    assert(set(one_perm) == set(range(len(one_perm))))
    res = []
    tmp_set = set(one_perm)
    while len(tmp_set) != 0:
        popped = tmp_set.pop()
        cur = popped
        cycle=[]
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
    def __init__(self, patt, adjlis):
        assert(type(patt) is list)
        assert(all(type(double) is tuple for double in patt))
        assert(all(type(cycle) is list and type(boolean) is bool for cycle,boolean in patt))
        assert(all(type(element) is int for cycle,_ in patt for element in cycle))
        assert(all(type(elem) is int) for elem in adjlis)
        # check if elements are legal
        self.patt = [(list(a),b) for a,b in patt]
        self.adjlis = list(adjlis)
        self.lengths = [len(a) for a,_ in patt]
        self.length = sum(self.lengths)
        self.numcycles = len(self.lengths)
    def number_of_cycles(self):
        return self.numcycles
    def get_pattern_cycle_pair(self,i):
        return self.patt[i] if 0 <= i < self.numcycles else None
    def get_adjacency_set(self):
        return self.adjlis
    def __len__(self):
        return self.length
    def __str__(self):
        patt_str = ''.join([('({})' if whole else '[{}]').format(' '.join(str(item) for item in substr)) for substr,whole in self.patt])
        adj_str = ", ".join(str(item) for item in self.adjlis)
        return "({}, {{{}}})".format(patt_str, adj_str)
    def occurrences_in(self, perm):
        for m in match(perm,self):
            yield m
        return
    def avoided_by(self, perm):
        for occ in self.occurrences_in(perm):
            # if we find an occurrence we stop
            return False
        # otherwise we know the permutation avoids the pattern
        return True
    def contained_in(self, perm):
        return not self.avoided_by(perm)



#best function
def normalize_set_of_substrings(substrings):
    flattened_substrings = sorted([elem for substring in substrings for elem in substring])
    res = []
    for substring in substrings:
        res.append([])
        for elem in substring:
            res[-1].append(flattened_substrings.index(elem))
    return res

def match(perm,patt):
    count = 0
    for substrings in available_substrings(perm,patt):
        norm = normalize_set_of_substrings(substrings)
        for i,substring in enumerate(substrings):
            cycle = patt.get_pattern_cycle_pair(i)[0]
            if any(a!=b for a,b in zip(cycle,norm[i])):
                break
        else:
            for adj in patt.get_adjacency_set():
                for i,norm_substring in enumerate(norm):
                    for j,elem in enumerate(norm_substring):
                        if elem == adj:
                            a = substrings[i][j]
                        if elem == (adj+1)%len(patt):
                            b = substrings[i][j]
                if (a + 1) % len(perm) != b:
                    break
            else:
                yield substrings

def available_substrings(perm, patt):
    ind = 0
    k = patt.number_of_cycles()
    iter_lis = [None] * k
    res = [None] * k
    perm_cycles = [lis*2 for lis in sorted(perm.get_cycles(), key=lambda cycle:len(cycle))]
    def calc_iter(ind):
        res2 = []
        for perm_cycle in perm_cycles:
            substr,whole = patt.get_pattern_cycle_pair(ind)
            len_cycle = len(perm_cycle)//2
            len_patt  = len(substr)
            if len_patt <= len_cycle and (not whole or len_patt == len_cycle):
                for i in range(len_cycle):
                    tmp = perm_cycle[i:i+len_patt]
                    if all(elem not in [a for lis in res[:ind] for a in lis] for elem in tmp):
                        res2.append(tmp)
        return iter(res2)
    iter_lis[ind] = calc_iter(ind)

    #alphabetic order with cutoffs
    while ind != -1:
        if iter_lis[ind] is None:
            iter_lis[ind] = calc_iter(ind)
        else:
            try:
                res[ind] = next(iter_lis[ind])
                ind += 1
                if ind == k:
                    yield list(res)
                    ind -= 1
            except StopIteration:
                iter_lis[ind] = None
                ind -= 1

class Permutation:
    """
A permutation can either be initialized using one-line notation as a list of integers or in cycle notation as a list of list of integers.
The following two are equivalent
    perm = Permutation([0,3,1,2])
    perm = Permutation([[0],[1,3,2]])
Furthermore a permutation object of length n must be initialized with each integer in range(n) exactly once.
    """
    def __init__(self, data):

        assert(type(data) is list)
        if all(type(d) is int for d in data):
            self.perm = list(data)
            self.cycles = one_line_notation_to_cycle_notation(self.perm)
        elif all(type(d) is list for d in data) and all(type(d) is int for lis in data for d in lis):
            self.cycles = [list(d) for d in data]
            self.perm = cycle_notation_to_one_line_notation(self.cycles)
        else:
            assert("help")
        # check if elements are legal
    def __len__(self):
        return len(self.perm)
    def __eq__(self,other):
        return len(self) == len(other) and all(a == b for a,b in zip(self.perm,other.perm))
    def __str__(self):
        return ''.join(['({})'.format(' '.join(str(elem) for elem in cycle)) for cycle in self.cycles])
    def get_cycles(self):
        return self.cycles
    def occurrences(self, patt):
        return patt.occurrences_in(self)
    def avoids(self, patt):
        return patt.avoided_by(self)
    def contains(self, patt):
        return not patt.contained_in(self)


def set_avoids(perm, patts):
    return all(patt.avoided_by(perm) for patt in patts)
