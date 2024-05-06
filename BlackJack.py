from itertools import product
import random
from os import linesep
#Run my code to see the rules
suits = ('Hearts', 'Clubs', 'Spades', 'Diamonds')
numbers = [2,3,4,5,6,7,8,9,10,11,12,13,14]
a = 551
user = ""
standard_deck = []
playing_deck = []
playerHand = []
dealerHand = []
end = False
status = ""
bust  = ""
def rules():
    print(" ")
    print("This is blackjack. The goal is to reach 21 without going over (busting).")
    print("The dealer deals from 3 decks combined, as a casino would have.")
    print("Aces are worth either 11 or 1. The first ace you get is 11, unless it'll make you bust, and everyone after that is a 1.")
    print("The dealer deals two cards to each person, one face up and one face down.")
    print("The dealer is only allowed to look at their cards if they has a 10 or an ace face up, and has to reveal if they have blackjack.")
    print("Otherwise they have to deal to themselves until they get to 17 with face up cards .")
    print("If you bust you lose, but you automatically win when you hit 21.")
    print("You start with 500 dollars.")
    print("When you win the amount of money you bet is doubled, but you only lose as much as you bet.")
    print("You are forced to restart once you hit 1 million dollars or lose all of your money.")
    print("Each round the deck is reset.")

def create_standard_deck():
    #This creates a standard deck that has 3 decks like an actual casino. You can change the first for loop for different amount of decks
    deck = []
    for i in range(3):
        for i in range(len(suits)):
            for x in numbers:
                card = [suits[i],x]
                deck.append(card)
    return deck

def remove_card_from_deck(playing_deck, card):
    #This removes a card from the deck
    playing_deck.remove(card)
    return playing_deck

def draw_card(hand,deck):
    #This draws a card, adds removes it from the deck, then adds it to the current hand
    num = random.choice(range(2,len(deck)))
    card = deck[num]
    remove_card_from_deck(deck,card)
    if card[1] == 14:
        card[1] = "Ace"
    elif card[1] == 13:
        card[1] = "King"
    elif card[1] == 12:
        card[1] = "Queen"
    elif card[1] == 11:
        card[1] = "Jack"
    hand.append(card)
    return hand,deck

def get_count(player):
    #This gets the count of the current hand
    count = 0
    aceCount = 0
    for i in player:
        if i[1] == "Ace":
            if aceCount == 0 and count < 11:
                count += 11
                aceCount += 1
            else:
                count += 1
                aceCount += 1
        elif i[1] == "King":
            count += 10
        elif i[1] == "Queen":
            count += 10
        elif i[1] == "Jack":
            count += 10
        else:
            count += i[1]
    return count

def bet_amount(credit):
    #This allows the user to make bets and cleans up my code
    while True:
        try:
            bet = int(input("How much would you like to bet? "))
            while bet > credit or bet < 0:
                try:
                    bet = int(input("Please input a bet less than your balance and greater than 0: "))
                except ValueError:
                    print("Please input a number.")
                    print(" ")
            break
        except ValueError:
            print("Please enter a number.")
            print(" ")
    credit -= bet
    return bet,credit

def credit_change(credit,bet,status):
    if status is True:
        credit += bet*2
        print("You won "+str(bet*2))
        print("Your new balance is: "+str(credit))
    else:
        print("You lost "+str(bet))
        print("Your new balance is: "+str(credit))
    return credit

def bank_change(bank,bet,status):
    if status is True:
        bank -= bet
    else:
        bank += bet
    return bank

def display_dealer(dealerHand):
    #This is to display the dealer's hand
    num = len(dealerHand)-1
    count = get_count(dealerHand)
    print(" ")
    print("Dealer's Hand:")
    if count == 21:
        for i in range(len(dealerHand)):
            if i == num:
                print(dealerHand[i])
            else:
                print(dealerHand[i],end=", ")
    else:
        print("['?',?]",end=", ")
        for i in range(1,len(dealerHand)):
            if i == num:
                print(dealerHand[i])
            else:
                print(dealerHand[i],end=", ")

def display_player(playerHand):
    #This displays the players hand and count
    count = get_count(playerHand)
    print("Player's Hand:")
    #This is so the comma won't be added to the last variable
    num = len(playerHand)-1
    for i in range(len(playerHand)):
        if i == num:
            print(playerHand[i])
        else:
            print(playerHand[i],end=", ")
    print("Count: "+str(count))

