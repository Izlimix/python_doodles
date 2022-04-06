#!/usr/bin/env python3

# Test of command-line script execution and echoing args
# (Just use the python arg parsing module sys.argv or argparse)

if __name__ == "__main__":
    import sys
    print(f"Received {len(sys.argv)-1} non-standard args:")
    for i in range(1, len(sys.argv)):
        print(i, sys.argv[i])
