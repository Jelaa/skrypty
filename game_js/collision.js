export function detectCollision(ball, gameObject) {

    let ball_bottom = ball.ball_position.y + ball.size;
    let ball_top = ball.ball_position.y;
    let top_object = gameObject.position.y;
    let bottom_object = gameObject.position.y + gameObject.height;
    let left_obeject = gameObject.position.x;
    let right_object = gameObject.position.x + gameObject.width;

    if(
        ball_bottom >= top_object && 
        ball_top <= bottom_object &&
        ball.ball_position.x >= left_obeject && 
        ball.ball_position.x + ball.size <= right_object
    ) {
        return true;
    } else {
        return false;
    }
}