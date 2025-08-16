
from collections import Counter

class CheckoutSolution:

    # skus = unicode string
    def checkout(self, skus):
        individual_items = list(skus)
        item_counts = Counter(skus)

        amount_of_A = item_counts.get('A', 0)
        amount_of_B = item_counts.get('B', 0)
        amount_of_C = item_counts.get('C', 0)
        amount_of_D = item_counts.get('D', 0)

        discount_A = (amount_of_A // 3)
        discount_B = (amount_of_B // 2)

        individual_A = amount_of_A - (discount_A * 3)
        individual_B = amount_of_B - (discount_B * 2)

        total = (amount_of_D * 15) + (amount_of_C * 20) + (discount_A * 130) + (discount_B * 45) + (individual_A * 50) + (individual_B * 30)

        return total

if __name__ == "__main__":
    checkout = CheckoutSolution()
    print(checkout.checkout("ABCD"))  # Example usage
    print(checkout.checkout("AAABBBCCCDDD"))  # Another example
    print(checkout.checkout("AAAAAAAABBBBBBBBBCCCDDD"))  # Another example

