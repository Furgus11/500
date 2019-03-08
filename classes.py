from random import shuffle
class Card:
	def __init__(self, suit, value, can_play = 1):
		if value == "Joker":
			self.string = "Joker"
			self.suit = suit
			self.value = value
			self.can_play = can_play # 1: true, 0: false
		else:
			self.suit = suit
			self.value = value
			self.string = value + " " + suit
			self.can_play = can_play
	def __str__(self):
		return self.string
	def __repr__(self):
		return self.string
	def sorting_value(self, trump = None):
		opposite = "None"
		if trump == "Spades":
			opposite = "Clubs"
		elif trump == "Clubs":
			opposite = "Spades"
		elif trump == "Hearts":
			opposite = "Diamonds"
		elif trump == "Diamonds":
			opposite = "Hearts"

		suit_value = 0
		if self.value == "Joker":
			return 100
		elif self.value == 'J' and self.suit == trump:
			return 99
		elif self.value == 'J' and self.suit == opposite:
			return 98

		elif self.suit == trump:
			suit_value = 4
		elif self.suit == "Hearts":
			suit_value = 3
		elif self.suit == "Diamonds":
			suit_value = 2
		elif self.suit == "Clubs":
			suit_value = 1
		elif self.suit == "Spades":
			suit_value = 0

		num_value = 0
		try:
			num_value = int(self.value) - 4
		except:
			if self.value == 'J':
				num_value = 7
			elif self.value == 'Q':
				num_value = 8
			elif self.value == 'K':
				num_value = 9
			elif self.value == 'A':
				num_value = 10

		return suit_value * 11 + num_value

