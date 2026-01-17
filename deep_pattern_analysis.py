#!/usr/bin/env python3
"""
Deep Pattern Analysis: Atomic Limits vs Exceptional Structures
Searches for connections between period digits and mathematical constants
"""

import sys
from collections import Counter
from itertools import combinations

# ============================================================================
# MATHEMATICAL CONSTANTS FROM EXCEPTIONAL STRUCTURES
# ============================================================================

class ExceptionalStructures:
    """Known constants from E8, Golay, Monster, etc."""
    
    # E8 Lattice (Dimension 8)
    E8 = {
        'dimension': 8,
        'root_vectors': 240,
        'kissing_number': 240,
        'coxeter_number': 30,
        'weyl_group_order': 696729600,
        'highest_root': [2, 3, 4, 5, 6, 4, 2, 3],  # Example coordinate
        'simple_roots': 8,
        'dual_coxeter': 30,
        'determinant': 1,
    }
    
    # Golay Codes
    GOLAY = {
        # Binary Golay Code
        'binary_dimension': 23,
        'binary_codewords': 4096,  # 2^12
        'binary_distance': 7,
        'binary_data_bits': 12,
        'binary_parity_bits': 11,
        
        # Extended Binary Golay
        'extended_dimension': 24,
        'extended_codewords': 4096,
        'extended_distance': 8,
        
        # Ternary Golay
        'ternary_dimension': 11,
        'ternary_codewords': 729,  # 3^6 - LOOK! 729 appears in 1/137!
        'ternary_distance': 5,
    }
    
    # Leech Lattice (Dimension 24)
    LEECH = {
        'dimension': 24,
        'minimal_vectors': 196560,
        'kissing_number': 196560,
        'coxeter_number': 0,  # No Coxeter group
        'covering_radius': 2,
    }
    
    # Mathieu Groups
    MATHIEU = {
        'M22_order': 443520,
        'M23_order': 10200960,
        'M24_order': 244823040,
        'M22_degree': 22,
        'M23_degree': 23,
        'M24_degree': 24,
    }
    
    # Monster Group
    MONSTER = {
        'order': '808017424794512875886459904961710757005754368000000000',  # ~8×10^53
        'supersingular_primes': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 43, 47, 59, 71],
        'conjugacy_classes': 194,
        'dimension_smallest_rep': 196883,
        'j_invariant_coefficients': [-744, 196884, 21493760, 864299970],  # First few
    }
    
    # Special numbers that appear
    SPECIAL_NUMBERS = {
        'powers_of_3': [3, 9, 27, 81, 243, 729, 2187, 6561],  # 3^1 to 3^8
        'powers_of_2': [2, 4, 8, 16, 32, 64, 128, 256],       # 2^1 to 2^8
        'small_primes': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43],
        'factorials': [1, 2, 6, 24, 120, 720, 5040],  # 1! to 7!
    }

# ============================================================================
# PATTERN MATCHING FUNCTIONS
# ============================================================================

