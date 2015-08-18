from libtree.tree import insert_node
from time import time

RUNS = (
    (1, 500),
    (1, 1000),
    (1, 10000),
    ##(1, 100000),
    ##(1, 1000000)
    (2, 100),
    ##(2, 200),
    ##(2, 500),
    (3, 25),
    (3, 35),
    (4, 10),
    (5, 8),
    #(5, 10),
    (6, 6),
    (7, 5),
    (8, 4),
    (9, 3),
    (10, 3),
    (11, 2),
    (12, 2),
    (15, 2),
    #(17, 2),
    ##(20, 2)
)

stats = list()
averages = list()
average = lambda a: sum(a) / len(a)


def calculate_tree_size(levels, per_level):
    return int(((1 - per_level ** (levels + 1)) / (1 - per_level)) - 1)


def populate_tree(per, node, levels, per_level, auto_position, depth=1):
    global stats
    for i in range(0, per_level):
        start = time()
        new_node = insert_node(per, node, auto_position=auto_position)
        duration = time() - start
        stats.append(duration)

        if depth < levels:
            populate_tree(per, new_node, levels, per_level, auto_position,
                          depth+1)


def benchmark(per, levels, per_level, auto_position):
    global stats, averages
    stats = list()
    root = insert_node(per, None, 'root')

    start = time()
    populate_tree(per, root, levels, per_level, auto_position)
    duration = time() - start

    start = time()
    per.commit()
    duration_commit = time() - start

    output = '=> {}s per node, {}s total, {}s commit time'
    _average = average(stats)
    print(output.format(_average, duration, duration_commit))
    #print(len(stats))
    averages.append(_average)


def setup(per):
    pass


def run(per):
    print('auto position OFF')
    for levels, per_level in RUNS:
        per.flush_tables()
        per.commit()
        output = '{} levels, {} nodes per level ({} nodes total)...'
        print(output.format(levels, per_level,
                            calculate_tree_size(levels, per_level)))
        benchmark(per, levels, per_level, False)
    output = 'Overall insertion speed on average: {}s'
    print(output.format(average(averages)))

    print()
    print('auto position ON')
    for levels, per_level in RUNS:
        per.flush_tables()
        per.commit()
        output = '{} levels, {} nodes per level ({} nodes total)...'
        print(output.format(levels, per_level,
                            calculate_tree_size(levels, per_level)))
        benchmark(per, levels, per_level, True)
    output = 'Overall insertion speed on average: {}s'
    print(output.format(average(averages)))


