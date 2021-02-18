import { detectCollision } from './collision.js'

export default class Ball {
    constructor(gameManager) {
        //this.image = document.getElementById("img_ball");
        this.board_width = gameManager.board_width;
        this.board_height = gameManager.board_height;
        this.size = 15;
        this.gameManager = gameManager;
        this.reset();
    }

    reset() {
        this.speed = {x: 4, y: -2};
        this.ball_position = {x: 100, y: 400};
    }

    draw(context) {
        context.beginPath();
        context.arc(
            this.ball_position.x, 
            this.ball_position.y, 
            this.size, 
            0, 
            Math.PI*2);
        context.fillStyle = "Magenta";
        context.closePath();
        context.fill();
        /*context.drawImage(
            this.image,
            this.ball_position.x,
            this.ball_position.y,
            this.size,
            this.size
          );*/
        
    }

    update() {
        this.ball_position.x += this.speed.x;
        this.ball_position.y += this.speed.y;

        // wall on left or right

        if(this.ball_position.x + this.size > this.board_width || this.ball_position.x - this.size < 0) {
            this.speed.x = -this.speed.x;
        }

        // wall on top

        if(this.ball_position.y - this.size < 0) {
            this.speed.y = -this.speed.y;
        }

        if(this.ball_position.y + this.size > this.board_height) {
            this.gameManager.lives--;
            this.reset();
        }

        if(detectCollision(this, this.gameManager.paddle)) {
            this.speed.y = -this.speed.y;
            this.ball_position.y = this.gameManager.paddle.position.y - this.size;
        }

    }
}
