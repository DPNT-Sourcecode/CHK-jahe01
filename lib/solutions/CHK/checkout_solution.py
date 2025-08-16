
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

        # F Calculation
        discount_F = amount_of_F // 3
        new_amount_of_F = amount_of_F - discount_F
        total_F = new_amount_of_F * 10

        total = (amount_of_D * 15) + (amount_of_C * 20) + (total_A) + (total_B) + (total_E) + (total_F)

        return total
    


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








