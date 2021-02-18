export default class KeyHandler {
    constructor(paddle, gameManager) {
      document.addEventListener("keydown", event => {
        switch(event.keyCode) {
            case 37:
                paddle.moveLeft();
                break;
            case 39:
                paddle.moveRight();
                break;
            case 27:
                gameManager.pause();
                break;
            case 13:
                gameManager.game_init();
                break;
        }
      });

      document.addEventListener("keyup", event => {
        switch(event.keyCode) {
            case 37:
                if(paddle.speed < 0)
                    paddle.stop();
                break;
            case 39:
                if(paddle.speed > 0)
                    paddle.stop();
                break;
            /*case 27:
              gameManager.pause();
              break;*/
        }
      });
    }
  }
  