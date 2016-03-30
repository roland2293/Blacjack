# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        self.ace = False

    def __str__(self):
        # return a string representation of a hand
        ans = "Hand contains "
        for i in range(len(self.hand)):
            ans = ans + str(self.hand[i]) + " "
        return ans
    
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = 0
        for card in self.hand:
            if (card.get_rank() == 'A'):
                self.ace = True
            for key, value in VALUES.items():
                if card.get_rank() == key:
                    self.value += value
        if not (self.ace):
            return self.value
        else:
            if self.value + 10 <= 21:
                return self.value + 10
            else:
                return self.value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand:
            card.draw(canvas, [pos[0]+self.hand.index(card)*100, pos[1]])
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)                    

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        card = self.deck[-1]
        self.deck.pop(-1)
        return card
    
    def __str__(self):
        # return a string representing the deck
        ans = "Deck contains "
        for i in range(len(self.deck)):
            ans = ans + str(self.deck[i]) + " "
        return ans

player_hand = Hand()
dealer_hand = Hand()

#define event handlers for buttons
def deal():
    global outcome,score, in_play, game, player_hand, dealer_hand
    # your code goes here
    if in_play:
        score -= 1
        outcome = "You Lose! New Deal?"
        in_play = False
    else:
        in_play = True
        game = Deck()
        game.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        dealer_hand.add_card(game.deal_card())
        dealer_hand.add_card(game.deal_card())
        player_hand.add_card(game.deal_card())
        player_hand.add_card(game.deal_card())
        outcome = "Hit or Stand?"    

def hit():
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global score, in_play, outcome
    if in_play:
        player_hand.add_card(game.deal_card())
        if player_hand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "You are busted! New Deal?"

    
def stand():
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global score, in_play, outcome
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(game.deal_card())
        if dealer_hand.get_value() < player_hand.get_value() or dealer_hand.get_value() > 21:
            score += 1
            outcome = "You Won! New Deal?"
        else:
            score -= 1
            outcome = "You Lose! New Deal?"

    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [50, 100], 55, "Red")
    canvas.draw_text("Score "+str(score), [400, 100], 40, "Black")
    canvas.draw_text("Dealer", [50, 150], 30, "Black")
    canvas.draw_text("Player", [50, 375], 30, "Black")
    canvas.draw_text(outcome, [200, 375], 30, "Black")
    player_hand.draw(canvas, [50, 425])
    dealer_hand.draw(canvas, [50, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric