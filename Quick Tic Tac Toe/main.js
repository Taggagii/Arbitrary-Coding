

var screen = document.getElementById("screen");
var context = screen.getContext("2d");

console.log("good")

let size = Math.min(window.innerHeight, window.innerWidth) - 100;
let tileSize = size / 3;

let XCODE = 1;
let OCODE = 2;

let TYPEROW = 0;
let TYPECOL = 1;
let TYPEDIAG = 2;

var game_running = true;

var current_symbol = XCODE;

var board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

screen.width = size;
screen.height = size;

function render_grid() {
    context.beginPath()
    context.strokeStyle = "black";
    context.lineWidth = 1;
    for (var i = 0; i < size; i += tileSize) {
        context.moveTo(i, 0);
        context.lineTo(i, size);
        context.moveTo(0, i);
        context.lineTo(size, i);
    }
    context.stroke();
}
render_grid();

function render_x(x, y) {
    let posx = x * tileSize;
    let posy = y * tileSize;

    context.beginPath();
    context.lineWidth = 5;
    context.strokeStyle = "black";
    context.moveTo(posx, posy);
    context.lineTo(posx + tileSize, posy + tileSize);
    context.moveTo(posx + tileSize, posy);
    context.lineTo(posx, posy + tileSize);
    context.stroke();
}

function render_o(x, y) {
    let posx = x * tileSize;
    let posy = y * tileSize;
    context.strokeStyle = "black";
    context.lineWidth = 5;
    context.beginPath();
    context.arc(posx + tileSize / 2, posy + tileSize / 2, tileSize / 2, 0, 2 * Math.PI);
    context.stroke();
}

function render_board() {
    if (!game_running) return;
    for (var y = 0; y < 3; ++y) {
        for (var x = 0; x < 3; ++x) {
            if (board[y][x] == XCODE) {
                render_x(x, y);
            } else if (board[y][x] == OCODE) {
                render_o(x, y);
            } else {
                continue;
            }
        }
    }   
    check_win_condition();
    setTimeout(() => {
        render_board();
    }, 50);
}
render_board();

function check_win_condition() {
    game_running = false;
    let overstrokesize = 50;
    for (var i = 0; i < 3; ++i) {
        if (board[i][0] && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
            context.strokeStyle = "red";
            context.strokeWidth = overstrokesize;
            context.beginPath()
            context.moveTo(0, i * tileSize + tileSize / 2);
            context.lineTo(size, i * tileSize + tileSize / 2);
            context.stroke();
            return board[i][0];
        }
        if (board[0][i] && board[0][i] == board[1][i] && board[1][i] == board[2][i]) {
            context.strokeStyle = "red";
            context.strokeWidth = overstrokesize;
            context.beginPath()
            context.moveTo(i * tileSize + tileSize / 2, 0);
            context.lineTo(i * tileSize + tileSize / 2, size);
            context.stroke();
            return board[0][i];
        }
    }
    if (board[0][0] && board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
        console.log("this");
        context.strokeStyle = "red";
        context.strokeWidth = overstrokesize;
        context.beginPath()
        context.moveTo(0, 0);
        context.lineTo(size, size);
        context.stroke();
        return board[0][0];
    }
    if (board[0][2] && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
        context.strokeStyle = "red";
        context.strokeWidth = overstrokesize;
        context.beginPath()
        context.moveTo(size, 0);
        context.lineTo(0, size);
        context.stroke();
        return board[0][2]
    }    
    game_running = true;
    return 0;
}

screen.addEventListener("mousedown", (event) => {
    if (!game_running) return;
    let rect = screen.getBoundingClientRect();
    let x = Math.floor((event.x - rect.x) / tileSize);
    let y = Math.floor((event.y - rect.y) / tileSize);

    if (!board[y][x]) {
        board[y][x] = current_symbol;
        current_symbol = ((current_symbol) % 2) + 1;
        console.log(current_symbol);
        
    }
})