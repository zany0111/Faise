import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.deck.append(created_card)
    def shuffle(self):
        random.shuffle(self.deck)
    def remove_one(self):
        return self.deck.pop(0)

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
class Chip:
    def __init__(self):
        self.total = 100
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed", chips.total)
            else:
                break
def hit(deck, hand):
    single_card = deck.remove_one()
    hand.add_card(single_card)
    hand.adjust_for_ace()
def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input('Hit or Stand? (h/s) ')
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer's turn.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break
def show_game(player, dealer):
    print("\nDealer's hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's hand:", *player.cards, sep='\n ')
def show_all(player, dealer):
    print("\nDealer's hand:", *dealer.cards, sep='\n ')
    print("Dealer's hand =", dealer.value)
    print("\nPlayer's hand:", *player.cards, sep='\n ')
    print("Player's hand =", player.value)
def player_busts(player, dealer, chips):
    print('Player busts!')
    chips.lose_bet()
def player_wins(player, dealer, chips):
    print('Player wins!')
    chips.win_bet()
def dealer_busts(player, dealer, chips):
    print('Dealer busts!')
    chips.win_bet()
def dealer_wins(player, dealer, chips):
    print('Dealer wins!')
    chips.lose_bet()
def push(player, dealer):
    print('Dealer and player tie! PUSH.')
while True:
    print('Welcome to Blackjack!')
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.remove_one())
    player_hand.add_card(deck.remove_one())
    dealer_hand = Hand()
    dealer_hand.add_card(deck.remove_one())
    dealer_hand.add_card(deck.remove_one())
    player_chips = Chip()
    take_bet(player_chips)
    show_game(player_hand, dealer_hand)
    playing = True
    while playing:
        hit_or_stand(deck, player_hand)
        show_game(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    print(f"\nPlayer's total chips are at: {player_chips.total}")
    new_game = input('Would you like to play another hand? (y/n) ')
    if new_game[0].lower() == 'y':
        continue
    else:
        print('Thanks for playing!')
        break
