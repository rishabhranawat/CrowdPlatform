#alculate similarity between two text documents.

import sys

SHINGLE_SIZE = 5

def get_shingles(f, size):
    shingles = set()
    buf = f
    for i in range(0, len(buf)-size+1):
        yield buf[i:i+size]

def jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x / float(y)


f1 = 'rishabh ra'
f2 = 'rishabh ranawat'

shingles1 = set(get_shingles(f1, size=SHINGLE_SIZE))
shingles2 = set(get_shingles(f2, size=SHINGLE_SIZE))

print(jaccard(shingles1, shingles2), f1, f2)

# EOF

