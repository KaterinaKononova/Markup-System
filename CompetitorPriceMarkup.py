class CompetitorsPriceMarkup:

    def __init__(self, cost_price, competitor_price):
        self.cost_price = cost_price
        self.comp_price = competitor_price

    def get_cost(self):
        return self.cost_price

    def get_competitor_price(self):
        return self.comp_price

    def get_competitor_price_markup(self):
        rec_markup = (self.comp_price - self.cost_price) / self.cost_price * 100
        return rec_markup


m_array = [1, 2, 3, 4, 5, 6]
p_array = [2, 2, 2, 2, 2, 3]


print(f_array)