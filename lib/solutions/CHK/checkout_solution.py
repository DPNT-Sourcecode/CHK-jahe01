
from collections import Counter

class CheckoutSolution:


    def _validate_and_count(self, skus):

        if not isinstance(skus, str):
            return None
        if skus == "":
            return Counter()  # empty is valid -> totals 0
        allowed = {"A", "B", "C", "D"}
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

        discount_A = (amount_of_A // 3)
        discount_B = (amount_of_B // 2)

        individual_A = amount_of_A - (discount_A * 3)
        individual_B = amount_of_B - (discount_B * 2)

        total = (amount_of_D * 15) + (amount_of_C * 20) + (discount_A * 130) + (discount_B * 45) + (individual_A * 50) + (individual_B * 30)

        return total






