"""Activity 8 - Heaps and Priority Queues (Activities 1-6)."""
import random


class _Heap:
    """Array-based binary heap. Subclasses define _before(a, b):
    True if a should sit closer to the root than b."""

    def __init__(self):
        self._data = []

    def _before(self, a, b):
        raise NotImplementedError

    def size(self):
        return len(self._data)

    def is_empty(self):
        return not self._data

    def peek(self):
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def insert(self, value):
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def extract(self):
        if not self._data:
            raise IndexError("extract from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        d = self._data
        while i > 0:
            parent = (i - 1) // 2
            if self._before(d[i], d[parent]):
                d[i], d[parent] = d[parent], d[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        d, n = self._data, len(self._data)
        while True:
            left, right, best = 2 * i + 1, 2 * i + 2, i
            if left < n and self._before(d[left], d[best]):
                best = left
            if right < n and self._before(d[right], d[best]):
                best = right
            if best == i:
                break
            d[i], d[best] = d[best], d[i]
            i = best


# Activity 1
class MinHeap(_Heap):
    def _before(self, a, b):
        return a < b


# Activity 2
class MaxHeap(_Heap):
    def _before(self, a, b):
        return a > b


# Activity 3
def heap_sort(arr):
    """Ascending sort using a max-heap (does not modify the input)."""
    heap = MaxHeap()
    for x in arr:
        heap.insert(x)
    result = [None] * len(arr)
    for i in range(len(arr) - 1, -1, -1):  # largest goes to the end
        result[i] = heap.extract()
    return result


# Activity 4
def kth_largest(nums, k):
    """kth largest using a min-heap of size k."""
    if not 1 <= k <= len(nums):
        raise ValueError("k must be between 1 and len(nums)")
    heap = MinHeap()
    for x in nums:
        if heap.size() < k:
            heap.insert(x)
        elif x > heap.peek():
            heap.extract()
            heap.insert(x)
    return heap.peek()


# Activity 5
def merge_k_sorted(arrays):
    """Merge sorted arrays using a min-heap of (value, source index, position)."""
    heap = MinHeap()
    for src, arr in enumerate(arrays):
        if arr:
            heap.insert((arr[0], src, 0))
    merged = []
    while not heap.is_empty():
        value, src, pos = heap.extract()
        merged.append(value)
        if pos + 1 < len(arrays[src]):
            heap.insert((arrays[src][pos + 1], src, pos + 1))
    return merged


# Activity 6 (stretch)
def run_scheduler(jobs):
    """jobs: list of (priority, name). Higher priority is released first."""
    heap = MaxHeap()
    for job in jobs:
        heap.insert(job)
    order = []
    step = 1
    while not heap.is_empty():
        priority, name = heap.extract()
        print(f"Step {step}: released {name} (priority {priority})")
        order.append(name)
        step += 1
    return order


def drain(heap):
    out = []
    while not heap.is_empty():
        out.append(heap.extract())
    return out


def test_all():
    data = [5, 9, 11, 14, 19, 17, 18, 13]

    # Activity 1
    h = MinHeap()
    assert h.size() == 0
    try:
        h.extract()
        assert False, "empty extract should raise"
    except IndexError:
        pass
    h.insert(7)
    assert h.peek() == 7 and h.size() == 1 and drain(h) == [7]
    h = MinHeap()
    for x in data:
        h.insert(x)
    assert drain(h) == [5, 9, 11, 13, 14, 17, 18, 19]
    h = MinHeap()
    for x in [3, 1, 3, 1, 2]:
        h.insert(x)
    assert drain(h) == [1, 1, 2, 3, 3]
    rnd = [random.randint(0, 100) for _ in range(200)]
    h = MinHeap()
    for x in rnd:
        h.insert(x)
    assert drain(h) == sorted(rnd)

    # Activity 2
    h = MaxHeap()
    for x in data:
        h.insert(x)
    assert drain(h) == [19, 18, 17, 14, 13, 11, 9, 5]
    h = MaxHeap()
    for x in rnd:
        h.insert(x)
    assert drain(h) == sorted(rnd, reverse=True)

    # Activity 3
    cases = [[4, 10, 3, 5, 1], [1, 2, 3, 4], [4, 3, 2, 1],
             [2, 3, 2, 1, 3, 1], [], [9],
             [random.randint(0, 50) for _ in range(100)]]
    for c in cases:
        assert heap_sort(c) == sorted(c)

    # Activity 4
    nums = [random.randint(0, 1000) for _ in range(50)] + [7, 7]
    for k in (1, 5, len(nums)):
        assert kth_largest(nums, k) == sorted(nums, reverse=True)[k - 1]
    assert kth_largest([5], 1) == 5
    assert kth_largest([4, 4, 4], 2) == 4

    # Activity 5
    a, b, c = [1, 4, 9, 20], [2, 3, 5], [0, 6, 7, 8, 30, 31]
    out = merge_k_sorted([a, b, c])
    assert out == sorted(a + b + c)
    assert merge_k_sorted([[], [], []]) == []
    assert merge_k_sorted([[1, 1], [1]]) == [1, 1, 1]

    # Activity 6
    order = run_scheduler([(2, "email"), (5, "backup"), (1, "print"),
                           (5, "deploy"), (3, "report")])
    print("Release order:", order)
    assert order[:2] in (["deploy", "backup"], ["backup", "deploy"])
    assert order[-1] == "print"

    print("All tests passed.")


if __name__ == "__main__":
    test_all()
