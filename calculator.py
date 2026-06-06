class PortfolioCalculator:
    def __init__(self, transactions):
        self.transactions = transactions
    
    def calculate_profit_loss(self, transaction):
        transaction_id, stock_name, quantity, buy_price, sell_price, status, date_added, date_sold = transaction
        
        if status == 'open' or sell_price is None:
            return None
        
        total_buy = quantity * buy_price
        total_sell = quantity * sell_price
        profit_loss = total_sell - total_buy
        
        return profit_loss
    
    def calculate_profit_loss_percentage(self, transaction):
        transaction_id, stock_name, quantity, buy_price, sell_price, status, date_added, date_sold = transaction
        
        if status == 'open' or sell_price is None:
            return None
        
        total_buy = quantity * buy_price
        total_sell = quantity * sell_price
        percentage = ((total_sell - total_buy) / total_buy) * 100
        
        return percentage
    
    def get_total_invested(self):
        total = 0
        for transaction in self.transactions:
            transaction_id, stock_name, quantity, buy_price, sell_price, status, date_added, date_sold = transaction
            total += quantity * buy_price
        return total
    
    def get_total_current_value(self):
        total = 0
        for transaction in self.transactions:
            transaction_id, stock_name, quantity, buy_price, sell_price, status, date_added, date_sold = transaction
            
            if status == 'closed' and sell_price:
                total += quantity * sell_price
            elif status == 'open':
                total += quantity * buy_price
        
        return total
    
    def get_total_profit_loss(self):
        total_profit_loss = 0
        for transaction in self.transactions:
            profit_loss = self.calculate_profit_loss(transaction)
            if profit_loss is not None:
                total_profit_loss += profit_loss
        return total_profit_loss
    
    def get_total_profit_loss_percentage(self):
        total_invested = self.get_total_invested()
        if total_invested == 0:
            return 0
        
        total_profit_loss = self.get_total_profit_loss()
        percentage = (total_profit_loss / total_invested) * 100
        
        return percentage
