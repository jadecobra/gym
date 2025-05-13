import math

# Define operations with their patterns and descriptions
OPERATIONS = {
    0b0000: ("return False", "contradiction", "FFFF"),
    0b0001: ("return not (p or q)", "logical NOR", "FFFT"),
    0b0010: ("return not p and q", "converse non implication", "FFTF"),
    0b0011: ("return not p", "negate first", "FFTT"),
    0b0100: ("return p and not q", "material non implication", "FTFF"),
    0b0101: ("return not q", "negate second", "FTFT"),
    0b0110: ("return (not p and q) or (p and not q)", "exclusive disjunction", "FTTF"),
    0b0111: ("return not (p and q)", "logical NAND", "FTTT"),
    0b1000: ("return p and q", "conjunction", "TFFF"),
    0b1001: ("return (p and q) or not (p or q)", "logical equality", "TFFT"),
    0b1010: ("return q", "project second", "TFTF"),
    0b1011: ("return not p or q", "logical implication", "TFTT"),
    0b1100: ("return p", "project first", "TTFF"),
    0b1101: ("return p or not q", "converse implication", "TTFT"),
    0b1110: ("return p or q", "disjunction", "TTTF"),
    0b1111: ("return True", "tautology", "TTTT")
}

# Define operation categories for constraints
CONJUNCTION = 0b1000  # p and q
DISJUNCTION = 0b1110  # p or q
OR_OPERATIONS = {
    0b1101,  # p or not q (converse implication)
    0b1011,  # not p or q (logical implication)
    0b0110,  # (not p and q) or (p and not q) (exclusive disjunction)
    0b1001,  # (p and q) or not (p or q) (logical equality)
    0b0001,  # not (p or q) (logical NOR)
}

def hamming_distance(a, b):
    """Calculate number of differing bits between two patterns."""
    return bin(a ^ b).count('1')

def get_neighbors(pattern, unused_patterns):
    """Find all patterns that differ by exactly one bit."""
    return [p for p in unused_patterns if hamming_distance(pattern, p) == 1]

def get_changed_bit_position(prev, current):
    """Determine which bit position changed between patterns."""
    changed_bits = prev ^ current
    return int(math.log2(changed_bits))

def get_operation_index(pattern, sequence):
    """Find the index of a pattern in a sequence, or -1 if not found."""
    return sequence.index(pattern) if pattern in sequence else -1

def check_conjunction_early(sequence):
    """Check if conjunction appears early (within first 4 steps)."""
    conjunction_index = get_operation_index(CONJUNCTION, sequence)
    if conjunction_index >= 4:
        return False
    return True

def check_disjunction_after_conjunction(sequence):
    """Check if disjunction appears after conjunction."""
    conjunction_index = get_operation_index(CONJUNCTION, sequence)
    disjunction_index = get_operation_index(DISJUNCTION, sequence)

    if disjunction_index != -1 and conjunction_index != -1:
        if disjunction_index < conjunction_index:
            return False
    return True

def check_or_ops_after_disjunction(sequence):
    """Check if OR operations appear after disjunction."""
    disjunction_index = get_operation_index(DISJUNCTION, sequence)

    if disjunction_index == -1:
        return True, []

    violations = []
    for op in OR_OPERATIONS:
        op_index = get_operation_index(op, sequence)
        if op_index != -1 and op_index < disjunction_index:
            violations.append((op, op_index))

    return len(violations) == 0, violations

def check_constraints(sequence):
    """Check if a sequence violates any constraints."""
    violations = []

    # Conjunction must appear early
    if not check_conjunction_early(sequence):
        violations.append("Conjunction not appearing early")

    # Disjunction must appear after conjunction
    if not check_disjunction_after_conjunction(sequence):
        violations.append("Disjunction appearing before conjunction")

    # OR operations must appear after disjunction
    valid_or_ops, or_violations = check_or_ops_after_disjunction(sequence)
    if not valid_or_ops:
        for op, idx in or_violations:
            violations.append(f"OR operation {OPERATIONS[op][1]} at position {idx+1} before disjunction")

    return violations

def try_next_pattern(sequence, unused_patterns, depth=0):
    current = sequence[-1]
    neighbors = get_neighbors(current, unused_patterns)
    if not neighbors:
        return None
    for next_pattern in neighbors:
        new_sequence = sequence + [next_pattern]
        violations = check_constraints(new_sequence)
        if violations and depth > 4:  # Changed from 6 to 4
            continue
        return next_pattern
    return None

def backtrack(sequence, unused_patterns, depth=0):
    if len(sequence) == 16:  # Temporarily reduce to 8 for debugging
    # if len(sequence) == 8:  # Temporarily reduce to 8 for debugging
        return sequence
    current = sequence[-1]
    neighbors = get_neighbors(current, unused_patterns)
    if not neighbors:
        return None
    for next_pattern in neighbors:  # Try all neighbors explicitly
        new_sequence = sequence + [next_pattern]
        new_unused = unused_patterns - {next_pattern}
        violations = check_constraints(new_sequence)
        if violations and depth > 4:
            continue
        result = backtrack(new_sequence, new_unused, depth + 1)
        if result:
            return result
    return None

