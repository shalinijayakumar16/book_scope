def get_rating(rating_str):
    rating_map = {
        "One": 1, "Two": 2, "Three": 3,
        "Four": 4, "Five": 5
    }
    return rating_map.get(rating_str, 0)


def clean_price(price_str):
    return float(price_str.replace("£", ""))