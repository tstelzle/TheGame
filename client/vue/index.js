var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!',
        ip: "localhost",
        port: "5050",
        website: "ServerConnect",
        game_name: "",
        game_uid: "",
        player_name: "",
        player_id: "",
        players: {},
        game_state: false,
        my_turn: false,
    },
    computed: {},
    methods: {
        changeWebsite(newValue) {
            if (newValue === "Lobby") {
                this.refresh()
            }
            this.website = newValue
        },
        is_current_player() {
            this.my_turn = setInterval(() => {
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
        get_api() {
            let path = Array.from(arguments).join("/")
            return fetch("http://" + this.ip + ":" + this.port + "/" + path)
                .then(response => response.json())
                .then(responseData => {
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
                    return responseData
                });
        }
    },
    created() {
        this.is_current_player()
    }
})