class Deck:
	def __init__(self):
		self.deck = []
		suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
		values = ["4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
		for suit in suits:
			for value in values:
				self.deck.append(Card(suit, value))
		self.deck.append(Card(None, "Joker"))
	def __str__(self):
		return str(self.deck)
	def deal(self):
		shuffle(self.deck)
		return [self.deck[0:10], self.deck[10:20], self.deck[20:30], self.deck[30:40], self.deck[40:45]]
	def printDeck(self):
		for card in self.deck:
			print (card.string)




class Scoreboard:
	# team1 = 0
	# team2 = 0
	def __init__(self, score1 = 0, score2 = 0):
		self.team1 = score1
		self.team2 = score2
	def __str__(self):
		return ("Team 1: " + str(self.team1) + "\nTeam 2: " + str(self.team2))

class Bid:
	def __init__ (self, suit, number, bidder):
		self.suit = suit
		self.number = number
		self.bidder = bidder
		self.string = bidder.name + " " + str(number) + " " + suit

	def __str__(self):
		return self.string

	def canBid(oldBid, newBid):
		if newBid.suit == "pass":
			return True
		if oldBid.number == newBid.number and oldBid.suit == newBid.suit:
			return False
		elif oldBid.number > newBid.number:
			return False
		elif oldBid.number < newBid.number:
			return True
		else:
			suitOrder = ["Spades", "Clubs", "Diamonds", "Hearts", "notrump", "nullo"]
			if suitOrder.index(oldBid.suit) > suitOrder.index(newBid.suit):
				return False
			else:
				return True

	def computePoints(self):
	    if self.suit == "nullo":
	        return 250
	    if self.suit == "opennullo":
	        return 350
	    points = 0
	    if self.number == "7":
	        points = 140
	    elif self.number == "8":
	        points = 240
	    elif self.number == "9":
	        points = 340
	    elif self.number == "10":
	        points = 440
	    if self.suit == "Clubs":
	        points += 20
	    elif self.suit == "Diamonds":
	        points += 40
	    elif self.suit == "Hearts":
	        points += 60
	    elif self.suit == "notrump":
		    points += 80
	    return points



class Player:
	def __init__(self, name, team, hand, index):
		self.name = name
		self.team = team
		self.hand = hand
		self.index = index

	def __str__(self):
	    return self.name + " " + str(self.index)


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player0 = Player("Player1", "team1", [], 0)
        self.player1 = Player("Player2", "team2", [], 1)
        self.player2 = Player("Player3", "team1", [], 2)
        self.player3 = Player("Player4", "team2", [], 3)
        self.players = [self.player0, self.player1, self.player2, self.player3]
        self.player0.hand, self.player1.hand, self.player2.hand, self.player3.hand, self.blind = self.deck.deal()
        self.scoreboard = Scoreboard()
        self.turn = 0
        self.hand_number = 0
        # initial dealer is player3 so player0 bids first
        self.dealer = self.player3
        self.state = 0 # 0 need to bid, 1 need to play
        # bidding
        self.bids = []
        self.bidPasses = [False, False, False, False]
        self.current_bid = Bid("None", 0, Player("No bids yet", "team0", [], -1))

        # playing hand
        self.trickNumber = 0
        self.team1Tricks = 0
        self.team2Tricks = 0
        self.currentTrick = [None,None,None,None,None]
        self.currentTrickSuit = None
        self.tricks = []
        self.lastTrickOfHand = [None,None,None,None,None]
        self.team1LastHandTricks = -1
        self.team2LastHandTricks = -1
        # trick = [card1, card2, card3, card4, leadIndex]

    def current_trick_to_array(self):
        ret = []
        for i in range(4):
            if self.currentTrick[i] != None:
                ret.append(self.currentTrick[i].suit)
                ret.append(self.currentTrick[i].value)
            else:
                ret.append("")
                ret.append("")
        return ret

    def last_trick_to_array(self):
        if len(self.tricks) > 0:
            trick = self.tricks[-1]
            if trick[0] == None:
                c11 = ""
                c12 = ""
            else:
                c11 = trick[0].suit
                c12 = trick[0].value
            if trick[1] == None:
                c21 = ""
                c22 = ""
            else:
                c21 = trick[1].suit
                c22 = trick[1].value
            if trick[2] == None:
                c31 = ""
                c32 = ""
            else:
                c31 = trick[2].suit
                c32 = trick[2].value
            if trick[3] == None:
                c41 = ""
                c42 = ""
            else:
                c41 = trick[3].suit
                c42 = trick[3].value
            return [c11, c12, c21, c22, c31, c32, c41, c42, trick[4]]
        elif self.team1LastHandTricks > 0:
            trick = self.lastTrickOfHand
            if trick[0] == None:
                c11 = ""
                c12 = ""
            else:
                c11 = trick[0].suit
                c12 = trick[0].value
            if trick[1] == None:
                c21 = ""
                c22 = ""
            else:
                c21 = trick[1].suit
                c22 = trick[1].value
            if trick[2] == None:
                c31 = ""
                c32 = ""
            else:
                c31 = trick[2].suit
                c32 = trick[2].value
            if trick[3] == None:
                c41 = ""
                c42 = ""
            else:
                c41 = trick[3].suit
                c42 = trick[3].value
            return [c11, c12, c21, c22, c31, c32, c41, c42, trick[4]]
        else:
            return "tricks are empty"

    def get_player_by_index(self, index):
        for player in self.players:
            if player.index == int(index):
                return player
        raise Exception("No Player found\nIndex: " + index)

    def hand_to_array(self, player_index, playable):
        if player_index > 3 or player_index < 0:
            raise Exception("player index was out of range - player_index: " + str(player_index))
        try:
            if self.current_bid.suit == "None":
                self.players[player_index].hand.sort(key=lambda x: x.sorting_value())
            else:
                self.players[player_index].hand.sort(key=lambda x: x.sorting_value(self.current_bid.suit))
        except:
            return "couldn't access players[ " + str(player_index) + "].hand - " + str(self.players[player_index].hand)
        ret = []
        for card in self.players[player_index].hand:
            ret.append(card.suit)
            ret.append(card.value)
            if playable == 1:
                ret.append(card.can_play)
        return ret

    def blind_to_array(self):
        if self.current_bid.suit == "None":
            self.blind.sort(key=lambda x: x.sorting_value())
        else:
            self.blind.sort(key=lambda x: x.sorting_value(self.current_bid.suit))
        ret = []
        for card in self.blind:
            ret.append(card.suit)
            ret.append(card.value)
        return ret

    def addBid(self, passed, suit, number, playerIndex):
        p = self.get_player_by_index(playerIndex)
        if passed == "true":
            self.bidPasses[int(playerIndex)] = True
            self.bids.append(['passed', playerIndex])
        else:
            bid = Bid(suit, number, p)
            self.bids.append(bid)
            self.current_bid = bid
        return self.determine_next_bidder()
        # return "done with bid"

    def determine_next_bidder(self):
        self.turn += 1
        if self.turn == 4:
            self.turn = 0
        if False in self.bidPasses:
            while self.bidPasses[self.turn]:
                self.turn += 1
                if self.turn == 4:
                    self.turn = 0
        else:
            if int(self.current_bid.number) > 6:
                self.turn = self.current_bid.bidder.index
                self.state = 1
            else:
                # passout
                self.new_hand()
                return "passout"
        return "turn is now: " + str(self.turn)

    def bids_to_array(self):
        ret = []
        for bid in self.bids:
            try:
                if bid[0] == 'passed':
                    ret.append('passed')
                    ret.append('passed')
                    ret.append('Player' + str(int(bid[1]) + 1))
            except:
                ret.append(bid.number)
                ret.append(bid.suit)
                ret.append(bid.bidder.name)
        return ret

    def update_hand_with_blind(self, hand, hand_indexs, blind_indexs):
    	if len(hand_indexs) != len(blind_indexs):
    		raise Exception("Number to discard and number to add must be the same")
    	for i in range(len(hand_indexs)):
    		hand[hand_indexs[i]] = self.blind[blind_indexs[i]]
    	# update state to play mode
    	self.state = 2
    	return hand

    def play_card(self, player_index, suit, value):
        # put card in current trick
        self.currentTrick[player_index] = Card(suit, value)
        # remove card from current hand
        self.players[player_index].hand = self.remove_card_from_hand(self.players[player_index].hand, Card(suit, value))

        # update turn
        self.turn = player_index + 1
        if self.turn == 4:
            self.turn = 0

        if self.current_bid.suit == "nullo" or self.current_bid.suit == "opennullo":
            if self.turn - self.current_bid.bidder.index == 2 or self.turn - self.current_bid.bidder.index == -2:
                self.turn += 1
                if self.turn == 4:
                    self.turn = 0

        # if that was first card played, set lead suit and update other hands card.can_play
        if self.one_card_played():
            if suit == self.get_opposite(self.current_bid.suit) and value == "J":
                self.currentTrickSuit = self.current_bid.suit
            elif value == "Joker":
                self.currentTrickSuit = self.current_bid.suit
            else:
                self.currentTrickSuit = suit
            self.currentTrick[4] = player_index
            self.update_other_hands_playable_cards(player_index)
        # if that was last card, append trick, determine winner of trick, set next lead(turn), clear current trick
        if self.trick_played():
            self.tricks.append(self.currentTrick)
            self.handle_end_trick()
            # if that was trick 10, update score, check score for winners/losers, reset tricks, enter bid state: move dealer
            if self.trickNumber == 10:
                self.lastTrickOfHand = self.tricks[-1]
                self.team1LastHandTricks = self.team1Tricks
                self.team2LastHandTricks = self.team2Tricks
                self.update_score_from_bid()
                if self.scoreboard.team1 >= 500 or self.scoreboard.team1 <= -500 or self.scoreboard.team2 >= 500 or self.scoreboard.team2 <= -500:
                    # call end game function
                    self.state = 3
                else:
                    self.new_hand()

        return "played card"

    def new_hand(self):
        # deal new cards
        self.player0.hand, self.player1.hand, self.player2.hand, self.player3.hand, self.blind = self.deck.deal()
        # dealer update
        if self.dealer.index == 0:
            self.dealer = self.player1
            self.turn = 2
        elif self.dealer.index == 1:
            self.dealer = self.player2
            self.turn = 3
        elif self.dealer.index == 2:
            self.dealer = self.player3
            self.turn = 0
        elif self.dealer.index == 3:
            self.dealer = self.player0
            self.turn = 1

        # bidding stage reset
        self.state = 0 # 0 need to bid, 1 need to play
        # bidding
        self.bids = []
        self.bidPasses = [False, False, False, False]
        self.current_bid = Bid("None", 0, Player("No bids yet", "team0", [], -1))

        # playing hand
        self.trickNumber = 0
        self.team1Tricks = 0
        self.team2Tricks = 0
        self.currentTrick = [None,None,None,None,None]
        self.currentTrickSuit = None
        self.tricks = []

    def update_score_from_bid(self):
        if self.current_bid.suit == "nullo" or self.current_bid.suit == "opennullo":
            if self.current_bid.bidder.index == 0 or self.current_bid.bidder.index == 2:
                self.award_nullo_points("team1")
                self.award_nullo_not_taken_points("team2")
            elif self.current_bid.bidder.index == 1 or self.current_bid.bidder.index == 3:
                self.award_nullo_points("team2")
                self.award_nullo_not_taken_points("team1")
        elif self.current_bid.bidder.index == 0 or self.current_bid.bidder.index == 2:
            self.award_made_or_miss_bid_points("team1")
            self.award_tricks_taken_points("team2")
        elif self.current_bid.bidder.index == 1 or self.current_bid.bidder.index == 3:
            self.award_made_or_miss_bid_points("team2")
            self.award_tricks_taken_points("team1")

    def award_nullo_not_taken_points(self, team):
        if team == "team1":
            self.scoreboard.team1 += 10 * self.team2Tricks
        elif team == "team2":
            self.scoreboard.team2 += 10 * self.team1Tricks

    def award_nullo_points(self, team):
        nullo_points = self.current_bid.computePoints()
        if team == "team1":
            if self.team1Tricks == 0:
                self.scoreboard.team1 += nullo_points
            else:
                self.scoreboard.team1 -= nullo_points
        elif team == "team2":
            if self.team2Tricks == 0:
                self.scoreboard.team2 += nullo_points
            else:
                self.scoreboard.team2 -= nullo_points
    def award_made_or_miss_bid_points(self, team):
        points = self.current_bid.computePoints()
        if points < 250 and (self.team1Tricks == 10 or self.team2Tricks == 10):
            points = 250
        if team == "team1":
            if self.team1Tricks >= int(self.current_bid.number):
                self.scoreboard.team1 += points
            else:
                self.scoreboard.team1 -= points
        elif team == "team2":
            if self.team2Tricks >= int(self.current_bid.number):
                self.scoreboard.team2 += points
            else:
                self.scoreboard.team2 -= points

    def award_tricks_taken_points(self, team):
        if team == "team1":
            self.scoreboard.team1 += 10 * self.team1Tricks
        elif team == "team2":
            self.scoreboard.team2 += 10 * self.team2Tricks

    def handle_end_trick(self):
        # What if the bid is nullo and one of the trick spots is empty?
        # determine winner of trick, update score, set next lead(turn), clear current trick
        lead = self.currentTrickSuit
        trump = self.current_bid.suit
        opposite = self.get_opposite(trump)

        i = self.get_index_of_winning_card(self.currentTrick, lead, trump, opposite)

        # set turn to that players index
        self.turn = i
        # use index to determine which team gets self.team1/2Tricks increased
        if i == 0 or i == 2:
            self.team1Tricks += 1
        elif i == 1 or i ==3:
            self.team2Tricks += 1
        else:
            raise Exception("Index of winner was not 0-3")
        # clear current trick
        self.currentTrick = [None,None,None,None,None]
        self.currentTrickSuit = None
        self.trickNumber += 1

        # set can play of winner hand to 1
        update_hand = []
        for card in self.players[self.turn].hand:
            update_hand.append(Card(card.suit,card.value, 1))
        self.players[self.turn].hand = update_hand


    def get_index_of_winning_card(self, trick, lead, trump, opposite):
    	card_value_list = []
    	cards_of_trump = []
    	for i in range(4):
    		card = trick[i]
    		if card != None:
    			if card.suit == trump or card.value == "Joker" or (card.value == "J" and card.suit == opposite):
    				cards_of_trump.append(card)

    	if cards_of_trump == []:
    		for i in range(4):
    			card = trick[i]
    			if card != None:
    				if card.suit == lead:
    					cards_of_trump.append(card)
    		card_value_list = [["4", lead], ["5", lead], ["6", lead], ["7", lead], ["8", lead], ["9", lead], ["10", lead], ["J", lead], ["Q", lead], ["K", lead], ["A", lead], ["Joker", 'null']]
    	else:
    		card_value_list = [["4", trump], ["5", trump], ["6", trump], ["7", trump], ["8", trump], ["9", trump], ["10", trump], ["Q", trump], ["K", trump], ["A", trump], ["J", opposite], ["J", trump], ["Joker", 'null']]

    	max_index = -1
    	max_card = None
    	for card in cards_of_trump:
    		card_index = card_value_list.index([card.value, card.suit])
    		if card_index > max_index:
    			max_index = card_index
    			max_card = card
    	for i in range(4):
    		card = trick[i]
    		if card != None:
    			if card.value == max_card.value and card.suit == max_card.suit:
    				return i
    	raise Exception("Coundn't find fucking winning card")


    def remove_card_from_hand(self, hand, card_to_remove):
        ret = []
        if card_to_remove.value == "Joker":
            for card in hand:
                if card.value != "Joker":
                    ret.append(card)
        else:
            for card in hand:
                if card.value != card_to_remove.value or card.suit != card_to_remove.suit:
                    ret.append(card)
        return ret

    def one_card_played(self):
        count = 0
        for i in range(4):
            c = self.currentTrick[i]
            if c == None:
                count += 1
        return count == 3
    def trick_played(self):
        count = 0
        for i in range(4):
            c = self.currentTrick[i]
            if c == None:
                count += 1
        if self.current_bid.suit == "nullo" or self.current_bid.suit == "opennullo":
            return count == 1
        else:
            return count == 0

    def update_other_hands_playable_cards(self, player_index):
        for i in range(4):
            if i != player_index:
                self.players[i].hand = self.update_playable_of_hand(self.players[i].hand, self.currentTrickSuit, self.current_bid.suit)

    def get_opposite(self, trump):
        opposite = "None"
        if trump == "Spades":
            opposite = "Clubs"
        elif trump == "Clubs":
            opposite = "Spades"
        elif trump == "Diamonds":
            opposite = "Hearts"
        elif trump == "Hearts":
            opposite = "Diamonds"
        return opposite

    def update_playable_of_hand(self, hand, leadSuit, trumpSuit):
        opposite = self.get_opposite(trumpSuit)
        ret = []
        if leadSuit == trumpSuit:
            has_trump_suit = False
            for card in hand:
                if card.suit == trumpSuit or (card.suit == opposite and card.value == "J") or card.value == "Joker":
                    has_trump_suit = True
            if has_trump_suit:
                for card in hand:
                    if card.suit == trumpSuit or card.value == "Joker" or (card.suit == opposite and card.value == "J"):
                        ret.append(Card(card.suit, card.value, 1))
                    else:
                        ret.append(Card(card.suit, card.value, 0))
            else:
                for card in hand:
                    ret.append(Card(card.suit, card.value, 1))

        else:
            has_lead_suit = False
            for card in hand:
                if card.suit == leadSuit and not (card.suit == opposite and card.value == "J"):
                    has_lead_suit = True
            if has_lead_suit:
                for card in hand:
                    if card.value == "J" and card.suit == opposite:
                        ret.append(Card(card.suit, card.value, 0))
                    elif card.suit == leadSuit:
                        ret.append(Card(card.suit, card.value, 1))
                    else:
                        ret.append(Card(card.suit, card.value, 0))
            else:
                for card in hand:
                    ret.append(Card(card.suit, card.value, 1))
        return ret

    def get_num_tricks(self, team):
        if self.trickNumber == 0 and team == 1:
            return self.team1LastHandTricks
        elif self.trickNumber == 0 and team == 2:
            return self.team2LastHandTricks
        elif self.trickNumber != 0 and team == 1:
            return self.team1Tricks
        elif self.trickNumber != 0 and team == 2:
            return self.team2Tricks










