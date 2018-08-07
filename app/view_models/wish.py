from app.view_models.book import Bookviewmodel


class MyWishes:
    def __init__(self, gift_count_list,  wishes_of_mine):
        self.wishes = []
        self.__wishes_of_mine = wishes_of_mine
        self.__gift_count_list = gift_count_list
        self.wishes = self.__parse()

    def __parse(self):
        temp_wishes = []
        for gift in self.__wishes_of_mine:
            one = self.__matching(gift)
            temp_wishes.append(one)
        return temp_wishes

    def __matching(self, wish):
        count = 0
        for gift_count in self.__gift_count_list:
            if wish.isbn == gift_count['isbn']:
                count = gift_count['count']
        my_wish = {
           'gifts_count': count,
            'book': Bookviewmodel(wish.current_book),
            'id': wish.id
        }

        return my_wish

