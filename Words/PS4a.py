# Problem Set 4A
# Name: Yaacoub Yaacoub
# Time Spent: x:xx


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    sequence = sequence.lower()
    if len(sequence) <= 1:
        return [sequence]
    else:
        list = []
        new_sequence = sequence[1:]
        permutation_list = get_permutations(new_sequence)
        for p in permutation_list:
            for i in range(len(p) + 1):
                list.append(p[:i] + sequence[0] + p[i:])
        return list


if __name__ == '__main__':
    #    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:  ', get_permutations(example_input))
    print()

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)

    example_input_2 = 'BuSt'
    print('Input:', example_input_2)
    print('Expected Output:', ['bust', 'ubst', 'usbt', 'ustb', 'bsut', 'sbut', 'subt', 'sutb', 'bstu', 'sbtu',
                               'stbu', 'stub', 'buts', 'ubts', 'utbs', 'utsb', 'btus', 'tbus', 'tubs', 'tusb',
                               'btsu', 'tbsu', 'tsbu', 'tsub'])
    print('Actual Output:  ', get_permutations(example_input_2))
    print()

    example_input_3 = '123'
    print('Input:', example_input_3)
    print('Expected Output:', ['123', '213', '231', '132', '312', '321'])
    print('Actual Output:  ', get_permutations(example_input_3))
    print()

    example_input_4 = 'aeiou'
    print('Input:', example_input_4)
    print('Expected Output:', )
    print('Actual Output:  ', get_permutations(example_input_4))
    print()
