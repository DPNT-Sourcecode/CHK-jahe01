
from collections import Counter

class CheckoutSolution:


    def _validate_and_count(self, skus):

        if not isinstance(skus, str):
            return None
        if skus == "":
            return Counter()  # empty is valid -> totals 0
        allowed = {"A", "B", "C", "D", "E"}
        if any(ch not in allowed for ch in skus):
            return None
        return Counter(skus)

    # skus = unicode string
    def checkout(self, skus):
        counts = self._validate_and_count(skus)
        if counts is None:
            return -1

        amount_of_A = counts.get('A', 0)
        amount_of_B = counts.get('B', 0)
        amount_of_C = counts.get('C', 0)
        amount_of_D = counts.get('D', 0)
        amount_of_E = counts.get('E', 0)

        # A calculation
        discount_A_200 = amount_of_A // 5
        remainder_after_5 = amount_of_A % 5

        discount_A_130 = remainder_after_5 // 3
        remainder_after_3 = remainder_after_5 % 3

        total_A = discount_A_200 * 200 + discount_A_130 * 130 + remainder_after_3 * 50


        # E Calculation
        free_Bs = amount_of_E // 2
        effective_B = max(0, amount_of_B - free_Bs)
        total_E = amount_of_E * 40

        # B Calculation
        discount_B = effective_B // 2
        remainder_B = effective_B % 2
        total_B = discount_B * 45 + remainder_B * 30

        total = (amount_of_D * 15) + (amount_of_C * 20) + (total_A) + (total_B) + (total_E)

        return total





