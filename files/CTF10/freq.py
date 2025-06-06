#!/usr/bin/env python3

from collections import Counter
import re

TOP_K  = 20
N_GRAM = 3

# Generate all the n-grams for value n
def ngrams(n, text):
    for i in range(len(text) -n + 1):
        # Ignore n-grams containing white space
        if not re.search(r'\s', text[i:i+n]):
           yield text[i:i+n]

# Read the data from the ciphertext
with open('L12G02.cph') as f: # ! Modified file name
    text = f.read()

# Count, sort, and print out the n-grams
for N in range(N_GRAM):
   print("-------------------------------------")
   print("{}-gram (top {}):".format(N+1, TOP_K))
   counts = Counter(ngrams(N+1, text))       # Count

   total_count = sum(counts.values())        # ! Calculate total count

   sorted_counts = counts.most_common(TOP_K) # Sort
   for ngram, count in sorted_counts:
       print("{}: {} ({:.2f}%)".format(ngram, count, (count/total_count)*100)) # ! Print with percentage