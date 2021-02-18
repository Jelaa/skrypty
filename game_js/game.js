import Paddle from './paddle.js';
import KeyHandler from './key.js';
import Ball from './ball.js';
//import {buildLevel, level_1, level_2} from './level.js';
import {buildLevel, levels} from './level.js';

const GAME_STATE = {
   PAUSED: 0,
   RUNNING: 1,
   MENU: 2,
   GAME_OVER: 3,
   NEW_LEVEL: 4
};

export default class GameManager {
    constructor(board_width, board_height) {
        this.board_width = board_width;
        this.board_height = board_height; 
        this.gameObjects = [];
        this.bricks = [];
        this.brick_number = 9;
        this.lives = 1;
        this.gameState = GAME_STATE.MENU;
        this.ball = new Ball(this);
        this.paddle = new Paddle(this);
        this.levels = levels;
        this.currentLevel = 0;
        new KeyHandler(this.paddle, this); 
    }

    game_init() {

        if(
            this.gameState !== GAME_STATE.MENU &&
            this.gameState !== GAME_STATE.NEW_LEVEL
        ) return;

        this.ball.reset();
        this.bricks = buildLevel(this, this.levels[this.currentLevel]);
        this.gameObjects = [this.paddle, this.ball];
        this.gameState = GAME_STATE.RUNNING;
    }

    draw(context) {

        [...this.bricks, ...this.gameObjects].forEach(object => object.draw(context));

        switch(this.gameState) {
            case GAME_STATE.PAUSED:
                context.rect(-1, -1, this.board_width, this.board_height);
                context.fillStyle = "rgba(0, 0, 0, 0.5)";
                context.fill();
                context.font = "30px Calibri";
                context.fillStyle = "Purple";
                context.textAlign = "center";
                context.fillText("PAUSED", this.board_width/2, this.board_height/2);
                break;
            case GAME_STATE.MENU:
                context.rect(-1, -1, this.board_width, this.board_height);
                context.fillStyle = "rgba(0, 0, 0, 1)";
                context.fill();
                context.font = "30px Calibri";
                context.fillStyle = "Purple";
                context.textAlign = "center";
                context.fillText("Press ENTER to start", this.board_width/2, this.board_height/2);
                break;
            case GAME_STATE.GAME_OVER:
                context.rect(-1, -1, this.board_width, this.board_height);
                context.fillStyle = "rgba(0, 0, 0, 1)";
                context.fill();
                context.font = "30px Calibri";
                context.fillStyle = "Purple";
                context.textAlign = "center";
                context.fillText("GAME OVER :(", this.board_width/2, this.board_height/2);
                break;
            case GAME_STATE.NEW_LEVEL:
                context.rect(-1, -1, this.board_width, this.board_height);
                context.fillStyle = "rgba(0, 0, 0, 0.5)";
                context.fill();
                context.font = "30px Calibri";
                context.fillStyle = "Purple";
                context.textAlign = "center";
                context.fillText("NEW LEVEL", this.board_width/2, this.board_height/2);
                break;
                
        }
    }

    update() {
        if(this.lives === 0) this.gameState = GAME_STATE.GAME_OVER;
        
        if(
            this.gameState == GAME_STATE.PAUSED  || 
            this.gameState == GAME_STATE.MENU ||
            this.gameState == GAME_STATE.GAME_OVER ||
            this.gameState == GAME_STATE.NEW_LEVEL
        ) return;

        if(this.bricks.length === 0) {
            this.currentLevel++;
            this.gameState = GAME_STATE.NEW_LEVEL;
            //this.game_init();
        }

        [...this.bricks, ...this.gameObjects].forEach(object => object.update());
        //this.gameObjects.forEach(object => object.update(delta_time));
        this.bricks = this.bricks.filter(brick => !brick.setForDelete);
    }

    pause() {
        if(this.gameState == GAME_STATE.PAUSED) {
            this.gameState = GAME_STATE.RUNNING;
        } else {
            this.gameState = GAME_STATE.PAUSED;
        }
    }
}