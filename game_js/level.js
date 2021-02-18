import Brick from './brick.js';

export function buildLevel(gameManager, level) {
    let bricks = [];
    level.forEach((row, rowIndex) => {
        row.forEach((brick, brickIndex) => {
            if (brick === 1) {
                let position = {
                    x: gameManager.board_width/gameManager.brick_number * brickIndex,
                    y: 70 + 20 * rowIndex
                }
                bricks.push(new Brick(gameManager, position));
            }
        });
    }); 
    return bricks;
}


const level_1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]

];

const level_2 = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0]
];

const level_3 = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 0, 0]
];

const level_4 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
];

const level_5 = [
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1]
];

export const levels = [level_1, level_2, level_3, level_4, level_5];
