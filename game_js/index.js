import GameManager from './game.js';

let canvas = document.getElementById("gameScreen");
let context = canvas.getContext("2d");
//document.body.style.backgroundColor = "Pink"
//document.getElementById("gameWindow").style.backgroundColor = 'Pink';

const GAME_WIDTH = 800;
const GAME_HEIGHT = 600;

let gameManager = new GameManager(GAME_WIDTH, GAME_HEIGHT);

let last_time = 0;

function gameLoop() { //timestamp
  //let delta_time = timestamp - last_time;
  //last_time = timestamp;

  context.clearRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
  gameManager.update();
  gameManager.draw(context);

  window.requestAnimationFrame(gameLoop);
}

window.requestAnimationFrame(gameLoop);
