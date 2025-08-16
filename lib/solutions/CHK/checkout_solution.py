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

    # skus = unicode string
    def checkout(self, skus):
        counts = self._validate_and_count(skus)
        if counts is None:
            return -1

        # amounts for A..Z
        amount = {sku: counts.get(sku, 0) for sku in ascii_uppercase}

        # Compute totals for the “giver” items (E, N, R) normally
        total_E = self.price_E(amount['E'])
        total_N = self.price_N(amount['N'])
        total_R = self.price_R(amount['R'])

        # Adjust the affected items’ counts (B, M, Q) using helpers
        eff_B = self.adjust_B_for_E(amount['B'], amount['E'])
        eff_M = self.adjust_M_for_N(amount['M'], amount['N'])
        eff_Q = self.adjust_Q_for_R(amount['Q'], amount['R'])

        # Price all other items (with adjusted counts where applicable)
        total_A = self.price_A(amount['A'])
        total_B = self.price_B(eff_B)
        total_C = self.price_C(amount['C'])
        total_D = self.price_D(amount['D'])
        total_F = self.price_F(amount['F'])
        total_G = self.price_G(amount['G'])
        total_H = self.price_H(amount['H'])
        total_I = self.price_I(amount['I'])
        total_J = self.price_J(amount['J'])
        total_K = self.price_K(amount['K'])
        total_L = self.price_L(amount['L'])
        total_M = self.price_M(eff_M)
        total_O = self.price_O(amount['O'])
        total_P = self.price_P(amount['P'])
        total_Q = self.price_Q(eff_Q)
        total_S = self.price_S(amount['S'])
        total_T = self.price_T(amount['T'])
        total_U = self.price_U(amount['U'])
        total_V = self.price_V(amount['V'])
        total_W = self.price_W(amount['W'])
        total_X = self.price_X(amount['X'])
        total_Y = self.price_Y(amount['Y'])
        total_Z = self.price_Z(amount['Z'])

        return (
            total_A + total_B + total_C + total_D + total_E + total_F +
            total_G + total_H + total_I + total_J + total_K + total_L +
            total_M + total_N + total_O + total_P + total_Q + total_R +
            total_S + total_T + total_U + total_V + total_W + total_X +
            total_Y + total_Z
        )


# ----------------- quick tests (same style as before) -----------------

if __name__ == "__main__":
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

    print("\nF new item:")
    print(checkout.checkout("F"), "expected 10")
    print(checkout.checkout("FF"), "expected 20")
    print(checkout.checkout("FFF"), "expected 20")
    print(checkout.checkout("FFFF"), "expected 30")
    print(checkout.checkout("FFFFF"), "expected 40")
    print(checkout.checkout("FFFFFF"), "expected 40")

    print("\nNew items & offers (G..Z):")
    print(checkout.checkout("G"), "expected 20")
    print(checkout.checkout("HHHHH"), "expected 45")        # 5H for 45
    print(checkout.checkout("HHHHHHHHHH"), "expected 80")   # 10H for 80
    print(checkout.checkout("HHHHHHHHHHH"), "expected 90")  # 10H + 1 = 80+10
    print(checkout.checkout("HHHHHHHHHHHHH"), "expected 125")# 10H + 5H = 80+45
    print(checkout.checkout("I"), "expected 35")
    print(checkout.checkout("J"), "expected 60")
    print(checkout.checkout("KK"), "expected 150")          # 2K for 150
    print(checkout.checkout("KKK"), "expected 230")         # 150 + 80
    print(checkout.checkout("L"), "expected 90")
    print(checkout.checkout("NNNM"), "expected 120")        # 3N=120, M free
    print(checkout.checkout("NNNMM"), "expected 135")       # 120 + 1*M(15)
    print(checkout.checkout("NNNNMM"), "expected 175")      # 4N=160, 1 M free -> 1*M(15)
    print(checkout.checkout("O"), "expected 10")
    print(checkout.checkout("PPPPP"), "expected 200")       # 5P for 200
    print(checkout.checkout("PPPPPP"), "expected 250")      # 200 + 1*50
    print(checkout.checkout("QQQ"), "expected 80")          # 3Q for 80
    print(checkout.checkout("QQQQ"), "expected 110")        # 80 + 30
    print(checkout.checkout("RRRQ"), "expected 150")        # 3R=150, Q free
    print(checkout.checkout("RRRQQQ"), "expected 210")      # 3R=150, Q eff=2 -> 60
    print(checkout.checkout("S"), "expected 30")
    print(checkout.checkout("T"), "expected 20")
    print(checkout.checkout("UUUU"), "expected 120")        # 4U pay 3*40
    print(checkout.checkout("UUUUU"), "expected 160")       # 120 + 40
    print(checkout.checkout("V"), "expected 50")
    print(checkout.checkout("VV"), "expected 90")           # 2V for 90
    print(checkout.checkout("VVV"), "expected 130")         # 3V for 130
    print(checkout.checkout("VVVV"), "expected 180")        # 2+2 or 3+1
    print(checkout.checkout("VVVVV"), "expected 220")       # 3+2
    print(checkout.checkout("VVVVVV"), "expected 260")      # 3+3
    print(checkout.checkout("W"), "expected 20")
    print(checkout.checkout("X"), "expected 90")
    print(checkout.checkout("Y"), "expected 10")
    print(checkout.checkout("Z"), "expected 50")

    print("\nMixed baskets:")
    print(checkout.checkout("ABCD"), "expected 115")
    print(checkout.checkout("ABCDE"), "expected 155")
    print(checkout.checkout("AAABBBCCCDDD"), "expected 310")
    print(checkout.checkout("AAAAAAAABBBBBBBBBCCCDDD"), "expected 645")
    print(checkout.checkout("FFFABC"), "expected 120")
    print(checkout.checkout("EEFFBB"), "expected 130")
    print(checkout.checkout("RRRQQQNNNM"), "expected 150 + 80 + 120 = 350")  # Q free once; Q eff=2 -> 60; but plus N gives M free; total 150+60+120+0? (we keep simple view)

    print("\nEdge cases:")
    print(checkout.checkout(""), "expected 0")





