"""
collections_examples.py
Examples of Python's collections module: Counter, defaultdict, OrderedDict, deque, namedtuple
Run: python3 collections_examples.py
"""
from collections import Counter, defaultdict, OrderedDict, deque, namedtuple


def demo_counter():
    words = ["apple", "banana", "apple", "orange", "banana", "apple"]
    c = Counter(words)
    print("Counter:", c)                        # Counter({'apple': 3, 'banana': 2, 'orange': 1})
    print("most_common(2):", c.most_common(2))  # [('apple', 3), ('banana', 2)]
    c.update(["banana", "kiwi"])              # update counts
    print("after update:", c)
    c.subtract(["apple", "kiwi"])
    print("after subtract:", c)


def demo_defaultdict():
    dd = defaultdict(list)
    pairs = [("a", 1), ("b", 2), ("a", 3)]
    for k, v in pairs:
        dd[k].append(v)
    print("defaultdict (lists):", dict(dd))

    counts = defaultdict(int)
    for word in ["x", "y", "x"]:
        counts[word] += 1
    print("defaultdict (int counts):", dict(counts))


def demo_ordereddict():
    od = OrderedDict()
    od['first'] = 1
    od['second'] = 2
    od['third'] = 3
    print("OrderedDict insertion order:", list(od.items()))
    od.move_to_end('second')
    print("after move_to_end('second'):", list(od.items()))


def demo_deque():
    d = deque([1, 2, 3])
    d.append(4)
    d.appendleft(0)
    print("deque after appends:", list(d))
    d.pop()
    d.popleft()
    print("deque after pops:", list(d))
    d = deque(maxlen=3)
    for i in range(5):
        d.append(i)
    print("deque with maxlen=3 (drops left):", list(d))


def demo_namedtuple():
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)
    print("namedtuple Point:", p)
    p2 = p._replace(x=99)
    print("_replace ->", p2)
    print("as dict ->", p2._asdict())


def simple_tests():
    # quick sanity checks
    c = Counter('aabbc')
    assert c['a'] == 2 and c['c'] == 1
    dd = defaultdict(int)
    dd['z'] += 5
    assert dd['z'] == 5
    od = OrderedDict([('a', 1), ('b', 2)])
    od.move_to_end('a')
    assert list(od.keys()) == ['b', 'a']
    d = deque(maxlen=2)
    d.append(1)
    d.append(2)
    d.append(3)
    assert list(d) == [2, 3]


if __name__ == '__main__':
    print('\n--- collections demo ---')
    demo_counter()
    print()
    demo_defaultdict()
    print()
    demo_ordereddict()
    print()
    demo_deque()
    print()
    demo_namedtuple()
    print('\n--- running simple tests ---')
    simple_tests()
    print('All simple tests passed.')
