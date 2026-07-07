class VectorAgent:
    def __init__(self):
        self.employee_id = "NX-VECTOR-02"
        self.role = "Hacim, Korelasyon ve Trend Analisti"
        self.price_history = {}
        self.max_history_len = 10

    def process_mining(self, symbol, current_price):
        # Fiyat hareketlerini ve anomalileri bulan matematiksel veri motoru
        if symbol not in self.price_history:
            self.price_history[symbol] = []
            
        self.price_history[symbol].append(current_price)
        if len(self.price_history[symbol]) > self.max_history_len:
            self.price_history[symbol].pop(0)

        history = self.price_history[symbol]
        avg_price = sum(history) / len(history) if history else current_price
        position_state = "UNDERVALUED" if current_price < avg_price else "OVERVALUED"
        
        return {
            "employee_id": self.employee_id,
            "avg_price": avg_price,
            "position_state": position_state,
            "is_anomaly": abs(current_price - avg_price) > (avg_price * 0.01)
        }