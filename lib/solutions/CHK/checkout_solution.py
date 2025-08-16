from collections import Counter
from string import ascii_uppercase

UNIT_PRICE = {
    "A": 50, "B": 30, "C": 20, "D": 15, "E": 40,
    "F": 10, "G": 20, "H": 10, "I": 35, "J": 60,
    "K": 70, "L": 90, "M": 15, "N": 40, "O": 10,
    "P": 50, "Q": 30, "R": 50, "S": 20, "T": 20,
    "U": 40, "V": 50, "W": 20, "X": 17, "Y": 20,
    "Z": 21,
}

BUNDLE_DEALS = {
    "A": {"PRICE_FOR_5": 200, "PRICE_FOR_3": 130},
    "B": {"PRICE_FOR_2": 45},
    "H": {"PRICE_FOR_10": 80, "PRICE_FOR_5": 45},
    "K": {"PRICE_FOR_2": 120},           # R5
    "P": {"PRICE_FOR_5": 200},
    "Q": {"PRICE_FOR_3": 80},
    "V": {"PRICE_FOR_3": 130, "PRICE_FOR_2": 90},

    # Self-freebies expressed as bundles priced via UNIT_PRICE
    # F: buy 2 get 1 free -> every 3 cost 2×F
    "F": {"PRICE_FOR_3": 2 * UNIT_PRICE["F"]},
    # U: 3U get one free -> every 4 cost 3×U
    "U": {"PRICE_FOR_4": 3 * UNIT_PRICE["U"]},
}


