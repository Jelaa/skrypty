import { detectCollision } from './collision.js'

export default class Brick {
    constructor(gameManager, position) {
        this.image = document.getElementById("img_brick");
        this.gameManager = gameManager;
        this.position = position;
        this.width = gameManager.board_width/gameManager.brick_number;
        this.height = 20;
        this.color = '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
        this.setForDelete = false;

    }

    update() {
        if(detectCollision(this.gameManager.ball, this)) {
            this.gameManager.ball.speed.y = -this.gameManager.ball.speed.y;
            this.setForDelete = true;
        }

    }

    draw(context) {
        /*context.fillStyle = this.color;
        context.fillRect(
                this.position.x,
                this.position.y,
                this.width,
                this.height
        );*/

        context.drawImage(
            this.image,
            this.position.x,
            this.position.y,
            this.width,
            this.height
          );
    }
}