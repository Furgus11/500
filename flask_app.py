from flask import Flask, render_template, jsonify, request
import classes

app = Flask(__name__)

global_game = classes.Game()

chat = classes.Chat()

reloads = ["false", "false", "false", "false"]

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)

@app.route('/api/update_hand_with_blind', methods=['GET'])
def update_hand_with_blind():
    # h1, h2, h3 are either 0 or 1
    # for each in h, if = 1 append index to hi
    player_index = int(request.args.get("player_index"))
    h = [request.args.get("h1"), request.args.get("h2"), request.args.get("h3"), request.args.get("h4"), request.args.get("h5"), request.args.get("h6"), request.args.get("h7"), request.args.get("h8"), request.args.get("h9"), request.args.get("h10")]
    b = [request.args.get("b1"), request.args.get("b2"), request.args.get("b3"), request.args.get("b4"), request.args.get("b5")]
    hi = []
    i = 0
    for each in h:
        if each == "1":
            hi.append(i)
        i += 1
    bi = []
    i = 0
    for each in b:
        if each == "1":
            bi.append(i)
        i += 1
    global global_game
    global_game.players[player_index].hand = global_game.update_hand_with_blind(global_game.players[player_index].hand, hi, bi)
    return "updated blind"

@app.route('/api/play_card')
def play_card():
    player_index = int(request.args.get("player_index"))
    suit = request.args.get("suit")
    value = request.args.get("value")
    return global_game.play_card(player_index, suit, value)

@app.route('/api/get_game_for_player')
def get_game_p1():
    player_index = int(request.args.get("player_index"))
    rl = "false"
    global reloads
    if reloads[player_index] == "true":
        reloads[player_index] = "false"
        rl = "true"

    return jsonify(current_trick = global_game.current_trick_to_array(), last_trick = global_game.last_trick_to_array(), team1_tricks = global_game.get_num_tricks(1), team2_tricks = global_game.get_num_tricks(2), playable_hand = global_game.hand_to_array(player_index, 1), blind = global_game.blind_to_array(), score1 = global_game.scoreboard.team1, score2 = global_game.scoreboard.team2, bids=global_game.bids_to_array(), turn=global_game.turn, state=global_game.state, current_bid_suit = global_game.current_bid.suit, current_bid_number = global_game.current_bid.number, current_bid_player = global_game.current_bid.bidder.name, current_bid_player_index = global_game.current_bid.bidder.index, bids_this_round = len(global_game.bids), player1_name = global_game.players[0].name, player2_name = global_game.players[1].name, player3_name = global_game.players[2].name, player4_name = global_game.players[3].name, rload=rl)

@app.route('/api/set_reload')
def set_reload():
    ri = int(request.args.get("index"))
    global reloads
    reloads[ri]  = "true"
    return "set"

@app.route('/api/get_names')
def get_names():
    return jsonify(player1_name = global_game.players[0].name, player2_name = global_game.players[1].name, player3_name = global_game.players[2].name, player4_name = global_game.players[3].name)

@app.route('/api/get_reload')
def get_reload():
    player_index = int(request.args.get("player_index"))
    rl = "false"
    global reloads
    if reloads[player_index] == "true":
        reloads[player_index] = "false"
        rl = "true"
    return jsonify(rload=rl)

@app.route('/api/add_bid')
def add_bid():
    bid_number = request.args.get("bid_number")
    bid_suit = request.args.get("bid_suit")
    bid_player_index = request.args.get("bid_player_index")
    bid_passed = request.args.get("bid_passed")
    global global_game
    s = global_game.addBid(bid_passed, bid_suit, bid_number, bid_player_index)
    return s

@app.route('/api/get_open_nullo_hand')
def get_opennullo_hand():
    bidder_index = int(request.args.get("bidder_index"))
    global global_game
    global_game.players[bidder_index].hand.sort(key=lambda x: x.sorting_value())
    return jsonify(hand = global_game.hand_to_array(bidder_index, 0))

@app.route('/api/newGame', methods=['GET'])
def reset_global_game():
    names = []
    names.append(request.args.get("name1"))
    names.append(request.args.get("name2"))
    names.append(request.args.get("name3"))
    names.append(request.args.get("name4"))
    global global_game
    global_game = classes.Game()
    global_game.set_player_names(names)
    return "a new game has started"

@app.route('/api/send_chat')
def send_chat():
    message = request.args.get("message")
    name = request.args.get("name")
    global chat
    chat.add(message, name)
    return "Sent chat"

@app.route('/api/get_chat')
def get_chat():
    return jsonify(messages = chat.get_messages())

@app.route('/api/clear_chat')
def clear_chat():
    global chat
    chat.clear()
    return "chat cleared"

@app.route('/api/new_hand')
def new_hand():
    global global_game
    global_game.new_hand()
    return "new hand"