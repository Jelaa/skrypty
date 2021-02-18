#!/bin/bash

FIRST_COL=10
FIRST_ROW=5

# game description
declare -i HEIGHT=$(($(tput lines)-20)) WIDTH=$(($(tput cols)/2-30))
declare -i CURRENT_ROW CURRENT_COL
declare -i COMMAND_ROW=$(($HEIGHT+2)) COMMAND_COL=$FIRST_COL
declare -i SCORE_ROW=$FIRST_ROW SCORE_COL=$(($WIDTH+2))
declare -i COMMENT_ROW=$(($FIRST_ROW-2)) COMMENT_COL=$FIRST_COL
declare play=true

# snake description
declare -i head_col head_row tail_col tail_row
declare -i prev_head_col prev_head_row
declare -i current_head_row current_head_col 
declare -i current_tail_row current_tail_col 
declare -A snake_body_row snake_body_row_temp
declare -A snake_body_col snake_body_col_temp
declare -i snake_length
declare alive=true

# food description
declare -i food_row food_col 
declare -A food_pos
declare food

# game colors description
border_color=$(tput setaf 5)   
snake_color=$(tput setaf 2)
snake_background_color=$(tput setb 2)
food_color=$(tput setaf 3)
text_color=$(tput setaf 6)
no_color=$(tput sgr0)

init_game() {

    clear
    echo -ne "\e[?25l"
    stty -echo
    #for ((i=0; i<HEIGHT; i++)); do
    #    for ((j=0; j<WIDTH; j++)); do
    #        eval "arr$i[$j]=' '"
    #    done
    #done
}

init_snake() {

    head_col=$((WIDTH/2))
    head_row=$((HEIGHT/2))
    tail_col=$head_col
    tail_row=$head_row

    current_head_row=$head_row
    current_head_col=$head_col
    current_tail_row=$tail_row
    current_tail_col=$tail_col

    tput cup $head_row $head_col
    printf %b "${snake_color}${snake_background_color}O${no_color}"

    snake_body_row+=$head_row
    snake_body_col+=$head_col

    snake_length=1
}

init_board() {

    CURRENT_ROW=$FIRST_ROW
    CURRENT_COL=$FIRST_COL

    tput cup $CURRENT_ROW $CURRENT_COL

    for ((i=$FIRST_COL; i<=WIDTH; i++));
    do
        printf %b "${border_color}X${no_color}"
        CURRENT_COL=$i
    done

    for ((i=$FIRST_ROW; i<=HEIGHT; i++));
    do
        CURRENT_ROW=$i
        tput cup $CURRENT_ROW $CURRENT_COL
        printf %b "${border_color}X${no_color}"
    done

    for ((i=$CURRENT_COL; i>=FIRST_COL; i--));
    do
        CURRENT_COL=$i
        tput cup $CURRENT_ROW $CURRENT_COL
        printf %b "${border_color}X${no_color}"
    done

    for ((i=$CURRENT_ROW; i>=FIRST_ROW; i--));
    do
        CURRENT_ROW=$i
        tput cup $CURRENT_ROW $CURRENT_COL
        printf %b "${border_color}X${no_color}"
    done

    init_snake
    food=0

    tput cup $SCORE_ROW $SCORE_COL
    echo "${text_color}SCORE${no_color}" "$(($snake_length-1))" 
    tput cup $COMMENT_ROW $COMMENT_COL
    echo "Keys: W - UP S - DOWN A - LEFT D - RIGHT Q - QUIT P - PAUSE"   
}

update_snake_body() {
    for ((i=0; i<$snake_length; i++)); do
        if [[ "$i" -ne 0 ]]; then
            snake_body_row_temp[$i]=${snake_body_row[$(($i-1))]}
            snake_body_col_temp[$i]=${snake_body_col[$(($i-1))]}
        else
            snake_body_row_temp[0]=$head_row
            snake_body_col_temp[0]=$head_col
        fi
    done

    for ((i=0; i<$snake_length; i++)); do
        snake_body_row[$i]=${snake_body_row_temp[$i]}
        snake_body_col[$i]=${snake_body_col_temp[$i]}
    done
}

