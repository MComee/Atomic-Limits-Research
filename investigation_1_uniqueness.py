#!/usr/bin/env python3
"""
Investigation 1: Pattern Uniqueness Analysis
Tests if patterns found in 137, 92, 173 are unique or common to all numbers
with periods 8, 22, 43
"""

import sys
from collections import Counter

def get_period_digits(n, max_digits=500):
    """Extract repeating period digits from 1/n"""
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

def find_period_length(n, max_length=500):
    """Find period length using multiplicative order"""
    remainders = {}
    remainder = 1
    position = 0
    
    while remainder != 0 and position < max_length:
        if remainder in remainders:
            return position - remainders[remainder]
        remainders[remainder] = position
        remainder = (remainder * 10) % n
        position += 1
    return 0

def to_base(num, base):
    """Convert number to given base"""
    if num == 0:
        return "0"
    digits = []
    while num:
        digits.append(str(num % base))
        num //= base
    return ''.join(reversed(digits))

def analyze_patterns(n, period_str):
    """Analyze patterns for a given number"""
    if not period_str or period_str == '0':
        return None
    
    period_int = int(period_str)
    digits = [int(d) for d in period_str]
    digit_sum = sum(digits)
    
    # Binary analysis
    binary = bin(period_int)[2:]
    ones = binary.count('1')
    zeros = binary.count('0')
    binary_balanced = (ones == zeros)
    
    # Ternary analysis
    ternary = to_base(period_int, 3)
    ternary_doubles = (len(ternary) == 2 * len(period_str))
    
    # Octal analysis
    octal = oct(period_int)[2:]
    octal_is_24 = (len(octal) == 24)
    
    # Digit sum analysis
    digit_sum_has_9_factor = (digit_sum % 9 == 0)
    digit_sum_has_3_squared = (digit_sum % 9 == 0) and ((digit_sum // 9) % 1 == 0)
    
    # Check for 729
    contains_729 = ('729' in period_str)
    
    # All 10 digits present
    all_digits = (len(set(digits)) == 10)
    
    return {
        'n': n,
        'period_length': len(period_str),
        'digit_sum': digit_sum,
        'digit_sum_div_9': digit_sum_has_9_factor,
        'binary_balanced': binary_balanced,
        'ternary_doubles': ternary_doubles,
        'octal_is_24': octal_is_24,
        'contains_729': contains_729,
        'all_digits': all_digits,
        'binary_ones': ones,
        'binary_zeros': zeros,
        'ternary_length': len(ternary),
        'octal_length': len(octal),
    }

def find_numbers_with_period(target_period, max_n=1000):
    """Find all numbers up to max_n with given period"""
    print(f"\nSearching for numbers with period {target_period} (up to {max_n})...")
    results = []
    
    for n in range(2, max_n + 1):
        if n % 100 == 0:
            print(f"  Progress: {n}/{max_n}", end='\r')
        
        period_length = find_period_length(n)
        if period_length == target_period:
            results.append(n)
    
    print(f"  Found {len(results)} numbers" + " " * 20)
    return results

def compare_patterns(numbers_list, target_n, target_name):
    """Compare patterns of target number vs all others with same period"""
    print(f"\n{'='*80}")
    print(f"PATTERN UNIQUENESS ANALYSIS: {target_n} ({target_name})")
    print(f"{'='*80}")
    
    # Analyze all numbers
    all_patterns = []
    target_patterns = None
    
    for n in numbers_list:
        _, period_str = get_period_digits(n)
        patterns = analyze_patterns(n, period_str)
        
        if patterns:
            all_patterns.append(patterns)
            if n == target_n:
                target_patterns = patterns
    
    if not target_patterns:
        print(f"Could not analyze {target_n}")
        return
    
    print(f"\nTarget: {target_n}")
    print(f"Period length: {target_patterns['period_length']}")
    print(f"Comparing against {len(all_patterns)} numbers with same period...\n")
    
    # Count how many have each pattern
    patterns_to_check = [
        ('digit_sum_div_9', "Digit sum divisible by 9"),
        ('binary_balanced', "Binary perfect balance"),
        ('ternary_doubles', "Ternary length = 2× period"),
        ('octal_is_24', "Octal length = 24"),
        ('contains_729', "Contains '729'"),
        ('all_digits', "All 10 digits present"),
    ]
    
    print("Pattern prevalence:")
    print("-" * 80)
    
    for pattern_key, pattern_desc in patterns_to_check:
        count = sum(1 for p in all_patterns if p[pattern_key])
        percentage = 100 * count / len(all_patterns)
        target_has = target_patterns[pattern_key]
        
        status = "✓ YES" if target_has else "✗ NO"
        
        print(f"{pattern_desc:40} {status:8}  |  {count}/{len(all_patterns)} ({percentage:5.1f}%)")
    
    # Count how many have ALL patterns that target has
    target_pattern_keys = [key for key, _ in patterns_to_check if target_patterns[key]]
    
    if target_pattern_keys:
        matching_all = sum(1 for p in all_patterns if all(p[key] for key in target_pattern_keys))
        print(f"\n{'='*80}")
        print(f"Numbers matching ALL of {target_n}'s patterns: {matching_all}/{len(all_patterns)}")
        
        if matching_all == 1:
            print(f"⭐ {target_n} is UNIQUE - no other number has this combination!")
        elif matching_all < 5:
            print(f"⭐ {target_n} is RARE - very few numbers share this combination")
            print(f"\nOther numbers with all patterns:")
            for p in all_patterns:
                if all(p[key] for key in target_pattern_keys) and p['n'] != target_n:
                    print(f"  {p['n']}")
        else:
            print(f"Pattern combination is relatively common")

def main():
    print("\n" + "="*80)
    print("INVESTIGATION 1: PATTERN UNIQUENESS ANALYSIS")
    print("Testing if 137, 92, 173 are truly exceptional")
    print("="*80)
    
    # Test each target number
    investigations = [
        (8, 137, "Fine-Structure Constant", 1000),
        (22, 92, "Uranium", 1000),
        (43, 173, "Feynman Limit", 500),
    ]
    
    for period, target_n, name, max_search in investigations:
        numbers_with_period = find_numbers_with_period(period, max_search)
        compare_patterns(numbers_with_period, target_n, name)
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("\nIf 137, 92, and 173 show UNIQUE or RARE pattern combinations,")
    print("this strengthens the case that they are selected for special properties.")
    print("\nIf patterns are COMMON, this weakens the significance of the finding.")
    print("="*80)
    print()

if __name__ == "__main__":
    main()
