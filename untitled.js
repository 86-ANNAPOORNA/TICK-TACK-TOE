let gameId;
let mode;

document.getElementById('multi').onclick = async () => {
    mode = 'multi';
    const response = await fetch('/start', { method: 'POST' });
    const data = await response.json();
    gameId = data.game_id;
    setupGame();
};

document.getElementById('ai').onclick = async () => {
    mode = 'ai';
    const response = await fetch('/start_ai', { method: 'POST' });
    const data = await response.json();
    gameId = data.game_id;
    setupGame();
};

function setupGame() {
    document.getElementById('board').style.display = 'grid';
    document.getElementById('reset').style.display = 'none';
    resetBoard();
}

document.querySelectorAll('.cell').forEach(cell => {
    cell.onclick = async () => {
        const index = cell.getAttribute('data-index');
        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game_id: gameId, position: index })
        });
        const data = await response.json();
        updateBoard(data);
    };
});

function resetBoard() {
    document.querySelectorAll('.cell').forEach(cell => {
        cell.innerText = ' ';
    });
    document.getElementById('message').innerText = '';
}

function updateBoard(data) {
    if (data.error) {
        alert(data.error);
        return;
    }
    data.board.forEach((value, index) => {
        document.querySelector(`.cell[data-index="${index}"]`).innerText = value;
    });
    if (data.winner) {
        document.getElementById('message').innerText = `Winner: ${data.winner}`;
        document.getElementById('reset').style.display = 'block';
    }
}

document.getElementById('reset').onclick = () => {
    resetBoard();
    document.getElementById('message').innerText = '';
};
