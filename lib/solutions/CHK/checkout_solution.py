
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
        total_F = new_amount_of_F * 10

    


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
    print(checkout.checkout("F"), "expected 10")        # single F
    print(checkout.checkout("FF"), "expected 20")       # no freebie yet
    print(checkout.checkout("FFF"), "expected 20")      # 3 for 20
    print(checkout.checkout("FFFF"), "expected 30")     # 3 for 20 + 1 = 10
    print(checkout.checkout("FFFFF"), "expected 40")    # 3 for 20 + 2 = 20
    print(checkout.checkout("FFFFFF"), "expected 40")   # 2×(3 for 20)

    print("\nMixed baskets:")
    print(checkout.checkout("ABCD"), "expected 115")
    print(checkout.checkout("ABCDE"), "expected 155")
    print(checkout.checkout("AAABBBCCCDDD"), "expected 310")
    print(checkout.checkout("AAAAAAAABBBBBBBBBCCCDDD"), "expected 645")
    print(checkout.checkout("FFFABC"), "expected 20 + 50 + 30 + 20 = 120")
    print(checkout.checkout("EEFFBB"), "expected 80 + 20 (2F no freebie) + 45 (2B offer) = 145")

    print("\nEdge cases:")
    print(checkout.checkout(""), "expected 0")