move_snake() {

    update_snake_body
    for ((i=0; i<$snake_length; i++)); do
        tput cup ${snake_body_row[$i]} ${snake_body_col[$i]}
        printf %b "${snake_color}${snake_background_color}O${no_color}"
    done  
    
    tput cup $current_tail_row $current_tail_col
    printf %b " "

    current_tail_row=${snake_body_row[$(($snake_length-1))]}
    current_tail_col=${snake_body_col[$(($snake_length-1))]}

    current_head_row=$head_row
    current_head_col=$head_col

    #sleep 0.1
    if [[ "$current_head_row" -eq "$food_row"  &&  "$current_head_col" -eq "$food_col" ]] || [[ "$prev_head_row" -eq "$food_row"  &&  "$prev_head_col" -eq "$food_col" && "$food" -eq 1 ]]; then
        food=0
        snake_length=$(($snake_length+1))
        tput cup $SCORE_ROW $SCORE_COL
        echo "${text_color}SCORE${no_color}" "$(($snake_length-1))"
    fi
}

check_collision() {
    for ((i=1; i<$snake_length; i++)); do
        if [[ "$head_row" -eq " ${snake_body_row[$i]}" && 
            "$head_col" -eq " ${snake_body_col[$i]}" ]]; then
            alive=false
        fi
    done

    if [[ "$head_row" -eq "$FIRST_ROW" || "$head_row" -eq "$HEIGHT" 
        || "$head_col" -eq "$FIRST_COL" || "$head_col" -eq "$WIDTH" ]]; then
        alive=false
    fi

    if [[ "$alive" = false ]]; then
        tput cup $COMMAND_ROW $COMMAND_COL
        tput ed
        echo "${text_color}GAME_OVER!${no_color}" "PLAY AGAIN? Yes ${text_color}[Y]${no_color} or No ${text_color}[N]${no_color}"
        read -s -n 1 play_key
        while [ "$play_key" != "y" ] && [ "$play_key" != "n" ];
        do
            read -s -n 1 exit_key
        done

        if [[ $play_key = y ]]; then
            play=true
        else
            play=false
            tput clear
            stty echo
            echo -e "\e[?25h"
            echo "YOU QUITED GAME :("
            exit 0
        fi
    fi
}

generate_food() {

    if [[ "$food" -eq 0 ]]; then
        food_row=$((RANDOM % HEIGHT))
        food_col=$((RANDOM % WIDTH))
        while [ "$FIRST_ROW" -ge "$food_row" ]; 
        do
            food_row=$((RANDOM % HEIGHT))
        done
        while [ "$FIRST_COL" -ge "$food_col" ]; 
        do
            food_col=$((RANDOM % WIDTH))
        done
        tput cup $food_row $food_col
        printf %b "${food_color}O${no_color}"
        food=1
    fi

}

quit_game() {

    tput cup $COMMAND_ROW $COMMAND_COL
    tput ed
    echo "QUITING... Do you really want to exit game? Yes ${text_color}[Y]${no_color} or No ${text_color}[N]${no_color}"
    read -s -n 1 exit_key
    while [ "$exit_key" != "y" ] && [ "$exit_key" != "n" ];
    do
        read -s -n 1 exit_key
    done
    
    if [[ $exit_key = y ]]; then
        tput clear
        stty echo
        echo -e "\e[?25h"
        echo "YOU QUITED GAME :("
        exit 0
    else
        tput cup $COMMAND_ROW $COMMAND_COL
        tput ed
    fi
}

while [ "$play" = true ];
do
    alive=true
    init_game
    init_board

    while [ "$alive" = true ];
    do
        generate_food
        move_snake
        read -s -n 1 -t 0.05 current_key
        if [[ $current_key = p ]]; then
            while [ "$resume_key" != "r" ];
            do
                tput cup $COMMAND_ROW $COMMAND_COL
                tput ed
                echo "GAME PAUSED... press ${text_color}[R]${no_color} to resume"
                read -s -n 1 resume_key
            done
            tput cup $(($HEIGHT+1)) $FIRST_COL
            tput ed
            resume_key=$previous_key
            current_key=$previous_key

        elif [[ $current_key != w && $current_key != s && $current_key != a 
            && $current_key != d && $current_key != q ]]; then
            current_key=$previous_key

        elif [[ ($current_key = w && $previous_key = s) || ($current_key = s 
            && $previous_key = w) || ($current_key = a && $previous_key = d) 
            || ($current_key = d && $previous_key = a) ]]; then
            current_key=$previous_key      
        fi

        prev_head_row=$head_row
        prev_head_col=$head_col

        case "$current_key" in
                "w") head_row=$(($head_row-1));;
                "s") head_row=$(($head_row+1));;
                "a") head_col=$(($head_col-1));;
                "d") head_col=$(($head_col+1));;
                "q") quit_game;;
        esac
        check_collision

        if [[ $current_key = q ]]; then
            current_key=$previous_key
        fi
        previous_key=$current_key
    done
done

exit 0
