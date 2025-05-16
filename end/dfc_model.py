import numpy as np

class DCFModel:
    def __init__(self, cash_flows, discount_rate, perpetuity_growth_rate, final_year=None):
        self.cash_flows = cash_flows
        self.discount_rate = discount_rate
        self.g = perpetuity_growth_rate
        self.final_year = final_year or len(cash_flows)

    def calculate_present_value(self):
        return sum(cf / ((1 + self.discount_rate) ** i) for i, cf in enumerate(self.cash_flows, start=1))

    def calculate_terminal_value(self):
        last_cash_flow = self.cash_flows[-1]
        terminal_value = last_cash_flow * (1 + self.g) / (self.discount_rate - self.g)
        return terminal_value / ((1 + self.discount_rate) ** self.final_year)

    def calculate_intrinsic_value(self):
        pv_cash_flows = self.calculate_present_value()
        terminal_value = self.calculate_terminal_value()
        return pv_cash_flows + terminal_value
