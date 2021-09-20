var app = new Vue({
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
        players: {},
        game_state: false,
        my_turn: false,
        handcards: {},
        topcards: {},
        selected_card: "",
        selected_pile: 0,
        win_state: ""
    },
    computed: {},
    methods: {
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
                players: {},
                game_state: false,
                my_turn: false,
                handcards: {},
                topcards: {},
                selected_card: "",
                selected_pile: 0,
                win_state: ""
            }
        },
        get_pile_direction(id) {
            if (id === 0 || id === 1) {
                return "1 -> 100"
            }
            return "100 -> 1"
        },
        changeWebsite(newValue) {
            if (newValue === "Lobby") {
                this.refresh()
            }
            if (this.win_state === "loss" || this.win_state === "win") {
                Object.assign(this.$data, this.initiale_state());
            }
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
        refresh() {
            this.get_players()
            this.get_game_state().then(() => {
                if (this.game_state === true) {
                    this.changeWebsite("Game")
                }
            })
        },
        add_player() {
            this.post_api("player", this.game_uid, this.player_name).then(response => {
                this.player_id = response["data"]
                this.changeWebsite("Lobby")
            })
        },
        get_players() {
            this.get_api("players", this.game_uid).then(response => {
                this.players = response["data"]
            })
        },
        get_game_state() {
            return this.get_api("game", "state", this.game_uid).then(response => {
                    this.game_state = response["data"] === "True";
                    return this.game_state
                }
            )
        },
        start_game() {
            this.post_api("game", "state", this.game_uid).then(response => {
                this.game_state = true
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
                if (this.game_state === true) {
                    this.get_api("player", this.game_uid, this.player_id).then(response => {
                        this.handcards = response["data"]
                    })
                }
            }, 2000)
        },
        get_topcards() {
            setInterval(() => {
                if (this.game_state === true) {
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
                    if (this.game_state === Boolean(true)) {
                        this.changeWebsite("Game")
                    }
                    else {
                        this.changeWebsite("Lobby")
                    }
                }
                else {
                    window.alert("Player UID Does Not Exist.")
                }
            })
        },
        play_card() {
            this.post_api("game", this.game_uid, this.player_id, this.selected_pile-1, this.selected_card).then(response => {
                if (response.isError === Boolean(false)) {
                    this.handcards = this.handcards.filter(function(value, index, arr){
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
        check_win() {
            setInterval(() => {
                if (this.game_state === true) {
                    this.get_api("game", "win", this.game_uid).then(response => {
                        console.log(response["data"])
                        console.log(typeof(response["data"]))
                        this.win_state = response["data"]
                        if (this.win_state === "loss") {
                            this.changeWebsite("Loss")
                        }
                        else if(this.win_state === "win") {
                            this.changeWebsite("Win")
                        }
                    })
                }
            }, 2000)
        },
        surrender() {
            this.post_api("game", "win", this.game_uid, "loss")
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
        this.check_win()
    }
})