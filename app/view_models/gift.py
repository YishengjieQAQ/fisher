from app.view_models.book import Bookviewmodel


class MyGifts:
    def __init__(self, wish_count_list,  gifts_of_mine):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            one = self.__matching(gift)
            temp_gifts.append(one)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        my_gift = {
           'trades_count': count,
            'book': Bookviewmodel(gift.current_book),
            'id': gift.id
        }

        return my_gift

