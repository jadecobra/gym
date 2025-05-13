import math
import random

def conjunction():
    # return p and q
    return 0b1000

def disjunction():
    # return p or q
    return 0b1110

def or_operations():
    return {
        0b1101,  # p or not q (converse implication)
        0b1011,  # not p or q (logical implication)
        0b0110,  # (not p and q) or (p and not q) (exclusive disjunction)
        0b1001,  # (p and q) or not (p or q) (logical equality)
        0b0001,  # not (p or q) (logical NOR)
    }

def binary_operations():
    return {
        0b0000: ("return False", "contradiction", "FFFF"),
        0b0001: ("return not (p or q)", "logical NOR", "FFFT"),
        0b0010: ("return not p and q", "converse non implication", "FFTF"),
        0b0011: ("return not p", "negate first", "FFTT"),
        0b0100: ("return p and not q", "material non implication", "FTFF"),
        0b0101: ("return not q", "negate second", "FTFT"),
        0b0110: ("return (not p and q) or (p and not q)", "exclusive disjunction", "FTTF"),
        0b0111: ("return not (p and q)", "logical NAND", "FTTT"),
        conjunction(): ("return p and q", "logical conjunction", "TFFF"),
        0b1001: ("return (p and q) or not (p or q)", "logical equality", "TFFT"),
        0b1010: ("return q", "project second", "TFTF"),
        0b1011: ("return not p or q", "logical implication", "TFTT"),
        0b1100: ("return p", "project first", "TTFF"),
        0b1101: ("return p or not q", "converse implication", "TTFT"),
        disjunction(): ("return p or q", "logical disjunction", "TTTF"),
        0b1111: ("return True", "tautology", "TTTT")
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
    conjunction_index = get_operation_index(conjunction(), sequence)
    # if conjunction_index >= 4:
    if conjunction_index >= 3:
        return False
    return True

def check_disjunction_after_conjunction(sequence):
    """Check if disjunction appears after conjunction."""
    conjunction_index = get_operation_index(conjunction(), sequence)
    disjunction_index = get_operation_index(disjunction(), sequence)

    if disjunction_index != -1 and conjunction_index != -1:
        if disjunction_index < conjunction_index:
            return False
    return True

def check_or_ops_after_disjunction(sequence):
    """Check if OR operations appear after disjunction."""
    disjunction_index = get_operation_index(disjunction, sequence)

    if disjunction_index == -1:
        return True, []

    violations = []
    for operation in or_operations():
        index = get_operation_index(operation, sequence)
        if index != -1 and index < disjunction_index:
            violations.append((operation, index))

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
        for operation, index in or_violations:
            violations.append(
                f"OR operation {binary_operations()[operation][1]} at position {index+1} before disjunction"
            )

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
    expr, name, bits = binary_operations()[pattern]
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
    conjunction_pos = get_operation_index(conjunction(), sequence) + 1
    print(f"- Conjunction appears at position {conjunction_pos}")

    # Check disjunction position
    disjunction_pos = get_operation_index(disjunction(), sequence) + 1
    print(f"- Disjunction appears at position {disjunction_pos}")

    # Check OR operations
    for op in or_operations():
        op_index = get_operation_index(op, sequence)
        if op_index != -1:
            op_pos = op_index + 1
            op_name = binary_operations()[op][1]
            if op_pos < disjunction_pos:
                print(f"- VIOLATION: {op_name} appears at position {op_pos}, before disjunction at {disjunction_pos}")
            else:
                print(f"- {op_name} appears at position {op_pos}, after disjunction at {disjunction_pos}")

def print_sequence(sequence):
    """Print the final sequence with details."""
    print("Final Truth Table Sequence:")
    for i in range(len(sequence)):
        print_step_info(sequence, i)

    print_constraint_verification(sequence)

def try_starting_pattern(start):
    """Try finding a sequence starting with a specific pattern."""
    print(f"Trying start pattern: {binary_operations()[start][2]} ({start:04b})")

    sequence = backtrack([start], set(range(16)) - {start})
    return sequence

def find_truth_table_sequence():
    starting_positions = [
        0b1100, # project first
        conjunction(),
        0b0000, # contradiction
        0b1111, # tautology
        0b1010, # project second
        0b0011, # negate first
        0b0101, # negate second
    ]
    random.shuffle(starting_positions)
    for start in starting_positions:
        sequence = backtrack([start], set(range(16)) - {start})
        if sequence:
            print_sequence(sequence)
            return sequence
        else:
            print(f"No sequence found starting with {binary_operations()[start][2]} ({start:04b})")
    else:
        print("No valid sequence found after trying all priority starts.")
        return None


if __name__ == '__main__':
    find_truth_table_sequence()