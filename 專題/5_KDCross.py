from backtesting import Backtest, Strategy
from backtesting.lib import crossover
# 定義策略
class strategy(Strategy):
    lower_bound = 20
    upper_bound = 80

    def init(self):
        self.k = self.I(lambda: self.data['K'], name='K')
        self.d = self.I(lambda: self.data['D'], name='D')

    def next(self):
        if crossover(self.k, self.d) and self.k[-1] < self.lower_bound and self.d[-1] < self.lower_bound and not self.position:
            self.buy()
        elif crossover(self.d, self.k) and self.k[-1] > self.upper_bound and self.d[-1] > self.upper_bound:
            if self.position and self.position.is_long:
                self.position.close()

# 計算 KD 指標
def calculate(df, period=9, signal_period=3):
    df = df.copy()
    high_max = df['High'].rolling(window=period).max()
    low_min = df['Low'].rolling(window=period).min()
    df['RSV'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['K'] = df['RSV'].ewm(alpha=1/signal_period).mean()
    df['D'] = df['K'].ewm(alpha=1/signal_period).mean()
    return df

def name():
    return 'KDCross'

if __name__ == '__main__':
    calculate()
