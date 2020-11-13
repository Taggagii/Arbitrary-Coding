#determines the winner for poker in the dumbest possible way
class Poker():
    def __init__(self):
        self.values = ['A', 'K', 'Q', 'J', 'T', '9',
                            '8', '7', '6', '5', '4', '3', '2']
        self.suits = ('C', 'S', 'D', 'H')
        self.hands = ('', '', '')
        self.counts = ([0, 0, 0, 0], [0, 0, 0, 0])
        self.number_hand = ([0]*14, [0]*14)
        self.hands_values = [0, 0]
        self.runners = [0, 1]
        self.high_cards = [0, 0]
        self.what_is = [0, 0]
        
    def winner(self, one, two):
        one, two = one.split(), two.split()
        self.hands = (one, two)
        self.suit_count()
        self.make_number_hand()
        self.check_royal_flush()
        if self.hands_values[0] > self.hands_values[1]: return 1
        if self.hands_values[0] < self.hands_values[1]: return 2
        return self.for_tie()
        
    def smaller(self, one, two):
        thing = [one, two]
        i = min(one, two)
        return thing.index(i)+1
    
    def for_tie(self):
        self.what_is = self.what_is[0]
        if self.what_is == 2 or self.what_is == 5:
            high_one = self.number_hand[0].index(1)
            high_two = self.number_hand[1].index(1)
            return self.smaller(high_one, high_two)
        if self.what_is == 3:
            high_one = self.number_hand[0].index(4)
            high_two = self.number_hand[1].index(4)
            return self.smaller(high_one, high_two)
        if self.what_is == 4:
            high_one_three = self.number_hand[0].index(3)
            high_two_three = self.number_hand[1].index(3)
            if high_one_three == high_two_three:
                high_one_two = self.number_hand[0].index(2)
                high_two_two = self.number_hand[1].index(2)
                return self.smaller(high_one_two, high_two_two)
            return self.smaller(high_one_three, high_two_three)
        if self.what_is == 6 or self.what_is == 10:
            for i in range(len(self.number_hand[0])):
                if self.number_hand[0][i] < self.number_hand[1][i]: return 2
                if self.number_hand[0][i] > self.number_hand[1][i]: return 1
        if self.what_is == 7:
            high_one = self.number_hand[0].index(3)
            high_two = self.number_hand[1].index(3)
            return self.smaller(high_one, high_two)
        if self.what_is == 8:
            high_one_one = self.number_hand[0].index(2)
            high_two_one = self.number_hand[1].index(2)
            if high_one_one == high_two_one:
                self.number_hand[0].reverse()
                self.number_hand[1].reverse()
                high_one_two = len(self.number_hand[0]) - self.number_hand[0].index(2) - 1
                high_two_two = len(self.number_hand[1]) - self.number_hand[1].index(2) - 1
                return self.smaller(high_one_two, high_two_two)
            return self.smaller(high_one_one, high_two_one) 
        if self.what_is == 9:
            high_one = self.number_hand[0].index(2)
            high_two = self.number_hand[1].index(2)
            return self.smaller(high_one, high_two)               
    
    def make_number_hand(self):
        for hand in range(2):
            for card in self.hands[hand]:
                for value in range(13):
                    if self.values[value] in card:
                        self.number_hand[hand][value] += 1
    
    def suit_count(self):
        for hand in range(2):
            for suit in range(len(self.suits)):
                for card in range(5):
                    if self.suits[suit] in self.hands[hand][card]:
                        self.counts[hand][suit] += 1

    def check_royal_flush(self):
        for number in self.runners:
            royal = True
            if 5 not in self.counts[number]: royal = False
            if royal:
                for place in (0, 1, 2, 3, 4):
                    if self.number_hand[number][place] != 1:
                        royal = False
                        break
            if royal:
                self.hands_values[number] = 10
                self.runners[number] -= 1
                self.what_is[number] = 1
            elif self.runners[0] >= 0 or self.runners[1] >= 1:
                self.check_straight_flush()
            
    def check_straight_flush(self):
        for number in self.runners:
            straight = False
            counter = 0
            if 5 in self.counts[number]:
                for card in (5, 6, 7, 8, 9, 10, 11, 12):
                    if straight and self.number_hand[number][card] != 1:
                        straight = False
                        break
                    elif self.number_hand[number][card] == 1: counter += 1
                    if counter == 4: break
                    if not straight and self.number_hand[number][card] == 1: straight = True
            if straight:
                self.hands_values[number] = 9
                self.runners[number] -= 1
                self.what_is[number] = 2
            elif self.runners[0] >= 0 and self.runners[1] >= 1:
                self.check_four_of_kind()
                
    def check_four_of_kind(self):
        for number in self.runners:
            if 4 in self.number_hand[number]: 
                self.hands_values[number] = 8
                self.runners[number] -= 1
                self.what_is[number] = 3
            elif self.runners[0] >= 0 or self.runners[1] >= 1:
                self.check_full_house()
        
                          
    def check_full_house(self):
        for number in self.runners:
            if 3 in self.number_hand[number] and 2 in self.number_hand[number]:
                self.hands_values[number] = 8
                self.runners[number] -= 1
                self.what_is[number] = 4
            elif self.runners[0] >= 0 or self.runners[1] >= 1:
                self.check_flush()
                
    def check_flush(self):
        for number in self.runners:
            if 5 in self.counts[number]:
                self.hands_values[number] = 7
                self.what_is[number] = 5
            elif self.runners[0] >= 0 or self.runners[1] >= 1:
                self.check_straight()
        
    def check_straight(self):
        for number in self.runners:
            straight = False
            counter = 0
            for card in (5, 6, 7, 8, 9, 10, 11, 12):
                if straight and self.number_hand[number][card] != 1:
                    straight = False
                    break
                elif straight and self.number_hand[number][card] == 1:
                    counter += 1
                if counter == 4: break
                if not straight and self.number_hand[number][card] == 1:
                    straight = True
            if straight:
                self.hands_values[number] = 6
                self.runners[number] -= 1
                self.what_is[number] = 6
            elif self.runners[0] >= 0 or self.runners[1] >= 1:
                self.check_three_of_kind()
                
    def check_three_of_kind(self):
        for number in self.runners:
            if 3 in self.number_hand[number]:
                self.hands_values[number] = 5
                self.runners[number] -= 1
                self.what_is[number] = 7
            elif self.runners[0] >= 0 or self.runners[1] >= 1:
                self.check_two_pairs()
        
    def check_two_pairs(self):
        for number in self.runners:
            if self.number_hand[number].count(2) == 2:
                self.hands_values[number] = 4
                self.runners[number] -= 1
                self.what_is[number] = 8
            elif self.runners[0] >= 0 or self.runners[1] >= 1:          
                self.check_one_pair()
        
    def check_one_pair(self):
        for number in self.runners:
            if 2 in self.number_hand[number]:
                self.hands_values[number] = 3
                self.runners[number] -= 1
                self.what_is[number] = 9
            else:
                self.hands_values[number] = 2
                self.runners[number] -= 1
                self.what_is[number] = 10



poker = Poker()
print(poker.winner('AH KH AS 3H 5H', 'AH KH AH 2H 5H'))
