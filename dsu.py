class DisjointSetUnion:
    def __init__(self, elements):
        self.parent = {}
        self.rank = {}

        for x in elements:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, a):
        if a != self.parent[a]:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]

    def union(self, a, b):
        parentX = self.find(a)
        parentY = self.find(b)

        if parentX == parentY:
            return False

        if self.rank[parentX] < self.rank[parentY]:
            self.parent[parentX] = parentY
        elif self.rank[parentX] > self.rank[parentY]:
            self.parent[parentY] = parentX
        else:
            self.parent[parentY] = parentX
            self.rank[parentX] += 1

        return True