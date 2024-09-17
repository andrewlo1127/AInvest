from backtesting import Backtest, Strategy
class strategy(Strategy):
    oversold_level = 30
    overbought_level = 70

    def init(self):
        # 初始化 RSI 指標
        self.rsi = self.I(lambda: self.data['RSI'], name='RSI')

    def next(self):
        # 當 RSI 低於超賣水平且沒有持倉時，買入
        if self.rsi[-1] < self.oversold_level and not self.position:
            self.buy()
        # 當 RSI 高於超買水平且持有多頭倉位時，平倉
        elif self.rsi[-1] > self.overbought_level:
            if self.position and self.position.is_long:
                self.position.close()

# 計算 RSI 指標
def calculate(df, period=14):
    df = df.copy()
    # 計算價格變動的差異
    delta = df['Close'].diff()
    # 計算上漲和下跌的平均值
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    # 計算 RSI
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def name():
    return "RSI"

if __name__ == "__main__":
    calculate()