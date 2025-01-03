import functools


@functools.cache
def count_ways(design, patterns):
    if len(design) == 0:
        return 0, True

    total_ways = 0

    pattern_found_for_real = False
    for pattern in patterns:
        if design == pattern:
            # Exact match.
            total_ways += 1
            pattern_found_for_real = True
        elif design.startswith(pattern):
            pattern_length = len(pattern)
            # print(f"using pattern {pattern} for first bit of design {design}")
            remaining = design[pattern_length:]
            ways, pattern_found = count_ways(remaining, patterns)
            if pattern_found:
                pattern_found_for_real = True
                total_ways += ways
    return total_ways, pattern_found_for_real


def solve(filename):
    file = open(filename, "r")
    lines = file.readlines()
    total = 0

    patterns = lines[0].split(", ")
    patterns = [x.strip() for x in patterns]
    designs = lines[2:]

    total_ways = 0

    for design in designs:
        design = design.strip()
        ways, pattern_found = count_ways(design, tuple(patterns))
        # print(f"Design {design}: {ways}, pattern found: {pattern_found}")
        if pattern_found:
            total += 1
            total_ways += ways
    patterns.sort()

    print("Part 1:", total)
    print("Part 1:", total_ways)

solve("input.txt")