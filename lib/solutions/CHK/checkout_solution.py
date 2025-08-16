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
    "K": {"PRICE_FOR_2": 120},
    "P": {"PRICE_FOR_5": 200},
    "Q": {"PRICE_FOR_3": 80},
    "V": {"PRICE_FOR_3": 130, "PRICE_FOR_2": 90},
    "F": {"PRICE_FOR_3": 2 * UNIT_PRICE["F"]},
    "U": {"PRICE_FOR_4": 3 * UNIT_PRICE["U"]},
}


class CheckoutSolution:

    def _validate_and_count(self, skus):
        if not isinstance(skus, str):
            return None
        if skus == "":
            return Counter()
        if any(ch not in ascii_uppercase for ch in skus):
            return None
        return Counter(skus)

    # ---------------- Prices ----------------

    def price_A(self, amount):
        unit_price = UNIT_PRICE['A']
        lowest_total_price = amount * unit_price  # baseline with no discounts applied

        # Explore all possible mixes of 5-pack and 3-pack bundles
        for num_five_pack_bundles in range(amount // 5 + 1):
            remaining_after_fives = amount - 5 * num_five_pack_bundles

            for num_three_pack_bundles in range(remaining_after_fives // 3 + 1):
                remaining_singles = remaining_after_fives - 3 * num_three_pack_bundles

                total_for_this_combo = (
                    num_five_pack_bundles * BUNDLE_DEALS["A"]["PRICE_FOR_5"]
                    + num_three_pack_bundles * BUNDLE_DEALS["A"]["PRICE_FOR_3"]
                    + remaining_singles * unit_price
                )

                lowest_total_price = min(lowest_total_price, total_for_this_combo)

        return lowest_total_price

    def price_B(self, amount):
        unit_price = UNIT_PRICE['B']
        return (amount // 2) * BUNDLE_DEALS["B"]["PRICE_FOR_2"] \
               + (amount % 2) * unit_price

    def price_C(self, amount): return amount * UNIT_PRICE['C']
    def price_D(self, amount): return amount * UNIT_PRICE['D']
    def price_E(self, amount): return amount * UNIT_PRICE['E']

    def price_F(self, amount):
        unit_price = UNIT_PRICE['F']
        amount_of_discount_sets = amount // 3        # every 3 F’s form one “buy 2 get 1 free” set
        remaining_singles = amount % 3               # leftover F’s not part of a set

        total_price = (
            amount_of_discount_sets * BUNDLE_DEALS["F"]["PRICE_FOR_3"]
            + remaining_singles * unit_price
        )
        return total_price


    def price_G(self, amount): return amount * UNIT_PRICE['G']

    def price_H(self, amount):
        unit_price = UNIT_PRICE['H']
        lowest_total_price = amount * unit_price  # baseline with no bundles

        # Explore all possible combinations of 10-pack and 5-pack bundles
        for num_ten_pack_bundles in range(amount // 10 + 1):
            remaining_after_tens = amount - 10 * num_ten_pack_bundles

            for num_five_pack_bundles in range(remaining_after_tens // 5 + 1):
                remaining_singles = remaining_after_tens - 5 * num_five_pack_bundles

                total_for_this_combo = (
                    num_ten_pack_bundles * BUNDLE_DEALS["H"]["PRICE_FOR_10"]
                    + num_five_pack_bundles * BUNDLE_DEALS["H"]["PRICE_FOR_5"]
                    + remaining_singles * unit_price
                )

                lowest_total_price = min(lowest_total_price, total_for_this_combo)

        return lowest_total_price


    def price_I(self, amount): return amount * UNIT_PRICE['I']
    def price_J(self, amount): return amount * UNIT_PRICE['J']

    def price_K(self, amount):
        unit_price = UNIT_PRICE['K']
        return (amount // 2) * BUNDLE_DEALS["K"]["PRICE_FOR_2"] \
               + (amount % 2) * unit_price

    def price_L(self, amount): return amount * UNIT_PRICE['L']
    def price_M(self, amount): return amount * UNIT_PRICE['M']
    def price_N(self, amount): return amount * UNIT_PRICE['N']
    def price_O(self, amount): return amount * UNIT_PRICE['O']

    def price_P(self, amount):
        unit_price = UNIT_PRICE['P']
        return (amount // 5) * BUNDLE_DEALS["P"]["PRICE_FOR_5"] \
               + (amount % 5) * unit_price

    def price_Q(self, amount):
        unit_price = UNIT_PRICE['Q']
        return (amount // 3) * BUNDLE_DEALS["Q"]["PRICE_FOR_3"] \
               + (amount % 3) * unit_price

    def price_R(self, amount): return amount * UNIT_PRICE['R']

    def price_S(self, amount): return amount * UNIT_PRICE['S']
    def price_T(self, amount): return amount * UNIT_PRICE['T']
    def price_W(self, amount): return amount * UNIT_PRICE['W']
    def price_X(self, amount): return amount * UNIT_PRICE['X']
    def price_Y(self, amount): return amount * UNIT_PRICE['Y']
    def price_Z(self, amount): return amount * UNIT_PRICE['Z']

    def price_U(self, amount):
        unit_price = UNIT_PRICE['U']
        amount_of_discount_sets = amount // 4        # every 4 U's form one discount set (3 paid, 1 free)
        remaining_singles = amount % 4               # leftovers not covered by a discount set

        total_price = (
            amount_of_discount_sets * BUNDLE_DEALS["U"]["PRICE_FOR_4"]
            + remaining_singles * unit_price
        )
        return total_price


    def price_V(self, amount):
        unit_price = UNIT_PRICE['V']
        lowest_total_price = amount * unit_price  # total_without_discounts baseline

        # Explore all possible combinations of bundle usage:
        # try every feasible number of 3-pack bundles, then fill with 2-packs, then singles.
        for num_three_pack_bundles in range(amount // 3 + 1):
            remaining_after_three_packs = amount - 3 * num_three_pack_bundles
            num_two_pack_bundles = remaining_after_three_packs // 2
            remaining_singles = remaining_after_three_packs % 2

            total_for_this_combo = (
                num_three_pack_bundles * BUNDLE_DEALS["V"]["PRICE_FOR_3"]
                + num_two_pack_bundles * BUNDLE_DEALS["V"]["PRICE_FOR_2"]
                + remaining_singles * unit_price
            )

            lowest_total_price = min(lowest_total_price, total_for_this_combo)

        return lowest_total_price


    # ----------- Freebie adjusters -----------

    def calculate_new_amount_of_B(self, amount_B, amount_E):
        return max(0, amount_B - (amount_E // 2))

    def calculate_new_amount_of_Q(self, amount_Q, amount_R):
        return max(0, amount_Q - (amount_R // 3))

    def calculate_new_amount_of_M(self, amount_M, amount_N):
        return max(0, amount_M - (amount_N // 3))

    # ----------- Grounit_price offer STXYZ -----------

    def group_price_calculator_STXYZ(self, counts):
        valid_items = ('S', 'T', 'X', 'Y', 'Z')
        prices = []
        for sku in valid_items:
            prices.extend([UNIT_PRICE[sku]] * counts.get(sku, 0))
        if not prices:
            return 0

        total_without_discounts = sum(prices)
        amount_of_discount_sets = len(prices) // 3
        if amount_of_discount_sets == 0:
            return total_without_discounts

        prices.sort(reverse=True)
        sum_of_most_expensive_items = sum(prices[:3 * amount_of_discount_sets])
        return total_without_discounts - sum_of_most_expensive_items + amount_of_discount_sets * 45


    # ---------------- checkout ----------------

    def checkout(self, skus):
        counts = self._validate_and_count(skus)
        if counts is None:
            return -1

        amount = {sku: counts.get(sku, 0) for sku in ascii_uppercase}

        
        freebie_adjusted_B = self.calculate_new_amount_of_B(amount['B'], amount['E'])
        freebie_adjusted_M = self.calculate_new_amount_of_M(amount['M'], amount['N'])
        freebie_adjusted_Q = self.calculate_new_amount_of_Q(amount['Q'], amount['R'])

        override_counts = {
            'B': freebie_adjusted_B,
            'M': freebie_adjusted_M,
            'Q': freebie_adjusted_Q,
        }

        # Calculate group pricing for STXYZ
        group_pricing_totals = self.group_price_calculator_STXYZ({k: amount[k] for k in ('S', 'T', 'X', 'Y', 'Z')})
        
        # Setting them to 0 to avoid double counting
        for k in ('S', 'T', 'X', 'Y', 'Z'):
            override_counts[k] = 0

        items_total = sum(
            getattr(self, f"price_{sku}")(override_counts.get(sku, amount[sku]))
            for sku in ascii_uppercase
            if getattr(self, f"price_{sku}", None) and override_counts.get(sku, amount[sku]) > 0
        )

        return group_pricing_totals + items_total


if __name__ == "__main__":
    checkout = CheckoutSolution()

    print("Smoke tests:")
    print(checkout.checkout("AABCD"), "expected 165")   # 2A(100)+B(30)+C(20)+D(15)
    print(checkout.checkout("EEB"), "expected 80")      # 2E=80, B free
    print(checkout.checkout("STXYZ"), "expected 82")    # group 45 + leftovers 37
    print(checkout.checkout(""), "expected 0")          # empty = 0

    print("\nInvalid inputs:")
    print(checkout.checkout("a"), "expected -1")
    print(checkout.checkout("-"), "expected -1")
    print(checkout.checkout("ABCa"), "expected -1")
    print(checkout.checkout(123), "expected -1")
    print(checkout.checkout(None), "expected -1")
    print(checkout.checkout("A*B"), "expected -1")

    print("\nA multi-pricing (3A=130, 5A=200):")
    print(checkout.checkout("A"), "expected 50")
    print(checkout.checkout("AA"), "expected 100")
    print(checkout.checkout("AAA"), "expected 130")
    print(checkout.checkout("AAAA"), "expected 180")     # 130 + 50
    print(checkout.checkout("AAAAA"), "expected 200")
    print(checkout.checkout("AAAAAA"), "expected 250")   # 200 + 50
    print(checkout.checkout("AAAAAAAAA"), "expected 380")# 5A(200)+3A(130)+1A(50)

    print("\nB + E freebie (2E -> 1B free) and B deal (2B=45):")
    print(checkout.checkout("B"), "expected 30")
    print(checkout.checkout("BB"), "expected 45")
    print(checkout.checkout("BBB"), "expected 75")
    print(checkout.checkout("E"), "expected 40")
    print(checkout.checkout("EB"), "expected 70")         # no free (only 1E)
    print(checkout.checkout("EEB"), "expected 80")        # B free
    print(checkout.checkout("EEBB"), "expected 110")      # B eff=1 -> 30
    print(checkout.checkout("EEBBB"), "expected 125")     # B eff=2 -> 45; 80+45
    print(checkout.checkout("EEEEBBB"), "expected 190")   # 4E=160, free 2B -> 1B=30

    print("\nF self-freebie (buy 2 get 1 free -> 3F=20):")
    print(checkout.checkout("F"), "expected 10")
    print(checkout.checkout("FF"), "expected 20")
    print(checkout.checkout("FFF"), "expected 20")
    print(checkout.checkout("FFFF"), "expected 30")
    print(checkout.checkout("FFFFFF"), "expected 40")

    print("\nH multi-pricing (5H=45, 10H=80):")
    print(checkout.checkout("H"*5), "expected 45")
    print(checkout.checkout("H"*10), "expected 80")
    print(checkout.checkout("H"*11), "expected 90")       # 80 + 10
    print(checkout.checkout("H"*15), "expected 125")      # 80 + 45

    print("\nUpdated K pricing (K=70, 2K=120):")
    print(checkout.checkout("K"), "expected 70")
    print(checkout.checkout("KK"), "expected 120")
    print(checkout.checkout("KKK"), "expected 190")       # 120 + 70

    print("\nP, Q, V offers:")
    print(checkout.checkout("P"*5), "expected 200")       # 5P=200
    print(checkout.checkout("QQQ"), "expected 80")        # 3Q=80
    print(checkout.checkout("QQQQ"), "expected 110")      # 80 + 30
    print(checkout.checkout("VV"), "expected 90")         # 2V=90
    print(checkout.checkout("VVV"), "expected 130")       # 3V=130
    print(checkout.checkout("VVVV"), "expected 180")      # 2+2 or 3+1
    print(checkout.checkout("VVVVV"), "expected 220")     # 3+2

    print("\nU self-freebie (3U get 1 free -> each 4 costs 3*U):")
    print(checkout.checkout("U"*4), "expected 120")
    print(checkout.checkout("U"*5), "expected 160")

    print("\nGroup offer: any 3 of (S,T,X,Y,Z) for 45 (S=20, T=20, X=17, Y=20, Z=21):")
    # Singles
    print(checkout.checkout("S"), "expected 20")
    print(checkout.checkout("T"), "expected 20")
    print(checkout.checkout("X"), "expected 17")
    print(checkout.checkout("Y"), "expected 20")
    print(checkout.checkout("Z"), "expected 21")
    # Exact groups of 3
    print(checkout.checkout("STX"), "expected 45")        # 20+20+17 -> 45
    print(checkout.checkout("SZZ"), "expected 45")        # 20+21+21 -> 45
    print(checkout.checkout("SSS"), "expected 45")
    print(checkout.checkout("ZZZ"), "expected 45")
    print(checkout.checkout("XXX"), "expected 45")
    # Groups + leftovers
    print(checkout.checkout("STXYZ"), "expected 82")      # 45 + (20+17)
    print(checkout.checkout("ZZZZ"), "expected 66")       # 45 + 21
    print(checkout.checkout("ZZZXX"), "expected 79")      # 45 + 34
    print(checkout.checkout("SSTT"), "expected 65")       # 45 + 20
    print(checkout.checkout("STXX"), "expected 62")       # 45 + 17
    print(checkout.checkout("SSSZ"), "expected 65")       # 45 + 20
    print(checkout.checkout("ZX"), "expected 38")         # no group
    print(checkout.checkout("STXYZST"), "expected 107")   # 2 groups (top 6) + leftover X

    print("\nOther simple items (no special offers):")
    print(checkout.checkout("C"), "expected 20")
    print(checkout.checkout("D"), "expected 15")
    print(checkout.checkout("G"), "expected 20")
    print(checkout.checkout("I"), "expected 35")
    print(checkout.checkout("J"), "expected 60")
    print(checkout.checkout("L"), "expected 90")
    print(checkout.checkout("O"), "expected 10")
    print(checkout.checkout("R"), "expected 50")
    print(checkout.checkout("W"), "expected 20")

    print("\nR→Q and N→M freebies:")
    print(checkout.checkout("RRRQ"), "expected 150")      # Q free
    print(checkout.checkout("RRRQQQ"), "expected 210")    # Q eff=2 -> 60
    print(checkout.checkout("NNNM"), "expected 120")      # M free
    print(checkout.checkout("NNNMM"), "expected 135")     # M eff=1 -> 15
    print(checkout.checkout("NNNNMM"), "expected 175")    # 160 + 15

    print("\nMixed baskets (overlaps/group/freebies):")
    print(checkout.checkout("ABCD"), "expected 115")
    print(checkout.checkout("ABCDE"), "expected 155")
    print(checkout.checkout("EEBZ"), "expected 101")      # 80 + Z(21); B free
    print(checkout.checkout("EEFFBZZZ"), "expected 145")  # 80 + 20 + 0 + 45
    print(checkout.checkout("FFFABC"), "expected 120")    # 20 + 50 + 30 + 20
    print(checkout.checkout("STXYZAB"), "expected 162")   # group 82 + A(50) + B(30)
    print(checkout.checkout("RRRQQQNNNM"), "expected 330")# 150 + 60 + 120 + 0