def display_dealer_whole(dealerHand):
    #This displays the dealers hand where the user can all cards
    count = get_count(dealerHand)
    print("Dealer's Hand:")
    print(dealerHand)
    print("Count: "+str(count))
    
def draw_dealer(dealerHand,playing_deck):
    #This draws for the dealer and using traditional rules the dealer draws until they hit 17 or more
    firstCard = dealerHand[0]
    num = firstCard[1]
    if num == "Jack":
        num = 10
    elif num == "Queen":
        num = 10
    elif num == "King":
        num = 10
    elif num == "Ace":
        num = 11
    count = get_count(dealerHand)-num
    while count < 17:
        dealerHand, playing_deck = draw_card(dealerHand,playing_deck)
        count = get_count(dealerHand)-num
    return dealerHand, playing_deck

def display_hands(dealerHand,playerHand):
    #This displays both hands
    display_dealer(dealerHand)
    display_player(playerHand)

def reset_values(hand1, hand2):
    #Resets the hands for a new game
    hand1 = []
    hand2 = []
    return hand1, hand2

def play_again(status):
    if status == True:
        user = input("You won, but you can win bigger.\nWould you like to play again(y/n)? ")
        while user.lower() != "n" and user.lower() != "y":
            print(" ")
            user = input("Please enter y to play again and n to quit: ")
    else:
        user = input("You lost but victory is close.\nWould you like to play again(y/n)? ")
        while user.lower() != "n" and user.lower() != "y":
            print(" ")
            user = input("Please enter y to play again and n to quit: ")
    if user.lower() == "n":
        playAgain = False
    else:
        playAgain = True
    return playAgain

def check_status(dealerHand,playerHand,end,credit):
    #This compares hands to see who won
    dealerCount = get_count(dealerHand)
    playerCount = get_count(playerHand)
    status = False
    bust = False
    if end == True:
        display_dealer_whole(dealerHand)
        display_player(playerHand)
        if dealerCount > 21 or playerCount == 21:
            status = True
        elif dealerCount > playerCount or dealerCount == playerCount:
            status = False
        elif credit < 0:
            status = False
        else:
            status = True
        return status
    else:
        if playerCount > 21:
            status = False
            bust = True
        else:
            bust = False
        return bust

standard_deck = create_standard_deck()
playing_deck = standard_deck
credit = 500
bank = 10000000
while True:
    end = False
    rules()
    print(" ")
    print("Bank: "+str(bank))
    print("Balance: "+str(credit))
    bet,credit = bet_amount(credit)
    dealerHand, playerHand = reset_values(dealerHand, playerHand)
    #This is to make sure the player never runs out of cards
    if len(playing_deck) <= 4:
        playing_deck = standard_deck
    for i in range(2):
        playerHand,playing_deck = draw_card(playerHand,playing_deck)
        dealerHand,playing_deck = draw_card(dealerHand,playing_deck)
    display_hands(dealerHand,playerHand)
    while user is not False:
        user = input("\nPress h to hit, Press s to stand, Press q to quit\nWhat would you like to do? ")
        print(" ")
        while user.lower() != "h" and user.lower() != "s" and user.lower() != "q":
            user = input("\nPress h to hit, Press s to stand, Press q to quit\nWhat would you like to do? ")
        if user.lower() == "h":
            playerHand,playing_deck = draw_card(playerHand,playing_deck)
            display_hands(dealerHand,playerHand)
            #This checks if the player has busted
            bust = check_status(dealerHand,playerHand,end,credit)
            if bust is True:
                status = False
                credit = credit_change(credit,bet,status)
                bank = bank_change(bank,bet,status)
                user = play_again(status)
                break
            else:
                continue
        elif user.lower() == "s":
            if get_count(dealerHand) < 21:
                dealerHand, playing_deck = draw_dealer(dealerHand,playing_deck)
            end = True
            status = check_status(dealerHand,playerHand,end,credit)
            credit = credit_change(credit,bet,status)
            bank = bank_change(bank,bet,status)
            user = play_again(status)
            break
        else:
            user = False
    if user is False:
        break
    else:
        continue
print(" ")
print("Did you know tha most gamblers quit before winning big? Anyways, thank you for playing!")