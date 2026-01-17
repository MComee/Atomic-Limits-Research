#!/usr/bin/env python3
"""
CLARIFICATION: What is the "ternary doubling" claim?
Testing EXACTLY what the reviewer is disputing
"""

def get_period_digits(n, max_digits=500):
    """Extract the actual repeating period digits from 1/n"""
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

def to_base(num, base):
    """Convert number to given base, return string"""
    if num == 0:
        return "0"
    digits = []
    while num:
        digits.append(str(num % base))
        num //= base
    return ''.join(reversed(digits))

print("="*80)
print("TERNARY DOUBLING CLARIFICATION")
print("="*80)

print("\n1/92 Analysis:")
print("-"*80)

# Get the decimal period
_, period_str = get_period_digits(92)
period_length_decimal = len(period_str)
period_int = int(period_str)

print(f"Decimal period string: {period_str}")
print(f"Decimal period LENGTH: {period_length_decimal}")
print(f"Period as INTEGER: {period_int}")

# Convert the period INTEGER to base-3
ternary_str = to_base(period_int, 3)
ternary_length = len(ternary_str)

print(f"\nTernary representation of {period_int}:")
print(f"  Ternary string: {ternary_str[:60]}{'...' if len(ternary_str) > 60 else ''}")
print(f"  Ternary LENGTH: {ternary_length}")

print(f"\nRatio: {ternary_length} / {period_length_decimal} = {ternary_length / period_length_decimal:.4f}")

if ternary_length == 44:
    print("✓ OUR CLAIM: Ternary has 44 digits = 2 × 22")
elif ternary_length == 22:
    print("✗ REVIEWER: Ternary has 22 digits (same as decimal)")
else:
    print(f"? ACTUAL: Ternary has {ternary_length} digits")

print("\n" + "="*80)
print("EXPECTED THEORETICAL LENGTH")
print("="*80)

import math

# Theoretical prediction
# A number with n decimal digits has value ~ 10^n
# In base 3, this should have ~ n × log₃(10) digits

expected_ternary = period_length_decimal * math.log(10) / math.log(3)
print(f"Period has {period_length_decimal} decimal digits")
print(f"Expected ternary length ≈ {period_length_decimal} × log₃(10)")
print(f"                        ≈ {period_length_decimal} × {math.log(10)/math.log(3):.4f}")
print(f"                        ≈ {expected_ternary:.2f}")

print(f"\nActual ternary length: {ternary_length}")
print(f"Difference from expected: {ternary_length - expected_ternary:.2f}")

if abs(ternary_length - 2 * period_length_decimal) < 1:
    print(f"\n⭐ EXACT 2× DOUBLING CONFIRMED")
elif abs(ternary_length - expected_ternary) < 2:
    print(f"\n✓ Matches theoretical expectation (no anomaly)")
else:
    print(f"\n? Neither 2× nor theoretical expectation")

print("\n" + "="*80)
print("WHAT WE CLAIMED vs WHAT REVIEWER TESTED")
print("="*80)

print("\nOUR ORIGINAL CLAIM:")
print("  'The ternary representation of 1/92's period integer has")
print("   44 digits, which is EXACTLY 2× the decimal period of 22'")

print("\nREVIEWER'S INTERPRETATION:")
print("  They may have tested multiplicative order in base-3")
print("  (i.e., period of 1/92 when written in base-3 notation)")
print("  which would indeed be 22")

print("\nWHAT WE NEED TO VERIFY:")
print("  Does the INTEGER formed by the decimal period,")
print("  when converted to base-3, have 44 digits or 22?")

print(f"\n✓ ANSWER: {ternary_length} digits")

if ternary_length == 44:
    print("\n✓✓✓ WE ARE CORRECT - Reviewer misunderstood our claim")
elif ternary_length == 22:
    print("\n✗✗✗ REVIEWER IS CORRECT - Our code was wrong")
