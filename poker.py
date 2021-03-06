# coding=utf-8
"""This Python program solves Project Euler problem #54.

# THIS VERSION HAS BEEN SUPERSEDED BY THE ONE IN THE Py-classes directory

Program reads in a file with two poker hands per line and determines
how many are won by hand one. There are no ties.

Much of the code is not as efficient as could be. It was written
with understanding and maintainability in mind. Parts of the code
are described in the adjacent file outline.vim. In future will
create a version using classes.
"""
from collections import Counter
from operator import itemgetter

__author__ = 'rzucker'

CARD_VALS = "_123456789TJQKA"  # Used for converting the card values to 2..14
SUIT_VALS = "CDHS"             # Used for converting suits to 0..3

# Used to be a constant for hand types for comparison.
# This dictionary isn't truly necessary, but it makes for easier
# to understand code.
HAND_TYPE_VALS = {'Straight Flush': 9,
                  '4 Kind':         8,
                  'Full House':     7,
                  'Flush':          6,
                  'Straight':       5,
                  '3 Kind':         4,
                  'Two Pair':       3,
                  'One Pair':       2,
                  'High Card':      1}

# This dictionary is just used to make it easier to code debug messages when needed
DEBUG_HAND_TYPE_STRING = {9: "Straight Flush",
                          8: "4 of a Kind",
                          7: "Full House",
                          6: "Flush",
                          5: "Straight",
                          4: "3 of a Kind",
                          3: "Two Pair",
                          2: "One Pair",
                          1: "High Card"}


def straight(hand):
    """Returns true if hand is a straight.

    :param hand: a 2D array, 5x2, with a single hand
    hand is assumed to already sorted by value from high to low
    Therefore, can determine if it is a straight by making sure next card is one less than previous
    """

    # last_card is set to highest
    last_card = hand[0][0]
    for i in range(1, 5):
        # for next four cards make sure it is one less than the previous card
        if (last_card-1) == hand[i][0]:
            # set last card to be the latest card checked
            last_card = hand[i][0]
        else:
            return False
    return True


def flush(hand):
    """ Returns true if hand is a flush; i.e., suit is same for all five cards.

    :param hand: a 2D array, 5x2, with a single hand
    """

    # set suit to that of the first card
    suit = hand[0][1]
    for i in range(1, 5):
        # check suit of each remaining card to that of the first card
        if suit != hand[i][1]:
            return False
    return True


def straight_flush(hand):
    """Call the straight and flush functions.

    :param hand: a 2D  array, 5x2, with a single hand
    Could save computation by using a combined function
    to figure out all three, but this is clearer
    """

    return straight(hand) and flush(hand)


def card_val_convert(card):
    """Convert the card value into an integer, two to fourteen.

    :param card: a single string value, from 2 to TJQKA
    Use string find method on CARD_VALS list
    """

    card_val = CARD_VALS.find(card)
    return card_val


def card_suit_convert(card):
    """Convert the suit into an integer, zero to three.

    :param card: a single string value, one of C, D, H, or S
    """

    card_suit_num = SUIT_VALS.find(card)
    return card_suit_num


def hand_type(hand, card_counts):
    """Determines the type of hand.

    :param hand: a 2D array, 5x2, with a single hand
    :param card_counts: list of tupes with pip values and frequency counts
    :return: encodedhand type values
    Leverages straight() and flush() functions
    Also leverage count of most frequently occurring pip value in card_counts
    """
    unique_vals = len(card_counts)
    # If there are five unique card values, then it is one of straight, flush, straight flush, or just high card
    if unique_vals == 5:
        if straight_flush(hand):
            return HAND_TYPE_VALS['Straight Flush']
        elif flush(hand):
            return HAND_TYPE_VALS['Flush']
        elif straight(hand):
            return HAND_TYPE_VALS['Straight']
        else:
            return HAND_TYPE_VALS['High Card']
    # If there are four unique card values, it can only be one pair
    elif unique_vals == 4:
        return HAND_TYPE_VALS['One Pair']
    # If there are three unique card values, then either it's three of a kind or two pair
    elif unique_vals == 3:
        # If most frequent unique value occurs three times, then it's three of a kind
        if card_counts[0][1] == 3:
            return HAND_TYPE_VALS['3 Kind']
        else:
            return HAND_TYPE_VALS['Two Pair']
    # If there are two unique card values, it is four of a kind or a full house (three and two of a kind)
    elif unique_vals == 2:
        # If most frequent unique value occurs four times, then it's four of a kind
        if card_counts[0][1] == 4:
            return HAND_TYPE_VALS['4 Kind']
        else:
            return HAND_TYPE_VALS['Full House']
    # Without wild cards you cannot have five of a kind
    else:
        print("Bad value for number of unique values", unique_vals)


