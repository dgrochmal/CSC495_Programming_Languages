from starterpack import *
from random import shuffle

# Standard Deck
suits = ['hearts', 'diamonds', 'spades', 'clubs']
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
deck = [Card(value, suit) for value in values for suit in suits]

# STATE_PLAYERS, STATE_CURRENT_STATE, STATE_DECK
STATE_TURN = "turns"
STATE_HEARTS = "hearts"
STATE_HEARTS_BROKEN = "broken"
STATE_PLAYED_CARDS = "played"
PLAYER_STATE_SCORE = "score"

# helper functions
def get_highest_score(players):
    score = -1
    for p in players:
        if p[PLAYER_STATE_SCORE] > score:
            score = p.state[PLAYER_STATE_SCORE]
    return score


pass3s = {"1" : [], "2" : [], "3" : [], "4" : []}
# move functions
def pass3(player, state, input):
    num = player.number
    crds = ("card 1", "card 2", "card 3")
    #input should be already checked for validity before this point
    for i in range(3):
        str = input[crds[i]]
        c = getCard(str)
        index = -1
        for j in range(len(player.hand)):
            if player.hand[j] == c:
                index = j
        c = player.hand.pop(index)
        if num == 1:
            state['pass3s']['1'].append(c)
        elif num == 2:
            state['pass3s']['2'].append(c)
        elif num == 3:
            state['pass3s']['3'].append(c)
        elif num == 4:
            state['pass3s']['4'].append(c)
        c = None
    return ""
    #return "pass"

def play(player, state, input):
    return ""


def placeholder(player, state, input):
    return ""

played = ["", "", "", ""]
# transition logic
def play(player, state, input):
    num = player.number
    str = input['card']
    c = getCard(str)
    state['played'][num-1] = str
    for j in range(len(player.hand)):
        if player.hand[j] == c:
            index = j
    c = player.hand.pop(index)
    #playlogic
    return ""


def placeholder(player, state, input):
    return ""


def transition_stub(game):
    pass


# move objects
pass3_move = Move("pass3", pass3, {"card 1": None, "card 2": None, "card 3": None})
play_move = Move("play", play, {"card": None})
placeholder_move = Move("placeholder", placeholder, {})

# transitions - happen by name
start_to_main = Transition("main", (lambda state: state[STATE_TURN] == 1), transition_stub)
main_to_broken = Transition("broken", (lambda state: state[STATE_HEARTS] == STATE_HEARTS_BROKEN), transition_stub)
broken_to_start = Transition("main", (lambda state: len(state[STATE_DECK]) == 0), transition_stub)
broken_to_finish = Transition("main", (lambda state: get_highest_score(state[STATE_PLAYERS]) >= 100), transition_stub)


def game_status(player, state):
    print("\nTurn " + str(state[STATE_TURN]))
    print("Showing %s info about the game." % (player.name))
    print(player.hand)
    printBoard(state)
    print()  # separator line

def printBoard(state):
    filler(state)
    print("-----------------")
    print("|      %d %s       |" % (state['players'][0].score, state['players'][0].name[0]))
    print("|       %s     %d|" % (state['played'][0], state['players'][1].score))
    print("|%s %s       %s %s|" % (state['players'][3].name[0], state['played'][3], state['played'][1], state['players'][1].name[0]))
    print("|%d      %s      |" % (state['players'][3].score, state['played'][2]))
    print("|       %s %d     |" % (state['players'][2].name[0], state['players'][2].score))
    print("-----------------")

#Filler for grid to maintain formatting if a player hasnt played yet
def filler(state):
    for i in range(4):
        if(len(state['played'][i]) != 2):
            state['played'][i] = "  "

    # % (state[0][0][0])

def scorehand(state):
    for i in range(4):
        num = state['players'][i].number
        s = 0
        #lst = the players accumulated card list from the previous hand
        for j in range(len(lst)):
            if lst[j].suit == "hearts":
                s = s + 1
            if lst[j].suit == "spades" and lst[j].value == "queen":
                s = s + 13
        if s == 26:
            for t in range(4):
                state['players'][t].score = state['players'][t].score + 26
            if num == 1:
                state['players'][0].score = state['players'][0].score - 26
            elif num == 2:
                state['players'][1].score = state['players'][1].score - 26
            elif num == 3:
                state['players'][2].score = state['players'][2].score - 26
            elif num == 4:
                state['players'][3].score = state['players'][3].score - 26
        else:
            state['players'][i].score = state['players'][i].score + s
# states
broken_transitions = [broken_to_start, broken_to_finish]
broken_moves = [play_move]
broken = State("broken", broken_transitions, broken_moves, game_status, False)

main_transitions = [main_to_broken]
main_moves = [play_move]
main = State("main", main_transitions, main_moves, game_status, False)

start_transitions = [start_to_main]
start_moves = [pass3_move]
start = State("start", start_transitions, start_moves, game_status, False)

finish = State("finish", None, [placeholder_move], game_status, True)

states = [start, main, broken, finish]

# players
players = []
for i in range(1, 5):
    name = input("What is the name of player " + str(i) + "? ")
    hand = []
    accum = []
    player = Player(name, {}, i, hand, 0, accum)
    players.append(player)


def deal(game, deck):
    players[0].hand.extend(deck[0:13])
    sortCards(players[0].hand)
    players[1].hand.extend(deck[13:26])
    sortCards(players[1].hand)
    players[2].hand.extend(deck[26:39])
    sortCards(players[2].hand)
    players[3].hand.extend(deck[39:52])
    sortCards(players[3].hand)

def sortCards(lst):
    lst.sort(key=lambda x: x.value, reverse=True)
    lst.sort(key=lambda x: x.suit, reverse=True)


def setup(game):
    shuffle(deck)
    shuffle(deck)
    shuffle(deck)
    deal(game, deck)
    game.game_state[STATE_CURRENT_STATE] = start
    print("Starting Hearts!\n")


def finish(game):
    print("Finished playing :)")


hearts = Game(players, {}, states, setup, finish, pass3s, played)
hearts.start()
