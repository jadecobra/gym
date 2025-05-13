def satisfies_gray_code_property(sequence):
    # Verify the sequence satisfies Gray code property
    for i in range(1, len(sequence)):
        prev_pattern, _, _, _ = sequence[i-1]
        curr_pattern, _, _, _ = sequence[i]
        diff = bin(prev_pattern ^ curr_pattern).count('1')
        if diff != 1:
            print(f"Error: Step {i} changes {diff} bits, not 1!")


def pattern_unique(sequence):
    # Check all patterns are unique
    patterns = [operation[0] for operation in sequence]
    if len(patterns) != len(set(patterns)):
        print("Error: Duplicate patterns found!")
    return patterns


def all_patterns_used(patterns):
    # Check all 16 patterns are used
    all_patterns = set(range(16))
    used = set(patterns)
    if used != all_patterns:
        print(f"Error: Missing patterns: {all_patterns - used}")


def print_sequence(sequence):
    # Print the final sequence
    print("Final Truth Table Sequence:")
    for i, (binary, expr, name, bits) in enumerate(sequence, 1):
        print(f"{i}. {bits} ({binary:04b}) - {expr} - {name}")


def truth_table_sequence():
    """
    Returns a sequenced truth table with each step differing by exactly one bit,
    following a Gray code pattern and logical ordering requirements.
    """
    # Track used patterns
    used_patterns = set()

    # Define all 16 logical operations with their binary patterns and descriptions
    operations = (
        # Start with simplest operations
        (0b0000, "return False", "contradiction", "FFFF"),
        (0b1100, "return p", "project first", "TTFF"),
        (0b1000, "return p and q", "conjunction", "TFFF"),
        (0b1001, "return (p and q) or not (p or q)", "logical equality", "TFFT"),
        (0b0001, "return not (p or q)", "logical NOR", "FFFT"),
        (0b0101, "return not q", "negate second", "FTFT"),
        (0b0100, "return p and not q", "material non implication", "FTFF"),
        (0b0110, "return (not p and q) or (p and not q)", "exclusive disjunction", "FTTF"),
        (0b0010, "return not p and q", "converse non implication", "FFTF"),
        (0b0011, "return not p", "negate first", "FFTT"),
        (0b1011, "return not p or q", "logical implication", "TFTT"),
        (0b1111, "return True", "tautology", "TTTT"),
        (0b1110, "return p or q", "disjunction", "TTTF"),
        (0b1010, "return q", "project second", "TFTF"),
        (0b0010, "return not p and q", "converse non implication", "FFTF"),
        (0b0110, "return (not p and q) or (p and not q)", "exclusive disjunction", "FTTF"),
        (0b0111, "return not (p and q)", "logical NAND", "FTTT"),
        (0b1101, "return p or not q", "converse implication", "TTFT"),
    )

    # The correct sequence that maintains Gray code property
    sequence = (
        (0b0000, "return False", "contradiction", "FFFF"),
        (0b0001, "return not (p or q)", "logical NOR", "FFFT"),
        (0b0011, "return not p", "negate first", "FFTT"),
        (0b0010, "return not p and q", "converse non implication", "FFTF"),
        (0b0110, "return (not p and q) or (p and not q)", "exclusive disjunction", "FTTF"),
        (0b0111, "return not (p and q)", "logical NAND", "FTTT"),
        (0b0101, "return not q", "negate second", "FTFT"),
        (0b0100, "return p and not q", "material non implication", "FTFF"),
        (0b1100, "return p", "project first", "TTFF"),
        (0b1101, "return p or not q", "converse implication", "TTFT"),
        (0b1111, "return True", "tautology", "TTTT"),
        (0b1110, "return p or q", "disjunction", "TTTF"),
        (0b1010, "return q", "project second", "TFTF"),
        (0b1011, "return not p or q", "logical implication", "TFTT"),
        (0b1001, "return (p and q) or not (p or q)", "logical equality", "TFFT"),
        (0b1000, "return p and q", "conjunction", "TFFF"),
    )

    satisfies_gray_code_property(sequence)
    patterns = pattern_unique(sequence)
    all_patterns_used(patterns)
    print_sequence(sequence)




# Run the function
truth_table_sequence()