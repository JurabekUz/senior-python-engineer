# advanced iteration functions in the itertools package

import itertools


def example_function(x):
    return x < 40


def main():
    vals = [10, 20, 30, 40, 50, 40, 30]

    # dropwhile and takewhile will return values until
    # a certain condition is met that stops them
    print(list(itertools.dropwhile(example_function, vals)))  # [40, 50, 40, 30]
    print(list(itertools.takewhile(example_function, vals)))  # [10, 20, 30]


# infinate iterators: count, repeat, cycle


def count_example(start, step):
    """Use count to create a simple counter."""

    counter = itertools.count(start, step)
    for c in counter:
        if c < 100:
            print(c)
        else:
            break


def repeat_example(element, max_repeats):
    """
    Use repeat to create a simple iterator that repeats an element.

    Args:
        element: list, str, tuple, set, dict
        max_repeats: int
    """
    repeater = itertools.repeat(element, max_repeats)
    print(list(repeater))

    for r in repeater:
        print(r)


def cycle_example(elements):
    """
    Use cycle to create a simple iterator that cycles over a collection.

    Args:
        elements: list, str, tuple, set, dict
    """
    i = 0
    cycler = itertools.cycle(elements)
    while i < 100:
        print(next(cycler), end=" ")
        i += 1


# terminating iterators: accumulate, chain, chain_from_iterable


def accumulate_example(elements):
    """
    Use accumulate to create an iterator that accumulates values.

    Args:
        elements: list, str, tuple, set, dict
    """
    acc = itertools.accumulate(elements)
    print(list(acc))


def chain_example(elements1, elements2, elements3):
    chain = itertools.chain(elements1, elements2, elements3)
    print(list(chain))


def chain_from_iterable_example(elements):
    chain = itertools.chain.from_iterable(elements)
    print(list(chain))


# combinatorics: product, combinations, permutations, combinations_with_replacement


def product_example(elements1, elements2):
    product = itertools.product(elements1, elements2)
    print(list(product))


def combinations_example(elements, r):
    comb = itertools.combinations(elements, r)
    print(list(comb))


def permutations_example(elements, r):
    perm = itertools.permutations(elements, r)
    print(list(perm))


def combinations_with_replacement_example(elements, r):
    combinations_with_replacement = itertools.combinations_with_replacement(elements, r)
    print(list(combinations_with_replacement))


if __name__ == "__main__":
    # main()
    # count_example(10, 10)
    # repeat_example([1,2,3,4,5,6], 3)
    # cycle_example(['a', 'b', 'c', 'd', 'e'])

    # accumulate_example([1,2,3,4,5,6])
    # accumulate_example("hello")
    # accumulate_example({"a": 1, "b": 2, "c": 3})

    # chain_example([1,2,3], [4,5,6], [7,8,9])
    # chain_example("hello", "world", "python")

    # chain_from_iterable_example([[1,2,3], [4,5,6], [7,8,9]])
    # chain_from_iterable_example(["hello", "world", "python"])

    # product_example([1,2], ['a', 'b'])
    # combinations_example([1,2,3,4], 2)
    # permutations_example([1,2,3,4], 2)
    combinations_with_replacement_example([1, 2, 3, 4], 2)
