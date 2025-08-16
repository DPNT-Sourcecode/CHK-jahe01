from collections import Counter
from string import ascii_uppercase

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

    # ---------------- Prices (single-item only) ----------------

    # A calculation - always pick cheapest combination (3A=130, 5A=200)
    def price_A(self, amount):
        best = amount * 50
        for num5 in range(amount // 5 + 1):
            rem_after_5 = amount - 5 * num5
            for num3 in range(rem_after_5 // 3 + 1):
                rem = rem_after_5 - 3 * num3
                total = num5 * 200 + num3 * 130 + rem * 50
                best = min(best, total)
        return best

    def price_B(self, amount):                   # 2B = 45
        return (amount // 2) * 45 + (amount % 2) * 30

    def price_C(self, amount): return amount * 20
    def price_D(self, amount): return amount * 15
    def price_E(self, amount): return amount * 40
    def price_F(self, amount):                   # 3F = 20
        groups = amount // 3
        rem = amount % 3
        return groups * 20 + rem * 10

    def price_G(self, amount): return amount * 20

    def price_H(self, amount):                   # 5H=45, 10H=80
        best = amount * 10
        for num10 in range(amount // 10 + 1):
            rem10 = amount - 10 * num10
            for num5 in range(rem10 // 5 + 1):
                rem = rem10 - 5 * num5
                total = num10 * 80 + num5 * 45 + rem * 10
                best = min(best, total)
        return best

    def price_I(self, amount): return amount * 35
    def price_J(self, amount): return amount * 60

    # R5: K = 70, 2K = 120
    def price_K(self, amount):
        return (amount // 2) * 120 + (amount % 2) * 70

    def price_L(self, amount): return amount * 90
    def price_M(self, amount): return amount * 15
    def price_N(self, amount): return amount * 40
    def price_O(self, amount): return amount * 10
    def price_P(self, amount): return (amount // 5) * 200 + (amount % 5) * 50
    def price_Q(self, amount): return (amount // 3) * 80 + (amount % 3) * 30
    def price_R(self, amount): return amount * 50

    # R5: S/T=20, X=17, Y=20, Z=21 (base prices, but group offer handled separately)
    def price_S(self, amount): return amount * 20
    def price_T(self, amount): return amount * 20
    def price_W(self, amount): return amount * 20
    def price_X(self, amount): return amount * 17
    def price_Y(self, amount): return amount * 20
    def price_Z(self, amount): return amount * 21

    def price_U(self, amount):                   # 3U get 1 U free -> per 4 pay 3
        groups = amount // 4
        rem = amount % 4
        return groups * (3 * 40) + rem * 40

    def price_V(self, amount):                   # 2V=90, 3V=130 (choose best)
        best = amount * 50
        for num3 in range(amount // 3 + 1):
            rem3 = amount - 3 * num3
            num2 = rem3 // 2
            rem = rem3 % 2
            total = num3 * 130 + num2 * 90 + rem * 50
            best = min(best, total)
        return best

    # ----------- Freebie adjusters (separate from pricing) -----------

    def adjust_B_for_E(self, amount_B, amount_E):
        """2E -> 1B free"""
        return max(0, amount_B - (amount_E // 2))

    def adjust_Q_for_R(self, amount_Q, amount_R):
        """3R -> 1Q free"""
        return max(0, amount_Q - (amount_R // 3))

    def adjust_M_for_N(self, amount_M, amount_N):
        """3N -> 1M free"""
        return max(0, amount_M - (amount_N // 3))

    # ----------- Group offer: any 3 of (S,T,X,Y,Z) for 45 -----------

    def price_group_STXYZ(self, counts):
        """
        counts: dict with keys 'S','T','X','Y','Z' -> quantities
        Strategy: replace the sum of the most expensive 3*k items by k*45.
        """
        unit = {'S': 20, 'T': 20, 'X': 17, 'Y': 20, 'Z': 21}
        prices = []
        for sku in ('S', 'T', 'X', 'Y', 'Z'):
            prices.extend([unit[sku]] * counts.get(sku, 0))
        if not prices:
            return 0
        total_base = sum(prices)
        groups = len(prices) // 3
        if groups == 0:
            return total_base
        prices.sort(reverse=True)  # pick the expensive ones for the deal
        replaced_sum = sum(prices[:3 * groups])
        return total_base - replaced_sum + groups * 45

    # ------------------------------ checkout ------------------------------

    def checkout(self, skus):
        counts = self._validate_and_count(skus)
        if counts is None:
            return -1

        amount = {sku: counts.get(sku, 0) for sku in ascii_uppercase}

        # Apply cross-item freebies by adjusting the affected counts
        eff_B = self.adjust_B_for_E(amount['B'], amount['E'])
        eff_M = self.adjust_M_for_N(amount['M'], amount['N'])
        eff_Q = self.adjust_Q_for_R(amount['Q'], amount['R'])

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
    # Singles
    print(checkout.checkout("S"), "expected 20")
    print(checkout.checkout("T"), "expected 20")
    print(checkout.checkout("X"), "expected 17")
    print(checkout.checkout("Y"), "expected 20")
    print(checkout.checkout("Z"), "expected 21")
    # Exact groups of 3
    print(checkout.checkout("STX"), "expected 45")    # 20+20+17 -> 45
    print(checkout.checkout("SZZ"), "expected 45")    # 20+21+21 -> 45
    print(checkout.checkout("SSS"), "expected 45")
    print(checkout.checkout("ZZZ"), "expected 45")
    print(checkout.checkout("XXX"), "expected 45")
    # Groups + leftovers
    print(checkout.checkout("STXYZ"), "expected 82")  # 21+20+20 -> 45, leftover 20+17=37 -> 82
    print(checkout.checkout("ZZZZ"), "expected 66")   # 3*Z -> 45 + Z -> 21 -> 66
    print(checkout.checkout("ZZZXX"), "expected 79")  # (21+21+21)->45 + 17+17 -> 79
    print(checkout.checkout("SSTT"), "expected 65")   # (20+20+20)->45 + 20 -> 65
    print(checkout.checkout("STXX"), "expected 62")   # (20+20+17)->45 + 17 -> 62
    print(checkout.checkout("XXXXXX"), "expected 90") # 2 groups of 3*X -> 2*45

    print("\nOther unchanged offers:")
    print(checkout.checkout("HHHHH"), "expected 45")         # 5H for 45
    print(checkout.checkout("HHHHHHHHHH"), "expected 80")    # 10H for 80
    print(checkout.checkout("HHHHHHHHHHH"), "expected 90")   # 10H + 1*10
    print(checkout.checkout("I"), "expected 35")
    print(checkout.checkout("J"), "expected 60")
    print(checkout.checkout("L"), "expected 90")
    print(checkout.checkout("P"*5), "expected 200")          # 5P for 200
    print(checkout.checkout("QQQ"), "expected 80")           # 3Q for 80
    print(checkout.checkout("VV"), "expected 90")            # 2V=90
    print(checkout.checkout("VVV"), "expected 130")          # 3V=130
    print(checkout.checkout("VVVV"), "expected 180")         # 2+2 or 3+1
    print(checkout.checkout("U"*4), "expected 120")          # 4U pay 3*40

    print("\nMixed baskets (with group + freebies):")
    print(checkout.checkout("ABCD"), "expected 115")
    print(checkout.checkout("ABCDE"), "expected 155")
    print(checkout.checkout("NNNM"), "expected 120")         # 3N=120, M free
    print(checkout.checkout("NNNMM"), "expected 135")        # 3N=120, M eff=1 -> 15
    print(checkout.checkout("RRRQ"), "expected 150")         # 3R=150, Q free
    print(checkout.checkout("RRRQQQ"), "expected 210")       # 3R=150, Q eff=2 -> 60
    print(checkout.checkout("EEBZ"), "expected 101")         # 2E=80 (B free) + Z=21
    print(checkout.checkout("EEFFBZZZ"), "expected 145")     # 2E=80 + FF=20 + (B free) + ZZZ=45
    print(checkout.checkout("FFFABC"), "expected 120")       # 20 + 50 + 30 + 20
    print(checkout.checkout("STXYZAB"), "expected 82 + 115 = 197")
    print(checkout.checkout("RRRQQQNNNM"), "expected 330")   # 150 + (Q eff=2 -> 60) + 120 + (M free)

    print("\nEdge cases:")
    print(checkout.checkout(""), "expected 0")


# Call it if you want to run immediately
if __name__ == "__main__":
    run_tests_r5()


