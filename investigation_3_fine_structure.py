#!/usr/bin/env python3
"""
Investigation 3: Fine-Structure Constant 1/137.036
Tests if the actual NIST value preserves the dimension-8 encoding
"""

from math import gcd

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

def to_base(num, base):
    """Convert number to given base"""
    if num == 0:
        return "0"
    digits = []
    while num:
        digits.append(str(num % base))
        num //= base
    return ''.join(reversed(digits))

def analyze_rational(numerator, denominator, name):
    """Analyze a rational number p/q"""
    print(f"\n{'='*80}")
    print(f"ANALYSIS: {numerator}/{denominator} ({name})")
    print(f"{'='*80}")
    
    # Reduce to lowest terms
    g = gcd(numerator, denominator)
    num_reduced = numerator // g
    den_reduced = denominator // g
    
    decimal_value = numerator / denominator
    
    print(f"\nOriginal: {numerator}/{denominator} = {decimal_value}")
    print(f"Reduced: {num_reduced}/{den_reduced}")
    print(f"GCD: {g}")
    
    # For 1/(p/q) = q/p, the period is determined by p (the denominator in reduced form)
    print(f"\nReciprocal: 1/{decimal_value:.10f} = {den_reduced}/{num_reduced}")
    print(f"\nPeriod structure determined by denominator: {num_reduced}")
    
    # Analyze the denominator
    _, period_str = get_period_digits(num_reduced)
    period_length = len(period_str) if period_str else 0
    
    if period_length == 0:
        print("Could not compute period")
        return None
    
    print(f"\n{'-'*80}")
    print(f"PERIOD ANALYSIS")
    print(f"{'-'*80}")
    
    print(f"\nPeriod: {period_str[:70]}{'...' if len(period_str) > 70 else ''}")
    print(f"Period length: {period_length}")
    
    # Compare to dimension 8
    if period_length == 8:
        print(f"\n⭐ PERIOD LENGTH = 8 (E8 dimension!) ⭐")
        print(f"The dimension-8 encoding is PRESERVED!")
    elif period_length % 8 == 0:
        print(f"\n⚠ Period length = {period_length} = {period_length//8} × 8")
        print(f"Related to dimension 8, but not exactly 8")
    else:
        print(f"\n❌ Period length = {period_length}")
        print(f"Does NOT match dimension 8")
        print(f"The 0.036 correction DESTROYS the encoding")
    
    # Digit analysis
    if period_str and period_str != '0':
        period_int = int(period_str)
        digits = [int(d) for d in period_str]
        digit_sum = sum(digits)
        
        print(f"\nDigit sum: {digit_sum}")
        if digit_sum % 9 == 0:
            print(f"  Divisible by 9 ✓")
            if digit_sum % 9 == 0 and (digit_sum // 9) % 3 == 0:
                print(f"  Contains factor 3² ✓")
        
        # Check for 729
        if '729' in period_str:
            print(f"\n⭐ Contains '729' (3^6, ternary Golay codewords)!")
        
        # Binary analysis
        binary = bin(period_int)[2:]
        ones = binary.count('1')
        zeros = binary.count('0')
        
        print(f"\nBinary:")
        print(f"  Length: {len(binary)} bits")
        print(f"  Ones: {ones}, Zeros: {zeros}")
        if ones == zeros:
            print(f"  ⭐ Perfect balance!")
    
    return {
        'period_length': period_length,
        'matches_8': (period_length == 8),
        'period_str': period_str,
        'denominator': num_reduced,
    }

def compare_to_ideal():
    """Compare 137.036 to ideal 137"""
    print(f"\n{'='*80}")
    print("COMPARISON: 1/137 vs 1/137.036")
    print(f"{'='*80}")
    
    # Analyze ideal
    print("\n[A] IDEAL: 1/137")
    _, period_137 = get_period_digits(137)
    print(f"  Period: {period_137}")
    print(f"  Length: {len(period_137)} (dimension 8 ✓)")
    print(f"  Contains 729: {'Yes ⭐' if '729' in period_137 else 'No'}")
    
    # Analyze actual
    print("\n[B] ACTUAL: 1/137.036")
    print("  Approximated as 1000/137036 = 250/34259 (reduced)")
    
    result = analyze_rational(137036, 1000, "Fine-Structure α⁻¹")
    
    if result:
        print(f"\n{'-'*80}")
        print("VERDICT:")
        print(f"{'-'*80}")
        
        if result['matches_8']:
            print("""
⭐⭐⭐ EXTRAORDINARY RESULT ⭐⭐⭐

The actual fine-structure constant (137.036) PRESERVES the dimension-8 encoding!

This means:
1. The pattern is robust to small corrections
2. The 0.036 deviation doesn't break the mathematical structure
3. QED corrections may be constrained by this encoding
4. The connection to E8 is even stronger than expected

This is PROFOUND - it suggests the physical constant value is not arbitrary
but constrained by mathematical structure at a deep level.
""")
        else:
            print(f"""
The actual fine-structure constant has period length {result['period_length']}, not 8.

This means:
1. The dimension-8 encoding is specific to the idealized 1/137
2. The 0.036 correction breaks the mathematical pattern
3. The proximity to 1/137 may be anthropic or coincidental
4. Physical value differs from mathematical "ideal"

However, this doesn't invalidate the finding - it shows that 137 (the integer)
has special properties even if the physical constant differs slightly.
""")

def investigate_nearby_values():
    """Check values near 137 for comparison"""
    print(f"\n{'='*80}")
    print("NEARBY VALUES INVESTIGATION")
    print(f"{'='*80}")
    print("\nChecking integers near 137 for period length:")
    
    for n in [135, 136, 137, 138, 139]:
        _, period = get_period_digits(n)
        period_length = len(period) if period else 0
        marker = " ⭐ E8!" if period_length == 8 else ""
        print(f"  1/{n}: period length = {period_length}{marker}")
    
    print("\nThis shows how special (or not) 137 is among nearby integers.")

def qed_correction_analysis():
    """Analyze QED corrections and their relationship to patterns"""
    print(f"\n{'='*80}")
    print("QED CORRECTION ANALYSIS")
    print(f"{'='*80}")
    
    print("""
The fine-structure constant in QED:

α⁻¹ = 137.035999177(21) [NIST 2022]

Deviation from 137:
  Δ = 137.036 - 137 = 0.036
  Relative: 0.026%

QED Corrections:
- Vacuum polarization: ~ α/π ≈ 0.00232
- Vertex corrections: ~ α/π × log(...)
- Higher orders: (α/π)² and beyond

The 0.036 is approximately 15 × (α/π), suggesting ~15 virtual particle loops
or a sum of many contributions.

QUESTION: Can we derive 0.036 from E8 structure?

Speculative calculation:
- E8 has 240 roots
- 240 / 137 = 1.7518
- If α involves 240/137 in some way...
- Connection to quantum corrections?

This requires deeper theoretical work in:
1. E8 gauge theory
2. Octonionic quantum mechanics
3. Exceptional symmetries in QED

PREDICTION: If connection is real, α value should be derivable from
exceptional structure constants (240, 30, 8, etc.) through a formula
we haven't discovered yet.
""")

def main():
    print("\n" + "="*80)
    print("INVESTIGATION 3: FINE-STRUCTURE CONSTANT 1/137.036")
    print("Does the actual value preserve dimension-8 encoding?")
    print("="*80)
    
    # Main analysis
    compare_to_ideal()
    
    # Context
    investigate_nearby_values()
    
    # Theoretical implications
    qed_correction_analysis()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("""
Key Question: Does α⁻¹ = 137.036 preserve the dimension-8 encoding?

Run this script to find out if:
- The period length of 34259 (reduced form of 137.036) equals 8
- Or if it's a multiple of 8
- Or if it's completely different

The answer has profound implications for whether the physical constant
is constrained by mathematical structure.
""")

if __name__ == "__main__":
    main()
