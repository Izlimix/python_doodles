#!/usr/bin/env python3
import string

# "I do not control the speed at which lobsters die"
# https://knowyourmeme.com/memes/i-do-not-control-the-speed-at-which-lobsters-die

# Given a sentence, what other sentences can we make out of it?
# e.g. "I________control____________________lobsters____"

# Todo: Infinite repeats of a sentence? (cleaner)
# Todo: Cluster letters that are closer together, rather than picking the first-seen letter from a diff word?
# Todo: Line-sweep algorithm to determine valid sentences, after detecting valid word start and end points

def foo(s, target, *, skip=None, repeat=False):
    # Rough first draft. Find target in s
    # Note: doesn't work with infinite-length s (say if it's a repeating iterable)
    if not s or not target:
        return None
    # Check whether all the letters of target appear in s at least once
    if not set(s.lower()).issuperset(target.lower()):
        return None
    
    i = 0
    l = len(target)
    out = []
    while repeat and i < l:
        for letter in s:
            #if skip and letter in skip:
            #    out.append(letter)
            #el
            if i < l and letter.lower() == target[i].lower():
                out.append(letter)
                i += 1
            else:
                out.append("_")
        if repeat and i < l:
            out.append("\n")
    if l == i:
        return "".join(out)
    else:
        print(f"Couldn't find {target} in {s}")
        return None

class Demo:
    # Pangrams from https://en.wikipedia.org/wiki/Pangram
    fox = "The quick brown fox jumps over the lazy dog."
    waltz = "Waltz, bad nymph, for quick jigs vex."
    glib = "Glib jocks quiz nymph to vex dwarf."
    sphinx = "Sphinx of black quartz, judge my vow."
    zebras = "How quickly daft jumping zebras vex!"
    wizards = "The five boxing wizards jump quickly."
    liquor = "Pack my box with five dozen liquor jugs."

    def clean(s):
        return "".join(l for l in s.lower() if l in string.ascii_lowercase)

if __name__ == "__main__":
    import sys
    #a, b = sys.argv[1], sys.argv[2]
    a = Demo.fox
    b = Demo.sphinx
    print(f"Trying to find '{b}' in '{a}'")
    a = Demo.clean(a)
    b = Demo.clean(b)
    out = foo(a, b, repeat=True)
    if out:
        print("Found:")
        print(out)
    else:
        print("Not found")