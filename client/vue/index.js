// register modal component
Vue.component("modal", {
    template: "#modal-template"
});

new Vue({
    el: '#app',
    data: {
        ip: "localhost",
        port: "5050",
        website: "ServerConnect",
        game_name: "",
        game_uid: "",
        player_name: "",
        player_id: "",
        possible_player_id: "",
        players: [],
        current_player: 0,
        game_state: "init",
        my_turn: false,
        handcards: [],
        topcards: [],
        selected_card: "",
        selected_pile: "",
        cards_in_deck: 0,
        show_instructions: false,
        game_log: [],
        show_log: false,
        show_chat: false,
    },
    computed: {},
    methods: {
        isButtonOrange(card) {
            return this.selected_card === card;
        },
        isPileOrange(pile) {
            return this.selected_pile === pile
        },
        initiale_state() {
            return {
                ip: "localhost",
                port: "5050",
                website: "ServerConnect",
                game_name: "",
                game_uid: "",
                player_name: "",
                player_id: "",
                possible_player_id: "",
                players: [],
                current_player: 0,
                game_state: "init",
                my_turn: false,
                handcards: [],
                topcards: [],
                selected_card: "",
                selected_pile: "",
                cards_in_deck: 0,
                show_instructions: false,
                game_log: [],
            }
        },
        get_game_log() {
            setInterval(() => {
                if (this.game_uid) {
                    this.get_api("game", "log", this.game_uid, this.game_log.length).then(response => {
                        if (response.data !== "") {
                            this.game_log = this.game_log.concat(response.data.split(";"))
                        }
                    })
                }
            }, 2000)
        },
        select_pile(pile) {
            this.selected_pile = pile
        },
        select_handcard(card) {
            this.selected_card = card
        },
        get_pile_direction(id) {
            if (id === 0 || id === 1) {
                return "1 -> 100"
            }
            return "100 -> 1"
        },
        new_game() {
            Object.assign(this.$data, this.initiale_state());
            this.website = "Setup"
        },
        changeWebsite(newValue) {
            this.website = newValue
        },
        is_current_player() {
            setInterval(() => {
                if (this.player_id) {
                    this.get_api("game", "currentPlayer", this.game_uid).then(response => {
                        this.my_turn = response["data"] === this.player_id
                    })
                }
            }, 2000)
        },
        add_player() {
            this.post_api("player", this.game_uid, this.player_name).then(response => {
                this.player_id = response["data"]
                this.changeWebsite("Lobby")
            })
        },
        get_players() {
            setInterval(() => {
                if (this.game_uid) {
                    this.get_api("players", this.game_uid).then(response => {
                        this.players = response["data"][0]
                        this.current_player = response["data"][1]
                    })
                }
            }, 2000)
        },
        start_game() {
            this.post_api("game", "state", this.game_uid, "in_game").then(response => {
                // this.game_state = "in_game"
                this.changeWebsite("Game")
            })
        },
        create_game() {
            this.post_api("game", this.game_name).then(response => {
                    this.game_uid = response["data"]
                    this.changeWebsite("PlayerSetup")
                }
            );
        },
        get_game() {
            this.get_api("game", this.game_uid).then(response => {
                this.game_name = response["data"]
                this.changeWebsite("PlayerSetup")
            })
        },
        get_handcards() {
            setInterval(() => {
                if (this.game_state === "in_game") {
                    this.get_api("player", this.game_uid, this.player_id).then(response => {
                        this.handcards = response["data"]
                    })
                }
            }, 2000)
        },
        get_topcards() {
            setInterval(() => {
                if (this.game_state === "in_game") {
                    this.get_api("player", "piles", this.game_uid).then(response => {
                        this.topcards = response["data"]
                    })
                }
            }, 2000)
        },
        restore_player() {
            this.get_api("player", "valid", this.game_uid, this.possible_player_id).then(response => {
                if (response.isError === Boolean(false)) {
                    this.player_id = this.possible_player_id
                    if (this.game_state === "in_game") {
                        this.changeWebsite("Game")
                    } else {
                        this.changeWebsite("Lobby")
                    }
                } else {
                    window.alert("Player UID Does Not Exist.")
                }
            })
        },
        play_card() {
            this.post_api("game", this.game_uid, this.player_id, this.selected_pile, this.selected_card).then(response => {
                if (response.isError === Boolean(false)) {
                    this.handcards = this.handcards.filter(function (value, index, arr) {
                        return value !== this.selected_card;
                    });
                }
            })
        },
        end_turn() {
            this.post_api("game", this.game_uid, this.player_id).then(response => {
                if (response.statusCode === 400) {
                    window.alert("You have to play more cards!")
                }
            })
        },
        get_game_state() {
            setInterval(() => {
                if (this.game_uid) {
                    this.get_api("game", "state", this.game_uid).then(response => {
                        this.game_state = response["data"]
                        if (this.game_state === "loss") {
                            this.changeWebsite("Loss")
                        } else if (this.game_state === "win") {
                            this.changeWebsite("Win")
                        }
                    })
                }
            }, 2000)
        },
        surrender() {
            // TODO Reset Values for stopping api calls
            this.post_api("game", "state", this.game_uid, "loss")
        },
        update_deck_cards() {
            setInterval(() => {
                if (this.game_uid) {
                    this.get_api("game", "deck", this.game_uid).then(response => {
                        this.cards_in_deck = response["data"]
                    })
                }
            }, 2000)
        },
        get_api() {
            let path = Array.from(arguments).join("/")
            return fetch("http://" + this.ip + ":" + this.port + "/" + path)
                .then(response => response.json())
                .then(responseData => {
                    if (responseData.statusCode === 401) {
                        Object.assign(this.$data, this.initiale_state());
                    }
                    return responseData
                });
        },
        post_api() {
            let path = Array.from(arguments).join("/")
            return fetch("http://" + this.ip + ":" + this.port + "/" + path, {
                method: "POST"
            })
                .then(response => response.json())
                .then(responseData => {
                    if (responseData.statusCode === 401) {
                        Object.assign(this.$data, this.initiale_state());
                    }
                    return responseData
                });
        }
    },
    created() {
        this.is_current_player()
        this.get_handcards()
        this.get_topcards()
        this.get_game_state()
        this.update_deck_cards()
        this.get_players()
        this.get_game_log()
    }
})