def two_pair_tie_breaker(counts_card1, counts_card2):
    """Determine the winner when both hands have two pair. It's complicated enough to need its own function.

    :param counts_card1: list of tupes with pip values and frequency counts for hand1
    :param counts_card2: list of tupes with pip values and frequency counts for hand2
    :return: number of winning hand
    """
    # Check to see who has the highest two pair
    if counts_card1[0][0] > counts_card2[0][0]:
        return 1
    elif counts_card2[0][0] > counts_card1[0][0]:
        return 2
    # Top pair is equal. Check second pair
    elif counts_card1[1][0] > counts_card2[1][0]:
        return 1
    elif counts_card2[1][0] > counts_card1[1][0]:
        return 2
    # Both pair are equal. Check fifth card (third in count array)
    elif counts_card1[2][0] > counts_card2[2][0]:
        return 1
    elif counts_card2[2][0] > counts_card1[2][0]:
        return 2
    else:
        print("All cards match in two pairs. Illegal input")
        return -1


def one_pair_tie_breaker(hand1, hand2, counts_card1, counts_card2):
    """Determine the winner when both hands have one pair. It's complicated enough to need its own function.

    :param hand1: a 2D array, 5x2, for hand1
    :param hand2: a 2D array, 5x2, for hand2
    :param counts_card1: list of tupes with pip values and frequency counts for hand1
    :param counts_card2: list of tupes with pip values and frequency counts for hand2
    :return: number of winning hand
    """

    # Compare the value of the pair and return identity of higher value, if not the same
    if counts_card1[0][0] > counts_card2[0][0]:
        return 1
    elif counts_card2[0][0] > counts_card1[0][0]:
        return 2
    # Pair has same value, check highest of each hand one by one until mismatch
    else:
        for i in range(0, 5):
            if hand1[i][0] > hand2[i][0]:
                return 1
            elif hand2[i][0] > hand1[i][0]:
                return 2
        # All cards equal
        print("All cards equal. Illegal input")
        return -1


# Determining the winner when just high card has enough steps to needs its own function
def high_card_tie_breaker(hand1, hand2):
    """Determine the winner when just high card. Has enought steps to need its own funtion.

    :param hand1: a 2D array, 5x2, for hand1
    :param hand2: a 2D array, 5x2, for hand2
    :return: number of winning hand
    """

    for i in range(0, 5):
        if hand1[i][0] > hand2[i][0]:
            return 1
        elif hand2[i][0] > hand1[i][0]:
            return 2
    # All cards equal
    print("All cards equal. Illegal input")
    return -1


