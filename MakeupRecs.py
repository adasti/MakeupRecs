from pip._vendor import requests
import pandas as pd

class MakeupRecs:
    def __init__(self):
        self.url = 'https://makeup-api.herokuapp.com/api/v1/products.json'
        self.response = requests.get(self.url)
        self.cosmetics_data = self.response.json()
        self.cosmetics_df = pd.DataFrame(self.cosmetics_data)
        self.brands = ["almay", "alva", "anna sui", "annabelle", "benefit", "boosh", 
          "burt's bees", "butter london", "c'est moi", "cargo cosmetics",
           "china glaze", "clinique", "coastal classic creation", "colourpop",
             "covergirl", "dalish", "deciem", "dior", "dr. hauschka", "e.l.f."
             , "essie", "fenty", "glossier", "green people", "iman", "l'oreal"
             , "lotus cosmetics usa", "maia's mineral galaxy", "marcelle"
             , "marienatie", "maybelline", "milani", "mineral fusion", "misa"
             , "mistura", "moov", "nudus", "nyx", "orly", "pacifica"
             , "penny lane organics", "physicians formula", "piggy paint"
             , "pure anada", "rejuva minerals", "revlon"
             , "sally b's skin yummies", "salon perfect", "sante"
             , "sinful colours", "smashbox", "stila", "suncoat", "w3llpeople"
             , "wet n wild", "zorah", "zorah biocosmetiques"]
        
        self.products = ["blush", "bronzer", "eyebrow", "eyeliner", "eyeshadow", "foundation"
            "lip_liner", "lipstick", "mascara", "nail_polish"]
        
        self.questions = [" 1: I need some color on my cheeks and/or I want a flushed look",
             "2: I want some warmth and definition around my face",
             "3: I want to fill in my eyebrows and give them some volume",
             "4: I want to define my eye shape",
             "5: I want some color and depth on my eyelids",
             "6: I want a more even complexion and want some coveraage",
             "7: I want something to outline and define my lips",
             "8: I want some color on my lips",
             "9: I want my eyelashes to pop and have more volume/length",
             "10: I want to have some color and designs on my nails"]
        
        self.product_dict = {1 : "blush",
                2 : "bronzer",
                3 : "eyebrow",
                4 : "eyeliner",
                5 : "eyeshadow",
                6 : "foundation",
                7 : "lip_liner",
                8 : "lipstick",
                9 : "mascara",
                10 : "nail_polish"}

    def get_product(self):
        for question in self.questions:
            print(question)
        looking_for = input("Please look through through the following options and enter a number that best defines what you're looking for: ")
        if looking_for in self.product_dict:
            desired_product = self.product_dict[looking_for]
            return desired_product
        else:
            print("Please enter a valid number")
            return None

    def get_brand(self):
        for brand in self.brands:
            print(brand)
        preference = input("Please look through the list of brands and enter a brand you prefer: ")
        if preference.lower() in self.brands:
            prefered_brand = preference.lower()
        else:
            print("Please enter a valid brand.")
            return None
        
    def convert_prices(self):
        prices = []
        for product in self.cosmetics_data:
            if 'price' in product and product['price'] is not None:
                try:
                    price = float(product['price'])
                    prices.append(price)
                except (ValueError, TypeError):
                    pass
        return prices

    def get_max_price(self):
        product_prices = self.convert_prices()
        max_price = input("Please enter the maximum price you are willing to pay:")
        try:
            max_price = float(max_price)
            return max_price, product_prices
        except ValueError:
            print("Please enter a valid price you are willing to pay.")
            return None, product_prices

    def find_products(self):
        desired_product = self.get_product()
        preferred_brand = self.get_brand()
        max_price, all_prices = self.get_max_price()

        recommended_products = []
        for product in self.cosmetics_data:
            if (product['product_type'] == desired_product and
                product['brand'].lower() == preferred_brand and
                float(product['price']) <= max_price):
                
                recommended_products.append((product['brand'], product['name'], float(product['price'])))

        if recommended_products:
            sorted_recommended = sorted(recommended_products, key=lambda x: x[2])  # Sort by price
            results_df = pd.DataFrame(sorted_recommended, columns=['Brand', 'Name', 'Price'])
            return results_df
        else:
            print("No matching products found.")
            return None

# Usage:
finder = MakeupRecs()
recommended_df = finder.find_products()

if recommended_df is not None:
    print(recommended_df)