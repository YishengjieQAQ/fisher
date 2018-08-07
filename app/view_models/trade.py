from app.view_models.book import Bookviewmodel


class Tradeinfo:
    def __init__(self, all):
        self.total = 0
        self.trades = []
        self.__parse(all)

    def __parse(self, all):
        self.total = len(all)
        self.trades = [self.__map_to_trade(single) for single in all]


    def __map_to_trade(self,single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'

        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id

        )

class MyTrade:
    def __init__(self, trade_count_list, trade_of_mine):
        self.trade = []
        self.__trade_of_mine = trade_of_mine
        self.__trade_count_list = trade_count_list
        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trade_of_mine:
            one = self.__matching(trade)
            temp_trades.append(one)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'trades_count': count,
            'book': Bookviewmodel(trade.current_book),
            'id': trade.id
        }

        return r


