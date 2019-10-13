# -*- coding: utf-8 -*-
"""
Created on Sat Apr 6 23:14:16 2019

@author: Breeana

---Counting The Shuffles To Take A Deck Back To Its Original Position---

The properties of perfect shuffling lead to interesting patterns which we can
exploit to obtain a fast solution to how many shuffles are required before
returning to its original state. The naive approach is to simply instantiate
the state of a deck as a list with elements as cards, and to simulate shuffling
by moving elements as you would cards in a shuffle. For large decks, and even
moderately sized decks, this method proves too resource intensive.

Among the first important patterns I derived from the deck is that every card
returns to its original position in the deck at regular intervals. To simplify,
I refer to the amount of shuffles it takes for a card to return to its original
state as its frequency.

Another interesting pattern emerges when analyzing the various frequencies
cards have as they are shuffled. Cards through the process of perfect shuffling
rarely have distinct frequencies when compared with other cards. For example,
one card may have a frequency of 20 shuffles per cycle before returning to its
original state, while another may have another frequency, but it is rarely the
only card to have a frequency of 20. To make this point clear, this script
prints the unique frequencies of all relevant cards.

To reduce the amount of resources used, I spent some time determining whether
I could reduce the problem size in any way. This is what led me to the
discovery that within the entire set of cards there is only one pattern that
occurs at the beginning and end of shuffling. The order of cards in the top
portion of the deck has a certain order to begin with - for example the values
on those cards could be 8, 9, 10, 11, and 12 if the deck size is twelves cards
and the cut size is five cards. That order only occurs twice during shuffling;
once before we start shuffling and once at the end of shuffling. With a hard
rule such as that, the size of the problem is reduced from the full size of the
deck to the size of the cut.

In order to avoid simulating the shuffling of cards through the deck, I found
that all cards follow a specific step pattern when in certain potions of the
deck. There were three zones of movement - the bottom zone which will be
shuffled, the top zone which will be cut, and the middle zone which represents
all cards not in the first two zones. Within the bottom zone, all cards move
up the deck at two times their original position plus one. They experience an
exponential increase in position. Within the middle zone, cards are simply
pushed up by the number of cards added to the bottom - the number given by the
cut. In the top zone, all cards move to an even number position at the bottom
of the deck according to their position at the top. A card on the bottom of the
cut moves to position 0, the one above it moves to position 2, and so on.

With the movement of cards established, I can keep track of how many shuffles
it takes for a cards to return to its original position - its frequency. With
a reduced sample size, I can track the frequencies of only the top portion
of the deck where the cut was made. When the list of frequencies is complete -
which is to say that each card number in the cut portion has been tracked at
least one cycle through the deck - I can use all the unique frequencies of those
cards and find their least common multiple; it turns out that when you find the
LCM you get the number of shuffles it would take for all those cards to return to
the same state they were when the shuffling begin. With the understanding that
the top portion of the deck can only be in its original state when the entire
deck is also in its original state, I determined that the number of shuffles
required to fully shuffle the deck to its original state is equal to that least
common multiple.

In the special case when a cut is made that is larger than half the size of the
deck, there exists a portion of the deck that does not move at all. The problem
size can be reduced in this case by eliminating the cards that do not move and
altering the given cut size and deck size to reflect only the moving portions
of the deck. For example, when you have a deck of 6 cards and shuffle a cut of
4 cards, only the bottom two cards of the cut can be shuffled. Therefore the
new cut size would be 2 cards, and the new deck size would 4 cards.

This exact formula for determining the new cut size is equal to the original
deck size minus the original cut size - in other words it is the number of
cards not included in the original cut. This is intuitively true because, on
analysis, if the cut size is larger than half the deck then the number of cards
that can be shuffled in the cut is determined by the bottom portion. The total
deck size is found by doubling the cut size. Again this is intuitive since we
have the bottom cards as well as a true cut of equal size.

All of these things together make for an algorithm which runs much more quickly
than if I were to shuffle the entire deck in a simulation. The number of
shuffles the algorithm needs to perform to the original top cut of the deck is
typically in the hundreds for very long problems where the number of shuffles
required for such a deck could be in the billions.
"""

from math import gcd

print("\n\n\n\n")

print("\n----------------------------------------\n")
print("Welcome to the shuffle counter.")
print("\n----------------------------------------\n")

print("\n\n")

print("Please select a deck size: ")
while(True):
	try:
		size = int(input())
	except ValueError:
		print("\nPlease enter integer values for a deck size: ")
		continue
	except:
		exit()
	if(size < 2):
		print("\nPlease enter a value greater than 1 for a deck size: ")
		continue
	break

print("\n--------\n")

print("Please select a cut size less than the deck size to shuffle with: ")
while(True):
	try:
		cut = int(input())
	except ValueError:
		print("\nPlease enter integer values for a cut size: ")
		continue
	except:
		exit()
	if(cut < 1):
		print("\nPlease enter a value greater than 0 for a cut size: ")
		continue
	if(cut >= size):
		print("\nPlease enter a value less than the size of the deck for a cut size: ")
		continue
	if(cut > size/2):
		cut = size - cut
		sizeDiff = size - cut*2
		size = cut*2
	break

print("\n--------\n")

lowerLimit = size-cut
upperLimit = size
currentPosition = size-cut
previousFrequency = 0
frequencies = set([]);

	
#Move each card in the original cut through the deck according to its zone
for i in range(lowerLimit,upperLimit):
	cardFrequency = 0
	currentPosition = i
	if((i - lowerLimit)%100 == 0):
		print("Finished with " + str(i-lowerLimit) + " of " + str(cut) + " cards\r")
	while(True):
		if(currentPosition >= lowerLimit and currentPosition <= upperLimit):
			currentPosition = 2*(currentPosition-lowerLimit)
		elif(currentPosition < lowerLimit and currentPosition >= cut):
			currentPosition += cut
		elif(currentPosition < cut):
			currentPosition = currentPosition*2+1
		cardFrequency += 1
		#If the card has returned to its original position, add the frequency
		#retain only if unique
		if(currentPosition == i):
			frequencies.add(cardFrequency)
			break

print("Finished with " + str(cut) + " of " + str(cut) + " cards\r")

frequencies = list(frequencies)
LCM = frequencies[0]

#Get the least common multiplier for all in the frequency list
for i in frequencies[1:]:
	LCM = int(LCM*i/gcd(LCM,i))

print("\n\nShuffles required to return to original state: " + str(LCM))
print("\n")

print("Unique Frequency list: ")
print(frequencies)
