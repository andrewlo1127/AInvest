import importlib
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os
import py_compile

class HtmlViewer(QMainWindow):
    def __init__(self, file):
        super().__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        # 使用绝对路径
        file_path = os.path.abspath(file)
        url = QUrl.fromLocalFile(file_path)
        self.browser.setUrl(url)
        self.setWindowTitle("HTML Viewer")

def find_code_id(name, rslt, connection):
    with connection.cursor() as cursor:
        sql = """
        SELECT code_id
        FROM code
        WHERE strategy = %s
        """
        cursor.execute(sql, (name,))
        code_id = cursor.fetchone()[0]
    return code_id

# 將結果寫入資料庫
def insert_rslt_to_db(name, rslt, code_id, ticker, connection, member_id):
    with connection.cursor() as cursor:
        result_sql = """
        INSERT INTO test_head (code_id, member_id, target_name, times, sucess_p, acc_profit, acc_profit_margin, enter_time, exit_time, continue_time, buy_and_hold_return, html)
        VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(result_sql, (
            code_id,
            member_id,
            ticker.replace('.TW', ''),
            rslt['# Trades'],
            rslt['Win Rate [%]'],
            rslt['Return'],
            rslt['Return [%]'],
            rslt['Start'],
            rslt['End'],
            rslt['Duration'],
            rslt['Buy & Hold Return [%]'],
            name+'.html'
        ))
        connection.commit()

def find_th_id(connection):
    with connection.cursor() as cursor:
        sql = """
        SELECT th_id
        FROM test_head
        ORDER BY th_id DESC
        LIMIT 1
        """
        cursor.execute(sql)
        th_id = cursor.fetchone()[0]
    return th_id

def insert_trades_to_db(trades, th_id, connection):
    with connection.cursor() as cursor:
        for index, trade in trades.iterrows():
            sql = """
            INSERT INTO test_body (th_id, enter_date, exit_date, enter_price, exit_price, size, profit, profit_margin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                th_id,
                trade['EntryTime'],
                trade['ExitTime'],
                trade['EntryPrice'],
                trade['ExitPrice'],
                trade['Size'],
                trade['PnL'],
                trade['ReturnPct']
            ))
        connection.commit()

def get_file_name(connection, member_id, name):
    with connection.cursor() as cursor:
        sql = """
        SELECT file_name
        FROM code
        WHERE member_id = %s 
        AND strategy = %s
        """
        cursor.execute(sql, (member_id, name,))
        file_name = cursor.fetchone()[0]
    return file_name

def load_module(file_name):
    if file_name in sys.modules:
        del sys.modules[file_name]  # 刪除舊模塊，以便重載
        print(f"已刪除 {file_name} 模塊")

    # 動態導入指定的測試文件
    test_module = importlib.import_module(file_name)
    importlib.reload(test_module)

    return test_module

def test1_main(data, member_id,state):
    db_config = {
        'host': '3.106.70.39',
        'user': 'InvestUser',
        'password': 'Zw.urVWv*gD@J5rT',
        'database': 'aiinvest'
    }
    connection = pymysql.connect(**db_config)

    # 下載股票歷史數據
    ticker = data[0]
    start_date = data[2]
    end_date = data[3]
    money = data[5]
    commission = data[6]
    if (isinstance(ticker, list)):
        reslt = []
        file_name = get_file_name(connection, member_id, data[1])
        module = load_module(file_name)
        for tick in ticker:
            df = yf.download(tick, start=start_date, end=end_date)
            df = module.calculate(df)
            bt = Backtest(df.dropna(), module.strategy, cash=int(money), commission=float(commission))
            try:
                rslt = bt.run()
            except ValueError:
                rslt = {
                        'Start': 'NA',
                        'End': 'NA',
                        '# Trades': 'NA',
                        'Win Rate [%]': 'NA',
                        'Equity Final [$]': 'NA',
                        'Return [%]': 'NA',
                        'Buy & Hold Return [%]': 'NA',
                        'Sharpe Ratio': 'NA',
                        'Sortino Ratio': 'NA',
                        'Calmar Ratio': 'NA',
                        'Max. Drawdown [%]': 'NA',
                        'Avg. Drawdown [%]': 'NA',
                        'Max. Drawdown Duration': 'NA',
                        'Avg. Drawdown Duration': 'NA',
                        'Profit Factor': 'NA',
                        'Expectancy [%]': 'NA',
                        'SQN': 'NA'
                       }
                continue
            except Exception:
                rslt = {
                        'Start': 'NA',
                        'End': 'NA',
                        '# Trades': 'NA',
                        'Win Rate [%]': 'NA',
                        'Equity Final [$]': 'NA',
                        'Return [%]': 'NA',
                        'Buy & Hold Return [%]': 'NA',
                        'Sharpe Ratio': 'NA',
                        'Sortino Ratio': 'NA',
                        'Calmar Ratio': 'NA',
                        'Max. Drawdown [%]': 'NA',
                        'Avg. Drawdown [%]': 'NA',
                        'Max. Drawdown Duration': 'NA',
                        'Avg. Drawdown Duration': 'NA',
                        'Profit Factor': 'NA',
                        'Expectancy [%]': 'NA',
                        'SQN': 'NA'
                       }
                continue
            print(rslt)
            tick = tick.replace('.TW', '')
            bt.plot(filename='./HTML/'+str(tick)+'.html', open_browser=False)
            reslt.append(rslt)
            # 返回只包含所需字段的 DataFrame
        return reslt
    else:
        df = yf.download(ticker, start=start_date, end=end_date)
        # 找出檔案名稱
        if state ==0:  # 用不到了
            member_id = 5
            file_name = get_file_name(connection, member_id, data[1])
            module = load_module(file_name)
        else:
            file_name = get_file_name(connection, member_id, data[1])
            module = load_module(file_name)
        print(file_name)
        # 計算 KD
        df = module.calculate(df)

        # 抓取策略名稱
        name = module.name()  # 調用實例的 name() 方法
        print("name:", name)

        # 運行回測
        bt = Backtest(df.dropna(), module.strategy, cash=int(money), commission=float(commission))
        rslt = bt.run()
        print(rslt)
        print("\n", rslt["_trades"])

        rslt["Return"] = 0
        for index, trade in rslt['_trades'].iterrows():
            rslt["Return"] += float(trade['PnL'])
        html_file = f"strategy"
        bt.plot(filename='./HTML/'+html_file+'.html', open_browser=False)
        # bt.plot(open_browser=False)

        code_id = find_code_id(name, rslt, connection)
        insert_rslt_to_db(name, rslt, code_id, ticker, connection,member_id)
        th_id = find_th_id(connection)
        insert_trades_to_db(rslt['_trades'], th_id, connection)

        connection.close()
        print(data[0])
        # 返回只包含所需字段的 DataFrame
        return rslt, rslt['_trades'][['EntryTime', 'ExitTime', 'EntryPrice', 'ExitPrice', 'Size', 'PnL', 'ReturnPct']]

if __name__ == '__main__':
    test1_main()