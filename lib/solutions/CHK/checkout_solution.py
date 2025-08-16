from collections import Counter
from string import ascii_uppercase

class CheckoutSolution:

    def _validate_and_count(self, skus):
        if not isinstance(skus, str):
            return None
        if skus == "":
            return Counter()  # empty is valid -> totals 0
        # Round 4: A–Z are valid SKUs
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

    def price_B(self, amount):                   
        return (amount // 2) * 45 + (amount % 2) * 30

    def price_C(self, amount): return amount * 20
    def price_D(self, amount): return amount * 15
    def price_E(self, amount): return amount * 40          
    def price_F(self, amount):                              
        groups = amount // 3
        rem = amount % 3
        return groups * 20 + rem * 10

    def price_G(self, amount): return amount * 20

    def price_H(self, amount):                               
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
    def price_K(self, amount): return (amount // 2) * 150 + (amount % 2) * 80  # 2K=150
    def price_L(self, amount): return amount * 90
    def price_M(self, amount): return amount * 15
    def price_N(self, amount): return amount * 40           # <-- now N only prices N
    def price_O(self, amount): return amount * 10
    def price_P(self, amount): return (amount // 5) * 200 + (amount % 5) * 50  # 5P=200
    def price_Q(self, amount): return (amount // 3) * 80 + (amount % 3) * 30   # 3Q=80
    def price_R(self, amount): return amount * 50           # <-- now R only prices R
    def price_S(self, amount): return amount * 30
    def price_T(self, amount): return amount * 20
    def price_U(self, amount):                               # 3U get 1 U free -> per 4 pay 3
        groups = amount // 4
        rem = amount % 4
        return groups * (3 * 40) + rem * 40
    def price_V(self, amount):                               # 2V=90, 3V=130 (choose best)
        best = amount * 50
        for num3 in range(amount // 3 + 1):
            rem3 = amount - 3 * num3
            num2 = rem3 // 2
            rem = rem3 % 2
            total = num3 * 130 + num2 * 90 + rem * 50
            best = min(best, total)
        return best
    def price_W(self, amount): return amount * 20
    def price_X(self, amount): return amount * 90
    def price_Y(self, amount): return amount * 10
    def price_Z(self, amount): return amount * 50

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

    # ------------------------------ checkout ------------------------------

    def checkout(self, skus):
        counts = self._validate_and_count(skus)
        if counts is None:
            return -1

        amount = {sku: counts.get(sku, 0) for sku in ascii_uppercase}
        eff_B = self.adjust_B_for_E(amount['B'], amount['E'])
        eff_M = self.adjust_M_for_N(amount['M'], amount['N'])
        eff_Q = self.adjust_Q_for_R(amount['Q'], amount['R'])
        override_counts = {'B': eff_B, 'M': eff_M, 'Q': eff_Q}

        return sum(
            getattr(self, f"price_{sku}")(override_counts.get(sku, amount[sku]))
            for sku in ascii_uppercase
            if getattr(self, f"price_{sku}", None) and override_counts.get(sku, amount[sku]) > 0
        )





