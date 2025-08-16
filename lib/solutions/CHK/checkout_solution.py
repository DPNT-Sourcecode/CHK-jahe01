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

        # renamed: calculate_amount_of_X -> calculate_new_amount_of_X
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
    print(checkout.checkout("AABCD"))  # Example usage
    print(checkout.checkout("EEB"))    # Example usage
    print(checkout.checkout("STXYZ"))  # Example usage
    print(checkout.checkout("INVALID"))  # Should return -1
    print(checkout.checkout(""))        # Should return 0
    print(checkout.checkout("A"))       # Should return 50

