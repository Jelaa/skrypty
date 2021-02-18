export default class Paddle {
    constructor(gameManager) {
        this.board_width = gameManager.board_width;
        this.width = 150;
        this.height = 20;
        this.max_speed = 6;
        this.speed = 0;
    
        this.position = {
            x: gameManager.board_width / 2 - this.width / 2,
            y: gameManager.board_height - this.height - 10
        };
    }
  
    draw(context) {
        context.fillStyle = "Cyan"; //"#FF24DA80";
        context.fillRect(
            this.position.x,
            this.position.y,
            this.width,
            this.height
          );
    }

    update() {
        this.position.x += this.speed;
        if(this.position.x < 0) this.position.x = 0;
        if(this.position.x + this.width > this.board_width) 
            this.position.x = this.board_width - this.width;
    }

    moveLeft() {
        this.speed = -this.max_speed;
    }
    
    moveRight() {
        this.speed = this.max_speed;
    }

    stop() {
        this.speed = 0;
    }
  }
  