# Hand type is the same for both hands. Determine who wins via tie breaker routines
# Params: hand type, hand1 and hand2 (2D array), and sorted card count array for hand1 and hand2
def tie_breaker(type_of_hand, hand1, hand2, counts_card1, counts_card2):
    """Hand type is the same for both hands. Determines winner via various tie-breaker mechanisms.

    :param type_of_hand:
    :param hand1: a 2D array, 5x2, for hand1
    :param hand2: a 2D array, 5x2, for hand2
    :param counts_card1: list of tupes with pip values and frequency counts for hand1
    :param counts_card2: list of tupes with pip values and frequency counts for hand2
    :return: number of winning hand
    Makes use of hand type codes (HAND_TYPE_VALS) to classify solution
    """

    # If the hand is a flush, straight, or straight flush
    if type_of_hand == 9 or type_of_hand == 6 or type_of_hand == 5:
        # Can determine by comparing the highest card in each hand
        if hand1[0][0] > hand2[0][0]:
            print("Hand1 wins")
            return 1
        elif hand2[0][0] > hand1[0][0]:
            return 2
        else:
            print("Tie in hands - bad data")
            return -1

    # Hand is four of a kind
    elif type_of_hand == 8:
        # Card values in a four of a kind are unique. Just compare them
        if counts_card1[0][0] > counts_card2[0][0]:
            return 1
        else:
            return 2

    # Hand is full house or three of kind
    elif type_of_hand == 4 or type_of_hand == 7:
        # Can determine winner by comparing value of three of a kind. Must be different.
        if counts_card1[0][0] > counts_card2[0][0]:
            return 1
        else:
            return 2
    # Two pair
    elif type_of_hand == 3:
        return two_pair_tie_breaker(counts_card1, counts_card2)
    # One pair
    elif type_of_hand == 2:
        return one_pair_tie_breaker(hand1, hand2, counts_card1, counts_card2)
    # High card
    elif type_of_hand == 1:
        return high_card_tie_breaker(hand1, hand2)
    else:
        print("Illegal hand type (over nine or less than one")
        return -1


def main():
    """Main loop for Project Euler problem #54

    Sets-up main data structures
    Reads each line in the file, and converts into data structure format
    Calculates how often each pip value appears in each hand
    Calculates type and compares to determine winner, or if tie breaker is needed
    """

    hand1_wins = 0
    # Create a two dimensional array for hand1 and hand2
    # One for suit, one for value for each of five cards in a hand
    # This will get reinitialized each time through the loop
    hand1 = [[0]*2 for _ in range(5)]
    hand2 = [[0]*2 for _ in range(5)]
    # Need a one dimensional array for the pip values of the cards in each hand
    hand1_vals = [0] * 5
    hand2_vals = [0] * 5
    # Each line is one pair of poker hands
    for line in open('poker.txt'):
        # Use rstrip() to get rid of \n at the end
        hands = line.rstrip().split(" ")
        # Convert each hand into numeric form
        for i in range(5):
            # Convert the text form of the pip values to numbers, two to 14
            hand1[i][0] = card_val_convert(hands[i][0])
            hand2[i][0] = card_val_convert(hands[i+5][0])
            # Convert values of cards into a one dimensional list
            hand1_vals[i] = hand1[i][0]
            hand2_vals[i] = hand2[i][0]
            # Convert card suit to numeric values, zero to three
            hand1[i][1] = card_suit_convert(hands[i][1])
            hand2[i][1] = card_suit_convert(hands[i+5][1])
        # Sort each hand into descending order
        hand1.sort(reverse=True)
        hand2.sort(reverse=True)

        # Figure out how often each pip value occurs in each hand, and order by most frequent occurence
        # Create a counter (hash table) that counts how many of each pip value in each hand
        cards1 = Counter()
        cards2 = Counter()
        for card_val in hand1_vals:
            # Increment count of hash table value for card values in hand1
            cards1[card_val] += 1
        for card_val in hand2_vals:
            # Increment count of hash table value for card values in hand2
            cards2[card_val] += 1
        # Convert the counter into a dictionary, and sort by the most common appearing,
        # pip value and return as a list
        counts_card1 = sorted(cards1.items(), key=itemgetter(1), reverse=True)
        counts_card2 = sorted(cards2.items(), key=itemgetter(1), reverse=True)
        hand1_type = hand_type(hand1, counts_card1)
        hand2_type = hand_type(hand2, counts_card2)
        print("Hand 1 type is", DEBUG_HAND_TYPE_STRING[hand1_type], "   "
              "Hand 2 type is", DEBUG_HAND_TYPE_STRING[hand2_type])

        # Determine the winning hand
        # If different types of hands, the higher encoding wins
        if hand1_type > hand2_type:
            print("Hand 1 wins")
            hand1_wins += 1
        elif hand1_type == hand2_type:
            # Hand types are the same. Call the tie breaking routine
            if tie_breaker(hand1_type, hand1, hand2, counts_card1, counts_card2) == 1:
                print("Hand 1 wins")
                hand1_wins += 1
    print("\nHand 1 wins", hand1_wins, "times.")


# Check for interactive session
if __name__ == '__main__':
    # execute main program
    main()
