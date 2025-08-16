
from collections import Counter

class CheckoutSolution:


    def _validate_and_count(self, skus):

        if not isinstance(skus, str):
            return None
        if skus == "":
            return Counter()  # empty is valid -> totals 0
        allowed = {"A", "B", "C", "D", "E", "F"}
        if any(ch not in allowed for ch in skus):
            return None
        return Counter(skus)
    
    # A calculation - always pick cheapest combination
    def price_A(self, amount):
        best = amount * 50
        for num5 in range(amount // 5 + 1):
            for num3 in range((amount - num5 * 5) // 3 + 1):
                leftover = amount - num5 * 5 - num3 * 3
                total = num5 * 200 + num3 * 130 + leftover * 50
                best = min(best, total)
        return best
    
    def price_B(self, amount):
        # B Calculation
        discount_B = amount // 2
        remainder_B = amount % 2
        return discount_B * 45 + remainder_B * 30

    def price_C(self, amount):
        # C Calculation
        return amount * 20

    def price_D(self, amount):
        # D Calculation
        return amount * 15
    
    def price_E(self, amount_E, amount_B):
        # E Calculation
        free_Bs = amount_E // 2
        effective_B = max(0, amount_B - free_Bs)
        total_E = amount_E * 40
        return total_E, effective_B

    
    def price_F(self, amount):
        discount_F = amount // 3
        new_amount_of_F = amount - discount_F
        return new_amount_of_F * 10

    

    


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
        amount_of_F = counts.get('F', 0)


        # A Calculation
        total_A = self.price_A(amount_of_A)

        # E Calculation
        total_E, effective_B = self.price_E(amount_of_E, amount_of_B)

        # B Calculation
        total_B = self.price_B(effective_B)

        # C Calculation
        total_C = self.price_C(amount_of_C)

        # D Calculation
        total_D = self.price_D(amount_of_D)

        # F Calculation
        total_F = self.price_F(amount_of_F)


        return (total_A + total_B + total_C + total_D + total_E + total_F)


    






