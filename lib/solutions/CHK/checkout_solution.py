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
        up = UNIT_PRICE['A']
        best = amount * up
        for num5 in range(amount // 5 + 1):
            rem_after_5 = amount - 5 * num5
            for num3 in range(rem_after_5 // 3 + 1):
                rem = rem_after_5 - 3 * num3
                total = num5 * BUNDLE_DEALS["A"]["PRICE_FOR_5"] \
                        + num3 * BUNDLE_DEALS["A"]["PRICE_FOR_3"] \
                        + rem * up
                best = min(best, total)
        return best

    def price_B(self, amount):
        up = UNIT_PRICE['B']
        return (amount // 2) * BUNDLE_DEALS["B"]["PRICE_FOR_2"] \
               + (amount % 2) * up

    def price_C(self, amount): return amount * UNIT_PRICE['C']
    def price_D(self, amount): return amount * UNIT_PRICE['D']
    def price_E(self, amount): return amount * UNIT_PRICE['E']

    def price_F(self, amount):
        up = UNIT_PRICE['F']
        groups = amount // 3
        rem = amount % 3
        return groups * BUNDLE_DEALS["F"]["PRICE_FOR_3"] + rem * up

    def price_G(self, amount): return amount * UNIT_PRICE['G']

    def price_H(self, amount):
        up = UNIT_PRICE['H']
        best = amount * up
        for num10 in range(amount // 10 + 1):
            rem10 = amount - 10 * num10
            for num5 in range(rem10 // 5 + 1):
                rem = rem10 - 5 * num5
                total = num10 * BUNDLE_DEALS["H"]["PRICE_FOR_10"] \
                        + num5 * BUNDLE_DEALS["H"]["PRICE_FOR_5"] \
                        + rem * up
                best = min(best, total)
        return best

    def price_I(self, amount): return amount * UNIT_PRICE['I']
    def price_J(self, amount): return amount * UNIT_PRICE['J']

    def price_K(self, amount):
        up = UNIT_PRICE['K']
        return (amount // 2) * BUNDLE_DEALS["K"]["PRICE_FOR_2"] \
               + (amount % 2) * up

    def price_L(self, amount): return amount * UNIT_PRICE['L']
    def price_M(self, amount): return amount * UNIT_PRICE['M']
    def price_N(self, amount): return amount * UNIT_PRICE['N']
    def price_O(self, amount): return amount * UNIT_PRICE['O']

    def price_P(self, amount):
        up = UNIT_PRICE['P']
        return (amount // 5) * BUNDLE_DEALS["P"]["PRICE_FOR_5"] \
               + (amount % 5) * up

    def price_Q(self, amount):
        up = UNIT_PRICE['Q']
        return (amount // 3) * BUNDLE_DEALS["Q"]["PRICE_FOR_3"] \
               + (amount % 3) * up

    def price_R(self, amount): return amount * UNIT_PRICE['R']

    def price_S(self, amount): return amount * UNIT_PRICE['S']
    def price_T(self, amount): return amount * UNIT_PRICE['T']
    def price_W(self, amount): return amount * UNIT_PRICE['W']
    def price_X(self, amount): return amount * UNIT_PRICE['X']
    def price_Y(self, amount): return amount * UNIT_PRICE['Y']
    def price_Z(self, amount): return amount * UNIT_PRICE['Z']

    def price_U(self, amount):
        up = UNIT_PRICE['U']
        groups = amount // 4
        rem = amount % 4
        return groups * BUNDLE_DEALS["U"]["PRICE_FOR_4"] + rem * up

    def price_V(self, amount):
        up = UNIT_PRICE['V']
        best = amount * up
        for num3 in range(amount // 3 + 1):
            rem3 = amount - 3 * num3
            num2 = rem3 // 2
            rem = rem3 % 2
            total = num3 * BUNDLE_DEALS["V"]["PRICE_FOR_3"] \
                    + num2 * BUNDLE_DEALS["V"]["PRICE_FOR_2"] \
                    + rem * up
            best = min(best, total)
        return best

    # ----------- Freebie adjusters -----------

    def calculate_amount_of_B(self, amount_B, amount_E):
        return max(0, amount_B - (amount_E // 2))

    def calculate_amount_of_Q(self, amount_Q, amount_R):
        return max(0, amount_Q - (amount_R // 3))

    def calculate_amount_of_M(self, amount_M, amount_N):
        return max(0, amount_M - (amount_N // 3))

    # ----------- Group offer STXYZ -----------

    def price_group_STXYZ(self, counts):
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

    # ---------------- checkout ----------------

    def checkout(self, skus):
        counts = self._validate_and_count(skus)
        if counts is None:
            return -1

        amount = {sku: counts.get(sku, 0) for sku in ascii_uppercase}
        freebie_adjusted_B = self.calculate_amount_of_B(amount['B'], amount['E'])
        freebie_adjusted_M = self.calculate_amount_of_M(amount['M'], amount['N'])
        freebie_adjusted_Q = self.calculate_amount_of_Q(amount['Q'], amount['R'])

        override_counts = {'B': freebie_adjusted_B,
                           'M': freebie_adjusted_M,
                           'Q': freebie_adjusted_Q}

        group_total = self.price_group_STXYZ({k: amount[k] for k in ('S', 'T', 'X', 'Y', 'Z')})
        for k in ('S', 'T', 'X', 'Y', 'Z'):
            override_counts[k] = 0

        items_total = sum(
            getattr(self, f"price_{sku}")(override_counts.get(sku, amount[sku]))
            for sku in ascii_uppercase
            if getattr(self, f"price_{sku}", None) and override_counts.get(sku, amount[sku]) > 0
        )

        return group_total + items_total


if __name__ == "__main__":
    # Test cases for each individual price function

