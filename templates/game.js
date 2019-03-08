    var allBids = [[6, "Spades"], [6, "Clubs"], [6, "Diamonds"], [6, "Hearts"], [6, "notrump"], [7, "Spades"], [7, "Clubs"], [7, "Diamonds"], [7, "Hearts"], [7, "notrump"], [7, "nullo"], [8, "Spades"], [8, "Clubs"], [8, "Diamonds"], [8, "Hearts"], [8, "notrump"], [8, "opennullo"], [9, "Spades"], [9, "Clubs"], [9, "Diamonds"], [9, "Hearts"], [9, "notrump"], [10, "Spades"], [10, "Clubs"], [10, "Diamonds"], [10, "Hearts"], [10, "notrump"]];
    var pause_interval = false;

	function update_game() {
        console.log("Getting Game");
        $.get('/api/get_game_for_player', {"player_index": player_index}, function(game_data) {
            update_scoreboard(game_data.score1, game_data.score2)
            set_turn(game_data.turn, game_data.state);
            update_current_bid(game_data.current_bid_suit, game_data.current_bid_number, game_data.current_bid_player);
            // update last trick
            if (game_data.last_trick != "tricks are empty") {
                update_last_trick(game_data.last_trick[0], game_data.last_trick[1], game_data.last_trick[2], game_data.last_trick[3], game_data.last_trick[4], game_data.last_trick[5], game_data.last_trick[6], game_data.last_trick[7], game_data.last_trick[8], game_data.team1_tricks, game_data.team2_tricks)
            }
            if (game_data.state == 0){
                display_bidding_state(game_data);
                update_hand(game_data);
            }
            else if (game_data.state == 1) {
                display_blind_state(game_data);
            }
            else if (game_data.state == 2) {
                display_playing_state(game_data);
            }
            else if (game_data.state == 3) {
                // end game
                if (game_data.score1 > game_data.score2) {
                    $("#turnDisplayer").html("<div id='gameover'>The game is over and Team 1 wins</div>");
                } else {
                    $("#turnDisplayer").html("<div id='gameover'>The game is over and Team 2 wins</div>");
                }
            }
        });
    }

    function display_playing_state(game_data) {
        $("#biddingContainer").css("display", "none");
        $("#blindConainer").css("display", "none");
        $("#playingContainer").css("display", "block");

        // update playingContainer with cards that have been played
        update_playing_box(game_data.current_trick[0], game_data.current_trick[1], game_data.current_trick[2], game_data.current_trick[3], game_data.current_trick[4], game_data.current_trick[5], game_data.current_trick[6], game_data.current_trick[7])

        // if open nullo
        if (game_data.current_bid_suit === "opennullo" && game_data.current_bid_player_index != player_index) {
            display_open_nullo_cards(game_data);
        }

        if (game_data.turn == player_index) {
            // update hand with cards containing button on playable cards
            update_playable_hand(game_data);
            pause_interval = true;
        } else {
            // update hand with default cards
            update_hand(game_data);
        }
    }

    function display_open_nullo_cards(game_data) {
        console.log("displaying open nullo");
        index_of_nullo_bidder = game_data.current_bid_player_index;
        name_of_nullo_bidder = game_data.current_bid_player;
        $("#openNulloContainer").css("display", "block");
        $("#nulloLabel").html(name_of_nullo_bidder)
        $.get('/api/get_open_nullo_hand', {
            "bidder_index": index_of_nullo_bidder
        }, function (hand_data) {
        	$("#openNulloCardsContainer").html('');
            for (var i = 0; i < hand_data.hand.length; i+=2) {
                $("#openNulloCardsContainer").append(to_card_div(hand_data.hand[i], hand_data.hand[i + 1]));
            }
        });

    }

    function play_card(suit, value) {
        $.get('/api/play_card', {
            "player_index": player_index,
            "suit": suit,
            "value": value
        }, function(game_data) {
            // should be string: "played card" which is returned from Game.play_card(player_index, suit, value)
            console.log(game_data)
            update_game();
            pause_interval = false;
        });
    }

    function update_playable_hand(game_data) {
        $("#cardsContainer").html('');
        for (var i = 0; i < game_data.playable_hand.length; i+=3) {
            $("#cardsContainer").append(to_playable_card_div(game_data.playable_hand[i], game_data.playable_hand[i + 1], game_data.playable_hand[i + 2]));
        }
    }

    function to_playable_card_div(suit, value, playable) {
        var onclick_function = `onclick="alert('You cannot play this card')"`;
        var suit_color = "black";
        var playable_border = "";
        if (playable == 1) {
            onclick_function = `onclick='play_card("` + suit + `","` + value +`")'`;
            playable_border = "playable";
        }
        if (value === "Joker") {
            suit = '';
        } else if (suit === "Hearts") {
			suit = "&#9829;";
			suit_color = "red";
		} else if (suit === "Diamonds") {
			suit = "&#9830;";
			suit_color = "red";
		} else if (suit === "Spades") {
			suit = "&#9824;";
		} else if (suit === "Clubs") {
			suit = "&#9827;";
		}
		return `
		<div ` + onclick_function + ` class = "cardBox ` + playable_border + `">
			<span class="value">`
			+ value + `</span>
			<span class="suit ` + suit_color + `">` + suit + `</span>
		</div>
		`;
    }

    // display blind in content area with check boxes
    // display checkboxes under hand
    // display submit button -> onclick="get_blind_index_arrays_and_send_to_backend()"
    // submit button calls function that gets the arrays then passes those arrays to update_hand_with_blind(hand_indexs, blind_indexs)
    function display_blind_state(game_data) {
        $("#playingContainer").css("display", "none");
        $("#biddingContainer").css("display", "none");
        $("#blindConainer").css("display", "block");
        if (game_data.turn == player_index) {
            // display blind
            display_blind(game_data);
            update_hand_with_checkbox(game_data);
            pause_interval = true;
        } else {
            $("#blindConainer").html("The person who won the bid is integrating the blind into his hand");
            update_hand(game_data);
        }
    }

    function display_blind(game_data) {
        $("#blindConainer").html("");
        for (var i = 0; i < game_data.blind.length; i+=2) {
            var checked = "";
            if (game_data.blind[i] == game_data.current_bid_suit || (game_data.blind[i + 1] == "Joker" && game_data.current_bid_suit != "nullo" && game_data.current_bid_suit != "opennullo" ) || (opposite_suit(game_data.blind[i]) == game_data.current_bid_suit && game_data.blind[i + 1] == "J")) {
                checked = "checked='checked' disabled ";
            }
            $("#blindConainer").append(to_card_div_with_checkbox(game_data.blind[i], game_data.blind[i + 1], "blind", i / 2, checked))
        }
        $("#blindConainer").append("<input type='submit' onclick='get_blind_index_arrays_and_send_to_backend()'>");
        $("#blindConainer").append("<div id='blind-instructions'>Check the boxes from the blind you want to add to your hand. Check the boxes in the cards from your hand to discard. You must discard the same number of cards you add.<br> <center>You must add all trump cards to your hand.</center></div>")
    }

    function opposite_suit(suit) {
        if (suit == "Hearts") {
            return "Diamonds";
        } else if (suit == "Diamonds") {
            return "Hearts";
        } else if (suit == "Spades") {
            return "Clubs";
        } else if (suit == "Clubs") {
            return "Spades";
        } else {
            return "no opposite suit";
        }
    }

    function get_blind_index_arrays_and_send_to_backend() {
		var hand_index = [];
		var num_discard_from_hand = 0;
		var num_recieve_from_blind = 0;
		for (var i = 0; i < 10; i++) {
		    try {
		        if (document.getElementById('hand' + i).checked) {
    				hand_index.push(1);
    				num_discard_from_hand++;
    			} else {
    				hand_index.push(0);
    			}
		    } catch(err) {
		        throw "couldn't get id of: hand" + i;
		    }

		}
		var blind_index = [];
		for (var i = 0; i < 5; i++) {
			if (document.getElementById('blind' + i).checked) {
				blind_index.push(1);
				num_recieve_from_blind++;
			} else {
				blind_index.push(0);
			}
		}
		if (num_discard_from_hand != num_recieve_from_blind) {
			alert("Cannot discard more or less cards than you receive from blind");
		} else {
			update_hand_with_blind(hand_index, blind_index);
    		// updates game
    		update_game();
		}

	}

    // hand_indexs = [1, 0, 1, 0, 0, 1, 0, 1, 0, 0] where 1 mean they are to be switched out
    // blind_indexs = [1, 0, 1, 1, 1]
    function update_hand_with_blind(hand_indexs, blind_indexs) {
        $.get('/api/update_hand_with_blind', {
            "player_index": player_index,
            "h1": hand_indexs[0],
            "h2": hand_indexs[1],
            "h3": hand_indexs[2],
            "h4": hand_indexs[3],
            "h5": hand_indexs[4],
            "h6": hand_indexs[5],
            "h7": hand_indexs[6],
            "h8": hand_indexs[7],
            "h9": hand_indexs[8],
            "h10": hand_indexs[9],
            "b1": blind_indexs[0],
            "b2": blind_indexs[1],
            "b3": blind_indexs[2],
            "b4": blind_indexs[3],
            "b5": blind_indexs[4],
        }, function(game_data) {
           console.log(game_data);
           update_game();
           pause_interval = false;
        });
    }

    function update_current_bid(suit, number, player) {
        $("#bidNumber").html(number);
        $("#bidSuit").html(suit);
        $("#bidPlayer").html(player);
    }

    function display_bidding_state(game_data) {
        $("#playingContainer").css("display", "none");
        $("#blindConainer").css("display", "none");
        $("#biddingContainer").css("display", "block");
        update_bid_table(game_data.bids);
        if (game_data.turn == player_index) {
            // get minBidIndex
            minBidIndex = get_bid_index(game_data.current_bid_number, game_data.current_bid_suit, game_data.bids_this_round);
            display_bidding_form(minBidIndex + 1)
            pause_interval = true;
        } else {
            // hide biddding form
            $("#biddingFormContainer").html("");
        }

    }


    function update_hand(game_data) {
    	$("#cardsContainer").html('');
        for (var i = 0; i < game_data.playable_hand.length; i+=3) {
            $("#cardsContainer").append(to_card_div(game_data.playable_hand[i], game_data.playable_hand[i + 1]));
        }
    }
    function update_hand_with_checkbox(game_data) {
    	$("#cardsContainer").html('');
        for (var i = 0; i < game_data.playable_hand.length; i+=3) {
            $("#cardsContainer").append(to_card_div_with_checkbox(game_data.playable_hand[i], game_data.playable_hand[i + 1], "hand", i / 3, ""));
        }
    }

	function update_scoreboard(score1, score2) {
		$("#score1").html(score1);
		$("#score2").html(score2);
	}

	function update_bid_table(bids){
		var table_string = `
				<table>
					<tr>
					    <th>Number</th>
					    <th>Suit</th>
					    <th>Player</th>
					</tr>`
		for (var i = 0; i < bids.length; i+=3) {
			table_string = table_string + to_bid_table_row(bids[i], bids[i + 1], bids[i + 2]);
		}

		table_string = table_string + "</table>"

		$("#biddingTableContainer").html(table_string);
	}

	function to_bid_table_row(number, suit, player) {
        return '<tr><td>' + number + '</td><td>' + suit + '</td><td>' + player + '</td></tr>'
    }

    function display_bidding_form(minBidIndex) {
    	formString = `
    	<div id="biddingForm">
    	`
    	for (var i = minBidIndex; i < allBids.length; i++) {
    	    formString += "<label class='radio-container'>" + allBids[i][0] + " " + allBids[i][1]  + "<input name='bid' value='" + allBids[i][0] + " " + allBids[i][1] + "' type='radio'><span class='checkmark'></span></label>";
    	}
    	formString += `
    		<label class='radio-container'>Pass<input name='bid' type='radio' value='Pass' checked='checked'><span class='checkmark'></span></label></div>
    		<input onclick='send_bid()' id='biddingButton' type='submit' value="Submit Bid"></input></div>
    	`
    	$("#biddingFormContainer").html(formString);
    	$("#biddingButton").removeAttr("disabled");
    }


    function send_bid() {
        $("#biddingButton").attr("disabled", "disabled");
    	var radioValue = $("input[name='bid']:checked").val();
    	var parsed;
    	if (radioValue === "Pass") {

		    console.log("passing");
   			$.get('/api/add_bid', {
            	"bid_passed": "true",
            	"bid_suit": "",
            	"bid_number": "",
            	"bid_player_index": player_index
        	}, function(data1) {
        	    console.log(data1);
        	    update_game();
        	    pause_interval = false;
        	});
    	} else {
    		parsed = radioValue.split(" ");
    		$.get('/api/add_bid', {
            	"bid_passed": "false",
            	"bid_suit": parsed[1],
            	"bid_number": parsed[0],
            	"bid_player_index": player_index
        	}, function(data1) {
            	console.log(data1);
            	update_game();
        	    pause_interval = false;
        	});
    	}

    }

	function update_last_trick(s0, v0, s1, v1, s2, v2, s3, v3, lead, team1Tricks, team2Tricks) {
	    $(".trickLabel").css("display", "inline-block");
	    $(".trickLabelTop").css("display", "block");
		$("#trickBoxTwo").html(to_card_div(s2, v2));
		$("#trickBoxOne").html(to_card_div(s1, v1));
		$("#trickBoxThree").html(to_card_div(s3, v3));
		$("#trickBoxZero").html(to_card_div(s0, v0));
		if (lead == 0) {
			$("#trickBoxZero").css("background", "lightblue")
		} else {
		    $("#trickBoxZero").css("background", "transparent")
		}
		if (lead == 1) {
			$("#trickBoxOne").css("background", "lightblue")
		} else {
		    $("#trickBoxOne").css("background", "transparent")
		}
		if (lead == 2) {
			$("#trickBoxTwo").css("background", "lightblue")
		} else {
		    $("#trickBoxTwo").css("background", "transparent")
		}
	    if (lead == 3) {
			$("#trickBoxThree").css("background", "lightblue")
		} else {
		    $("#trickBoxThree").css("background", "transparent")
		}
		$("#t1Tricks").html(team1Tricks);
		$("#t2Tricks").html(team2Tricks);

	}

	function update_playing_box(s0, v0, s1, v1, s2, v2, s3, v3) {
		if (s0 != "" || v0 != "") {
			$("#playerBoxZero").html(to_card_div(s0, v0));
		} else {
			$("#playerBoxZero").html(to_card_div('&nbsp', '&nbsp'));
		}
		if (s1 != "" || v1 != "") {
			$("#playerBoxOne").html(to_card_div(s1, v1));
		} else {
			$("#playerBoxOne").html(to_card_div('&nbsp', '&nbsp'));
		}
		if (s2 != "" || v2 != "") {
			$("#playerBoxTwo").html(to_card_div(s2, v2));
		} else {
			$("#playerBoxTwo").html(to_card_div('&nbsp', '&nbsp'));
		}
		if (s3 != "" || v3 != "") {
			$("#playerBoxThree").html(to_card_div(s3, v3));
		} else {
			$("#playerBoxThree").html(to_card_div('&nbsp', '&nbsp'));
		}
	}

	function set_turn(turn, state) {
	    var state_string = "";
	    if (state == 0) {
	        state_string = " to bid"
	    } else if (state == 1) {
	        state_string = " to sort blind"
	    } else if (state == 2) {
	        state_string = " to play"
	    }
		if (turn == 0) {
			$("#playersTurn").html("Player 1" + state_string);
		} else if (turn == 1) {
			$("#playersTurn").html("Player 2" + state_string);
		} else if (turn == 2) {
			$("#playersTurn").html("Player 3" + state_string);
		} else if (turn == 3) {
			$("#playersTurn").html("Player 4" + state_string);
		}
	}

	function to_card_div(suit, value) {
	    var suit_color = "black";
        if (value === "Joker") {
            suit = '';
        } else if (suit === "Hearts") {
			suit = "&#9829;";
			suit_color = "red";
		} else if (suit === "Diamonds") {
			suit = "&#9830;";
			suit_color = "red";
		} else if (suit === "Spades") {
			suit = "&#9824;";
		} else if (suit === "Clubs") {
			suit = "&#9827;";
		}
		return `
		<div class = "cardBox">
			<span class="value">`
			+ value + `</span>
			<span class="suit ` + suit_color + `">` + suit + `</span>
		</div>
		`;
    }

    function to_card_div_with_checkbox(suit, value, hand_or_blind, i, checked) {
        suit_color = "black";
        if (value === "Joker") {
            suit = '';
        } else if (suit === "Hearts") {
			suit = "&#9829;";
			suit_color = "red";
		} else if (suit === "Diamonds") {
			suit = "&#9830;";
			suit_color = "red";
		} else if (suit === "Spades") {
			suit = "&#9824;";
		} else if (suit === "Clubs") {
			suit = "&#9827;";
		}
		return `
		<label class = "cardBox">
			<span class="value">`
			+ value + `</span>
			<span class="suit ` + suit_color + `">` + suit + `</span>
			<br>
			<input ` + checked + ` type="checkbox" id="` + hand_or_blind + i +`">
		</label>
		`;
    }

    function get_bid_index(number, suit, bidPosition) {
        var ret = -1;
        for (var i = 0 ; i < allBids.length; i++) {
            if (allBids[i][0] == number && allBids[i][1] == suit) {
                ret = i;
            }
        }
        if(bidPosition >= 2 && ret < 4) {
            ret = 4;
        }
        return ret;
    }

    // setInterval(update_game(), 3000);
    setInterval(function() {
        if (!pause_interval) {
            update_game();
        }
    }, 1000);