class CheckoutSolution:

    def _validate_and_count(self, skus):
        if not isinstance(skus, str):
            return None
        if skus == "":
            return Counter()  # empty is valid -> totals 0
        allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if any(ch not in allowed for ch in skus):
            return None
        return Counter(skus)

    # ---------------- Prices (single-item only; no cross-item effects here) ----------------

    # A: 3A=130, 5A=200 (always pick cheapest)
    def price_A(self, amount):
        up = UNIT_PRICE['A']
        best = amount * up
        for num5 in range(amount // 5 + 1):
            rem_after_5 = amount - 5 * num5
            for num3 in range(rem_after_5 // 3 + 1):
                rem = rem_after_5 - 3 * num3
                total = num5 * 200 + num3 * 130 + rem * up
                best = min(best, total)
        return best

    def price_B(self, amount):  # 2B=45
        up = UNIT_PRICE['B']
        return (amount // 2) * 45 + (amount % 2) * up

    def price_C(self, amount): return amount * UNIT_PRICE['C']
    def price_D(self, amount): return amount * UNIT_PRICE['D']
    def price_E(self, amount): return amount * UNIT_PRICE['E']

    # F: buy 2 get 1 free -> each 3 costs 2*F
    def price_F(self, amount):
        up = UNIT_PRICE['F']
        groups = amount // 3
        rem = amount % 3
        return groups * (2 * up) + rem * up

    def price_G(self, amount): return amount * UNIT_PRICE['G']

    # H: 5H=45, 10H=80 (pick cheapest)
    def price_H(self, amount):
        up = UNIT_PRICE['H']
        best = amount * up
        for num10 in range(amount // 10 + 1):
            rem10 = amount - 10 * num10
            for num5 in range(rem10 // 5 + 1):
                rem = rem10 - 5 * num5
                total = num10 * 80 + num5 * 45 + rem * up
                best = min(best, total)
        return best

    def price_I(self, amount): return amount * UNIT_PRICE['I']
    def price_J(self, amount): return amount * UNIT_PRICE['J']

    # K (R5): unit=70, 2K=120
    def price_K(self, amount):
        up = UNIT_PRICE['K']
        return (amount // 2) * 120 + (amount % 2) * up

    def price_L(self, amount): return amount * UNIT_PRICE['L']
    def price_M(self, amount): return amount * UNIT_PRICE['M']
    def price_N(self, amount): return amount * UNIT_PRICE['N']
    def price_O(self, amount): return amount * UNIT_PRICE['O']

    # P: 5P=200
    def price_P(self, amount):
        up = UNIT_PRICE['P']
        return (amount // 5) * 200 + (amount % 5) * up

    # Q: 3Q=80
    def price_Q(self, amount):
        up = UNIT_PRICE['Q']
        return (amount // 3) * 80 + (amount % 3) * up

    def price_R(self, amount): return amount * UNIT_PRICE['R']

    # R5 base prices (group offer handled separately for S/T/X/Y/Z)
    def price_S(self, amount): return amount * UNIT_PRICE['S']
    def price_T(self, amount): return amount * UNIT_PRICE['T']
    def price_W(self, amount): return amount * UNIT_PRICE['W']
    def price_X(self, amount): return amount * UNIT_PRICE['X']
    def price_Y(self, amount): return amount * UNIT_PRICE['Y']
    def price_Z(self, amount): return amount * UNIT_PRICE['Z']

    # U: 3U get 1 U free -> per 4 pay 3 * U
    def price_U(self, amount):
        up = UNIT_PRICE['U']
        groups = amount // 4
        rem = amount % 4
        return groups * (3 * up) + rem * up

    # V: 2V=90, 3V=130 (choose best)
    def price_V(self, amount):
        up = UNIT_PRICE['V']
        best = amount * up
        for num3 in range(amount // 3 + 1):
            rem3 = amount - 3 * num3
            num2 = rem3 // 2
            rem = rem3 % 2
            total = num3 * 130 + num2 * 90 + rem * up
            best = min(best, total)
        return best

    # ----------- Freebie adjusters (separate from pricing) -----------

    def calculate_amount_of_B(self, amount_B, amount_E):
        """2E -> 1B free"""
        return max(0, amount_B - (amount_E // 2))

    def calculate_amount_of_Q(self, amount_Q, amount_R):
        """3R -> 1Q free"""
        return max(0, amount_Q - (amount_R // 3))

    def adjust_M_for_N(self, amount_M, amount_N):
        """3N -> 1M free"""
        return max(0, amount_M - (amount_N // 3))

    # ----------- Group offer: any 3 of (S,T,X,Y,Z) for 45 -----------

    def price_group_STXYZ(self, counts):
        """
        counts: dict with keys 'S','T','X','Y','Z' -> quantities
        Strategy: discount the most expensive items first; every 3 items -> 45.
        """
        group = ('S', 'T', 'X', 'Y', 'Z')
        prices = []
        for sku in group:
            prices.extend([UNIT_PRICE[sku]] * counts.get(sku, 0))
        if not prices:
            return 0
        total_base = sum(prices)
        groups = len(prices) // 3
        if groups == 0:
            return total_base
        prices.sort(reverse=True)
        replaced_sum = sum(prices[:3 * groups])
        return total_base - replaced_sum + groups * 45

    # ------------------------------ checkout ------------------------------

    def checkout(self, skus):
        counts = self._validate_and_count(skus)
        if counts is None:
            return -1

        amount = {sku: counts.get(sku, 0) for sku in ascii_uppercase}

        # Apply cross-item freebies by adjusting the affected counts
        eff_B = self.calculate_amount_of_B(amount['B'], amount['E'])
        eff_M = self.adjust_M_for_N(amount['M'], amount['N'])
        eff_Q = self.calculate_amount_of_Q(amount['Q'], amount['R'])

        # Start with adjusted counts overrides
        override_counts = {'B': eff_B, 'M': eff_M, 'Q': eff_Q}

        # Handle the group offer for S/T/X/Y/Z, then zero them so they don't get priced twice
        group_total = self.price_group_STXYZ({k: amount[k] for k in ('S', 'T', 'X', 'Y', 'Z')})
        for k in ('S', 'T', 'X', 'Y', 'Z'):
            override_counts[k] = 0

        # Sum everything else via their price_* methods
        items_total = sum(
            getattr(self, f"price_{sku}")(override_counts.get(sku, amount[sku]))
            for sku in ascii_uppercase
            if getattr(self, f"price_{sku}", None) and override_counts.get(sku, amount[sku]) > 0
        )

        return group_total + items_total


# ----------------- Round 5 quick tests (same style) -----------------

def run_tests_r5():
    checkout = CheckoutSolution()

    print("Invalid cases:")
    print(checkout.checkout("a"), "expected -1")
    print(checkout.checkout("-"), "expected -1")
    print(checkout.checkout("ABCa"), "expected -1")
    print(checkout.checkout(123), "expected -1")
    print(checkout.checkout(None), "expected -1")
    print(checkout.checkout("A*B"), "expected -1")

    print("\nSimple A offers:")
    print(checkout.checkout("AAA"), "expected 130")
    print(checkout.checkout("AAAAA"), "expected 200")
    print(checkout.checkout("AAAAAA"), "expected 250")
    print(checkout.checkout("AAAAAAA"), "expected 300")
    print(checkout.checkout("AAAAAAAA"), "expected 330")

    print("\nB & E interactions:")
    print(checkout.checkout("BB"), "expected 45")
    print(checkout.checkout("BBB"), "expected 75")
    print(checkout.checkout("E"), "expected 40")
    print(checkout.checkout("EEB"), "expected 80")
    print(checkout.checkout("EEBB"), "expected 110")
    print(checkout.checkout("EEEEBBB"), "expected 190")

    print("\nF offer:")
    print(checkout.checkout("F"), "expected 10")
    print(checkout.checkout("FF"), "expected 20")
    print(checkout.checkout("FFF"), "expected 20")
    print(checkout.checkout("FFFF"), "expected 30")
    print(checkout.checkout("FFFFF"), "expected 40")
    print(checkout.checkout("FFFFFF"), "expected 40")

    print("\nUpdated K pricing (K=70, 2K=120):")
    print(checkout.checkout("K"), "expected 70")
    print(checkout.checkout("KK"), "expected 120")
    print(checkout.checkout("KKK"), "expected 190")  # 120 + 70

    print("\nGroup offer: any 3 of (S,T,X,Y,Z) for 45")
    print(checkout.checkout("S"), "expected 20")
    print(checkout.checkout("T"), "expected 20")
    print(checkout.checkout("X"), "expected 17")
    print(checkout.checkout("Y"), "expected 20")
    print(checkout.checkout("Z"), "expected 21")
    print(checkout.checkout("STX"), "expected 45")
    print(checkout.checkout("SZZ"), "expected 45")
    print(checkout.checkout("SSS"), "expected 45")
    print(checkout.checkout("ZZZ"), "expected 45")
    print(checkout.checkout("XXX"), "expected 45")
    print(checkout.checkout("STXYZ"), "expected 82")
    print(checkout.checkout("ZZZZ"), "expected 66")
    print(checkout.checkout("ZZZXX"), "expected 79")
    print(checkout.checkout("SSTT"), "expected 65")
    print(checkout.checkout("STXX"), "expected 62")
    print(checkout.checkout("XXXXXX"), "expected 90")

    print("\nOther unchanged offers:")
    print(checkout.checkout("HHHHH"), "expected 45")
    print(checkout.checkout("HHHHHHHHHH"), "expected 80")
    print(checkout.checkout("HHHHHHHHHHH"), "expected 90")
    print(checkout.checkout("I"), "expected 35")
    print(checkout.checkout("J"), "expected 60")
    print(checkout.checkout("L"), "expected 90")
    print(checkout.checkout("P"*5), "expected 200")
    print(checkout.checkout("QQQ"), "expected 80")
    print(checkout.checkout("VV"), "expected 90")
    print(checkout.checkout("VVV"), "expected 130")
    print(checkout.checkout("VVVV"), "expected 180")
    print(checkout.checkout("U"*4), "expected 120")

    print("\nMixed baskets (with group + freebies):")
    print(checkout.checkout("ABCD"), "expected 115")
    print(checkout.checkout("ABCDE"), "expected 155")
    print(checkout.checkout("NNNM"), "expected 120")
    print(checkout.checkout("NNNMM"), "expected 135")
    print(checkout.checkout("RRRQ"), "expected 150")
    print(checkout.checkout("RRRQQQ"), "expected 210")
    print(checkout.checkout("EEBZ"), "expected 101")
    print(checkout.checkout("EEFFBZZZ"), "expected 145")
    print(checkout.checkout("FFFABC"), "expected 120")
    print(checkout.checkout("STXYZAB"), "expected 162")  # 82 + A(50) + B(30)
    print(checkout.checkout("RRRQQQNNNM"), "expected 330")

    print("\nEdge cases:")
    print(checkout.checkout(""), "expected 0")


if __name__ == "__main__":
    run_tests_r5()