def print_step_info(sequence, i):
    """Print information about a single step in the sequence."""
    pattern = sequence[i]
    expr, name, bits = OPERATIONS[pattern]
    print(f"{i+1}. {bits} ({pattern:04b}) - {expr} - {name}")

    # Show bit changes (except for first step)
    if i > 0:
        prev = sequence[i-1]
        bit_pos = get_changed_bit_position(prev, pattern)
        print(f"   Changed bit at position {bit_pos} from previous step")

def print_constraint_verification(sequence):
    """Print verification of constraints for the final sequence."""
    print("\nVerifying constraints:")

    # Check conjunction position
    conjunction_pos = get_operation_index(CONJUNCTION, sequence) + 1
    print(f"- Conjunction appears at position {conjunction_pos}")

    # Check disjunction position
    disjunction_pos = get_operation_index(DISJUNCTION, sequence) + 1
    print(f"- Disjunction appears at position {disjunction_pos}")

    # Check OR operations
    for op in OR_OPERATIONS:
        op_index = get_operation_index(op, sequence)
        if op_index != -1:
            op_pos = op_index + 1
            op_name = OPERATIONS[op][1]
            if op_pos < disjunction_pos:
                print(f"- VIOLATION: {op_name} appears at position {op_pos}, before disjunction at {disjunction_pos}")
            else:
                print(f"- {op_name} appears at position {op_pos}, after disjunction at {disjunction_pos}")

def print_sequence(sequence):
    """Print the final sequence with details."""
    print("\nGray Code Final Truth Table Sequence:")
    for i in range(len(sequence)):
        print_step_info(sequence, i)

    print_constraint_verification(sequence)

def try_starting_pattern(start):
    """Try finding a sequence starting with a specific pattern."""
    print(f"Trying start pattern: {OPERATIONS[start][2]} ({start:04b})")

    sequence = backtrack([start], set(range(16)) - {start})
    return sequence

def generate_gray_code(n):
    """Generate a Gray code sequence for n bits."""
    if n <= 0:
        return [0]
    prev = generate_gray_code(n - 1)
    return prev + [x | (1 << (n - 1)) for x in reversed(prev)]

def adjust_sequence_for_constraints(gray_seq):
    """Adjust Gray code sequence to meet constraints with all unique patterns."""
    seq = list(gray_seq)  # Full 16-pattern Gray code

    # Remove and reinsert conjunction early (position 2)
    conj_idx = seq.index(CONJUNCTION)  # 0b1000
    if conj_idx != 2:
        seq.pop(conj_idx)
        seq.insert(2, CONJUNCTION)

    # Remove and reinsert disjunction after conjunction (position 6)
    disj_idx = seq.index(DISJUNCTION)  # 0b1110
    if disj_idx <= 2:
        seq.pop(disj_idx)
        seq.insert(6, DISJUNCTION)
    elif disj_idx != 6:
        seq.pop(disj_idx)
        seq.insert(6, DISJUNCTION)

    # Ensure OR operations appear after disjunction (positions 7-10)
    or_ops = sorted(OR_OPERATIONS)  # [0b0110, 0b1001, 0b1011, 0b1101]
    current_pos = 7
    for op in or_ops:
        op_idx = seq.index(op)
        if op_idx < 6:
            seq.pop(op_idx)
            seq.insert(current_pos, op)
            current_pos += 1
        elif op_idx >= current_pos:
            seq.pop(op_idx)
            seq.insert(current_pos, op)
            current_pos += 1

    # Fix single-bit changes by swapping where needed
    for i in range(1, len(seq)):
        if hamming_distance(seq[i-1], seq[i]) != 1:
            for j in range(i + 1, len(seq)):
                if (hamming_distance(seq[i-1], seq[j]) == 1 and
                    (i == len(seq) - 1 or hamming_distance(seq[j], seq[i+1]) == 1)):
                    seq[i], seq[j] = seq[j], seq[i]
                    break

    # Verify all 16 patterns are unique
    if len(set(seq)) != 16:
        raise ValueError("Sequence does not contain all 16 unique patterns")

    return seq

def find_truth_table_sequence():
    """Find a sequence using Gray code with constraint adjustments."""
    gray_seq = generate_gray_code(4)  # 4 bits for 16 patterns
    sequence = adjust_sequence_for_constraints(gray_seq)
    violations = check_constraints(sequence)
    if not violations:
        print_sequence(sequence)
        return sequence
    print("Adjusted sequence violates constraints:", violations)
    return None


if __name__ == '__main__':
    find_truth_table_sequence()