# Author: Yingtong Deng
# Blackjack
# Date due: 2020-11-06


import random

CARD_LABELS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
BLACKJACK = 21
DEALER_THRESHOLD = 16


def deal_card():
    """Evaluates to a character representing one of 13
    cards in the CARD_LABELS tuple

    :return: a single- or double-character string representing a playing card
    """
    card_label = random.choice(CARD_LABELS)
    return card_label


def get_card_value(card_label):
    """Evaluates to the integer value associated with
    the card label (a single- or double-character string)

    :param card_label: a single- or double-character string representing a card
    :return: an int representing the card's value
    """

    if card_label == "J" or card_label == "K" or card_label == "Q":
        card_label = 10
    if card_label == "A":
        card_label = 1
    card_label = int(card_label)

    return card_label

def deal_cards_to_player():
    """Deals cards to the player and returns the card
    total

    :return: the total value of the cards dealt
    """
    player_label_1 = deal_card()
    player_label_2 = deal_card()
    player_card_1 = get_card_value(player_label_1)
    player_card_2 = get_card_value(player_label_2)
    player_total = player_card_1 + player_card_2
    print("Player drew {} and {}.\nPlayer's total is {}.\n".format(str(player_label_1), str(player_label_2),
                                                                    str(player_total)))
    change_card = None
    while change_card != "s" and player_total < BLACKJACK:
        change_card = None
        while change_card not in ("s", "h"):
            change_card = input("Hit (h) or Stay (s)? ")
            print()
        if change_card == "h":
            player_extra_label = deal_card()
            player_extra = get_card_value(player_extra_label)
            player_total += player_extra
            print("Player drew {}.\nPlayer's total is {}.\n".format(str(player_extra_label), str(player_total)))

    return player_total


def deal_cards_to_dealer():
    """Deals cards to the dealer and returns the card
    total

    :return: the total value of the cards dealt
    """

    dealer_label_1 = deal_card()
    dealer_label_2 = deal_card()
    dealer_card_1 = get_card_value(dealer_label_1)
    dealer_card_2 = get_card_value(dealer_label_2)
    dealer_total = dealer_card_1 + dealer_card_2
    print("The dealer has {} and {}.\nDealer's total is {}.\n".format(str(dealer_label_1), str(dealer_label_2),
                                                                       str(dealer_total)))

    while dealer_total <= DEALER_THRESHOLD:
        dealer_extra_label = deal_card()
        dealer_extra = get_card_value(dealer_extra_label)
        dealer_total += dealer_extra
        print("Dealer drew {}.\nDealer's total is {}.\n".format(str(dealer_extra_label), str(dealer_total)))

    return dealer_total


def determine_outcome(player_total, dealer_total):
    """Determines the outcome of the game based on the value of
    the cards received by the player and dealer. Outputs a
    message indicating whether the player wins or loses.

    :param player_total: total value of cards drawn by player
    :param dealer_total: total value of cards drawn by dealer
    :return: None
    """
    # when they equal
    if dealer_total < player_total <= BLACKJACK or dealer_total > BLACKJACK:
        print("YOU WIN!\n")
    if player_total > BLACKJACK or player_total <= dealer_total <= BLACKJACK:
        print("YOU LOSE!\n")



# When the player's total is over 21 (`BLACKJACK`), the player loses.
# Furthermore, the dealer should not be dealt any cards when the player busts (receives a card total greater than 21).
# When the dealer's total is over 21, the player wins (as long as the player's total is 21 or under).


def play_blackjack():
    print("Let's Play Blackjack!\n")
    player_total = deal_cards_to_player()
    if player_total > BLACKJACK:
        dealer_total = DEALER_THRESHOLD
    else:
        dealer_total = deal_cards_to_dealer()
    determine_outcome(player_total, dealer_total)

    another_round = None
    while another_round != "N":
        another_round = None
        while another_round not in ("N", "Y"):
            another_round = input("Play again (Y/N)? ")
            print()
        if another_round == "Y":
            player_total = deal_cards_to_player()
            if player_total > BLACKJACK:
                dealer_total = DEALER_THRESHOLD
            else:
                dealer_total = deal_cards_to_dealer()
            determine_outcome(player_total, dealer_total)
        else:
            print("Goodbye.")


####### DO NOT EDIT ABOVE ########

def main():
    """Runs a program for playing Blackjack with one player
    and a dealer
    """

    # call play_blackjack() here and remove pass below
    play_blackjack()


####### DO NOT REMOVE IF STATEMENT BELOW ########

if __name__ == "__main__":
    main()