def find_subsequences(period_str, target_numbers):
    """Find if any target numbers appear as subsequences in period"""
    matches = []
    for num in target_numbers:
        num_str = str(num)
        if num_str in period_str:
            # Find all positions
            positions = []
            start = 0
            while True:
                pos = period_str.find(num_str, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            matches.append({
                'number': num,
                'positions': positions,
                'count': len(positions)
            })
    return matches

def find_modular_matches(period_int, structures_dict):
    """Check if period % key_number reveals patterns"""
    matches = []
    for name, value in structures_dict.items():
        if isinstance(value, int) and value > 0 and value < 10**6:
            result = period_int % value
            if result == 0:
                matches.append({
                    'structure': name,
                    'value': value,
                    'remainder': result,
                    'type': 'perfect_divisor'
                })
            elif result == 1:
                matches.append({
                    'structure': name,
                    'value': value,
                    'remainder': result,
                    'type': 'one_more_than_multiple'
                })
            elif result == value - 1:
                matches.append({
                    'structure': name,
                    'value': value,
                    'remainder': result,
                    'type': 'one_less_than_multiple'
                })
    return matches

def find_digit_patterns(period_str):
    """Analyze digit distribution and patterns"""
    digits = [int(d) for d in period_str]
    
    patterns = {
        'digit_frequency': dict(Counter(digits)),
        'most_common': Counter(digits).most_common(3),
        'least_common': Counter(digits).most_common()[-3:] if len(Counter(digits)) >= 3 else [],
        'runs': find_runs(period_str),
        'symmetries': find_symmetries(period_str),
    }
    return patterns

def find_runs(s):
    """Find consecutive repeated digits"""
    runs = []
    if not s:
        return runs
    
    current_digit = s[0]
    current_run = 1
    
    for i in range(1, len(s)):
        if s[i] == current_digit:
            current_run += 1
        else:
            if current_run >= 2:
                runs.append({'digit': current_digit, 'length': current_run, 'position': i - current_run})
            current_digit = s[i]
            current_run = 1
    
    if current_run >= 2:
        runs.append({'digit': current_digit, 'length': current_run, 'position': len(s) - current_run})
    
    return runs

def find_symmetries(s):
    """Check for palindromic or symmetric patterns"""
    length = len(s)
    symmetries = []
    
    # Check if entire string is palindrome
    if s == s[::-1]:
        symmetries.append({'type': 'full_palindrome', 'length': length})
    
    # Check for partial palindromes (substrings of length >= 5)
    for start in range(len(s) - 4):
        for end in range(start + 5, min(start + 15, len(s) + 1)):
            substring = s[start:end]
            if substring == substring[::-1]:
                symmetries.append({
                    'type': 'partial_palindrome',
                    'string': substring,
                    'position': start,
                    'length': len(substring)
                })
    
    return symmetries[:10]  # Limit to first 10

def analyze_arithmetic_sequences(period_str):
    """Look for arithmetic progressions in the digits"""
    digits = [int(d) for d in period_str]
    sequences = []
    
    # Look for sequences of length 3+
    for start in range(len(digits) - 2):
        for length in range(3, min(len(digits) - start + 1, 8)):
            subseq = digits[start:start+length]
            if len(subseq) >= 3:
                diffs = [subseq[i+1] - subseq[i] for i in range(len(subseq)-1)]
                if len(set(diffs)) == 1:  # All differences are the same
                    sequences.append({
                        'position': start,
                        'sequence': subseq,
                        'difference': diffs[0],
                        'length': length
                    })
    
    return sequences[:10]  # Limit output

def find_factor_connections(period_int, period_length, structures):
    """Check if period relates to structure through factorization"""
    connections = []
    
    # Check E8
    if period_int % structures.E8['root_vectors'] == 0:
        connections.append(f"Period divisible by E8 roots (240)")
    
    if period_int % structures.E8['coxeter_number'] == 0:
        connections.append(f"Period divisible by E8 Coxeter number (30)")
    
    # Check Golay
    if period_int % structures.GOLAY['ternary_codewords'] == 0:
        connections.append(f"Period divisible by ternary Golay codewords (729)")
    
    # Check if period length matches dimensions
    if period_length == structures.E8['dimension']:
        connections.append(f"Period length = E8 dimension (8)")
    
    if period_length in [structures.MATHIEU['M22_degree'], 
                         structures.MATHIEU['M23_degree'], 
                         structures.MATHIEU['M24_degree']]:
        connections.append(f"Period length matches Mathieu group degree")
    
    return connections

# ============================================================================
# MAIN ANALYSIS FUNCTION
# ============================================================================

def deep_analysis(n, period_str, period_int):
    """Perform comprehensive pattern analysis"""
    
    print(f"\n{'='*80}")
    print(f"DEEP PATTERN ANALYSIS: 1/{n}")
    print(f"{'='*80}")
    
    structures = ExceptionalStructures()
    
    # 1. Find subsequence matches with known constants
    print("\n>> SUBSEQUENCE MATCHES WITH EXCEPTIONAL STRUCTURES:")
    
    all_target_numbers = (
        list(structures.E8.values())[:5] +  # First 5 E8 constants
        list(structures.GOLAY.values())[:8] +
        list(structures.LEECH.values())[:4] +
        structures.SPECIAL_NUMBERS['powers_of_3'] +
        structures.SPECIAL_NUMBERS['powers_of_2'] +
        structures.MONSTER['supersingular_primes']
    )
    
    # Remove non-integers and make unique
    target_numbers = list(set([x for x in all_target_numbers if isinstance(x, int) and 0 < x < 10**6]))
    
    matches = find_subsequences(period_str, target_numbers)
    found_matches = [m for m in matches if m['count'] > 0]
    
    if found_matches:
        print(f"\n   Found {len(found_matches)} number patterns in period digits:")
        for match in found_matches[:15]:  # Show first 15
            print(f"     {match['number']:8d} appears {match['count']} time(s) at positions {match['positions'][:5]}")
    else:
        print("   No direct number matches found")
    
    # Special check for 729 (ternary Golay codewords AND appears in 1/137)
    if '729' in period_str:
        print(f"\n   ⭐ SPECIAL: 729 (3^6, ternary Golay codewords) found in period!")
    
    # 2. Modular arithmetic patterns
    print("\n>> MODULAR ARITHMETIC CONNECTIONS:")
    
    # Flatten all structure constants
    all_constants = {}
    for key, val in structures.E8.items():
        if isinstance(val, int):
            all_constants[f'E8_{key}'] = val
    for key, val in structures.GOLAY.items():
        if isinstance(val, int):
            all_constants[f'Golay_{key}'] = val
    for key, val in structures.LEECH.items():
        if isinstance(val, int):
            all_constants[f'Leech_{key}'] = val
    
    mod_matches = find_modular_matches(period_int, all_constants)
    
    if mod_matches:
        print(f"\n   Found {len(mod_matches)} modular relationships:")
        for match in mod_matches[:10]:
            print(f"     Period mod {match['structure']} ({match['value']}) = {match['remainder']} ({match['type']})")
    else:
        print("   No special modular relationships found")
    
    # 3. Digit pattern analysis
    print("\n>> DIGIT PATTERN ANALYSIS:")
    
    digit_patterns = find_digit_patterns(period_str)
    
    print(f"\n   Digit frequency:")
    for digit, count in sorted(digit_patterns['digit_frequency'].items()):
        print(f"     {digit}: {count} times")
    
    if digit_patterns['runs']:
        print(f"\n   Consecutive digit runs:")
        for run in digit_patterns['runs'][:5]:
            print(f"     {run['digit']} repeated {run['length']} times at position {run['position']}")
    
    if digit_patterns['symmetries']:
        print(f"\n   Symmetric patterns (palindromes):")
        for sym in digit_patterns['symmetries'][:5]:
            if sym['type'] == 'full_palindrome':
                print(f"     FULL PALINDROME of length {sym['length']}")
            else:
                print(f"     Partial: '{sym['string']}' at position {sym['position']}")
    
    # 4. Arithmetic sequences
    print("\n>> ARITHMETIC PROGRESSIONS IN DIGITS:")
    
    arith_seqs = analyze_arithmetic_sequences(period_str)
    if arith_seqs:
        for seq in arith_seqs[:5]:
            print(f"     {seq['sequence']} (diff={seq['difference']}) at position {seq['position']}")
    else:
        print("   No arithmetic progressions found")
    
    # 5. High-level structural connections
    print("\n>> STRUCTURAL CONNECTIONS:")
    
    factor_connections = find_factor_connections(period_int, len(period_str), structures)
    if factor_connections:
        for conn in factor_connections:
            print(f"   ⭐ {conn}")
    else:
        print("   No direct structural connections found")
    
    # 6. Statistical analysis
    print("\n>> STATISTICAL PROPERTIES:")
    
    digits = [int(d) for d in period_str]
    mean = sum(digits) / len(digits)
    variance = sum((d - mean)**2 for d in digits) / len(digits)
    
    print(f"   Mean digit value: {mean:.3f}")
    print(f"   Variance: {variance:.3f}")
    print(f"   Entropy: {calculate_entropy(period_str):.3f} bits")

def calculate_entropy(s):
    """Calculate Shannon entropy of digit string"""
    from math import log2
    freq = Counter(s)
    length = len(s)
    entropy = -sum((count/length) * log2(count/length) for count in freq.values())
    return entropy

# ============================================================================
# PERIOD COMPUTATION (from previous script)
# ============================================================================

def get_period_digits(n, max_digits=500):
    """Extract the repeating period digits from 1/n"""
    decimal_digits = []
    remainder = 1
    seen = {}
    position = 0
    
    while remainder != 0 and position < max_digits:
        if remainder in seen:
            period_start = seen[remainder]
            period = ''.join(decimal_digits[period_start:])
            return period_start, period
        
        seen[remainder] = position
        remainder *= 10
        digit = remainder // n
        decimal_digits.append(str(digit))
        remainder = remainder % n
        position += 1
    
    return 0, ''.join(decimal_digits)

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    print("\n" + "=" * 80)
    print("DEEP PATTERN ANALYSIS")
    print("Searching for connections between periods and exceptional structures")
    print("=" * 80)
    
    # Numbers to analyze
    analyses = [
        (137, "Fine-Structure ~1/137"),
        (92, "Uranium (Element 92)"),
        (173, "Feynman Limit"),
        (13703600, "Fine-Structure 137.036 (as 137036/1000, reduced)"),  # Actually we'd use 34259
        (137036, "Fine-Structure Integer 137036"),
        (137026, "Fine-Structure variant 137.026 (if requested)"),
    ]
    
    for n, name in analyses:
        print(f"\n{'#'*80}")
        print(f"Analyzing: {name}")
        print(f"{'#'*80}")
        
        # Get period
        print(f"\n>> Computing period for 1/{n}...")
        period_start, period_str = get_period_digits(n, max_digits=500)
        
        if not period_str or period_str == '0':
            print(f"   Could not compute period for {n}")
            continue
        
        period_length = len(period_str)
        period_int = int(period_str) if period_str else 0
        
        print(f"   Period: {period_str[:80]}{'...' if len(period_str) > 80 else ''}")
        print(f"   Length: {period_length}")
        
        # Perform deep analysis
        if period_int > 0:
            deep_analysis(n, period_str, period_int)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
