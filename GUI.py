import pygame
import time
from main_noprint import *  
# from main_print import *

BOARD_SIZE= 9
BOX_SIZE= 3
# define Colors
BLACK= (0, 0, 0)
WHITE= (255, 255, 255)
GREY= (200, 200, 200)
RED= (255, 0, 0)
LIGHT_BLUE= (173, 216, 230)
GREEN= (0, 255, 0)
BLUE = (0, 0, 255)  
LIGHT_GREY= (220, 220, 220)
BACKGROUND_COLOR = (240, 240, 240)

# define sizes
BUTTON_WIDTH, BUTTON_HEIGHT = 470, 100
SCREEN_HEIGHT= 690
SCREEN_WIDTH= 950
FONT_SIZE = 40

# load images
one_heart_image = pygame.image.load("1heart.jpg") 
two_image = pygame.image.load("2hearts.jpg")  
three_image = pygame.image.load("3hearts.jpg")  
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Resize the heart images
heart_width = 200  # Set the desired width for the hearts
heart_height = 50  # Set the desired height for the hearts
one_heart_image = pygame.transform.scale(one_heart_image, (heart_width, heart_height))
two_image = pygame.transform.scale(two_image, (heart_width, heart_height))
three_image = pygame.transform.scale(three_image, (heart_width, heart_height))

# Game
pygame.init()
pygame.display.set_caption("Sudoku Game")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, FONT_SIZE)

# helper functions (handle_arrow_keys, draw_button, draw_grid , show_notification, initialize_grid, draw_numbers, get_clicked_cell)
def handle_arrow_keys(selected_cell, key):
    row, col = selected_cell
    if key == pygame.K_UP:
        row = max(0, row - 1)
    elif key == pygame.K_DOWN:
        row = min(8, row + 1)
    elif key == pygame.K_LEFT:
        col = max(0, col - 1)
    elif key == pygame.K_RIGHT:
        col = min(8, col + 1)
    return (row, col)

def draw_button(text, rect, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def show_notification(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(WHITE)
    screen.blit(text, text_rect) #3shan trsm text on screen
    pygame.display.flip()
    pygame.time.delay(2000)
# da 3shan ye adjust elgrid myo5dsh kol elscreen
cell_size = 60
cell_margin = 8
board_size = 9 * cell_size + 10 * cell_margin
board_start_x = 15
board_start_y = 3

def draw_grid(selected_cell=None):
    screen.fill(BACKGROUND_COLOR)
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (board_start_x, board_start_y + i * (cell_size + cell_margin)),
                         (board_start_x + board_size, board_start_y + i * (cell_size + cell_margin)), thickness)
        pygame.draw.line(screen, BLACK, (board_start_x + i * (cell_size + cell_margin), board_start_y),
                         (board_start_x + i * (cell_size + cell_margin), board_start_y + board_size), thickness)

    if selected_cell:
        row, col = selected_cell
        cell_x = board_start_x + col * (cell_size + cell_margin) + 5  # Adding col * 2 for cell spacing
        cell_y = board_start_y + row * (cell_size + cell_margin) + 4  # Adding row * 2 for cell spacing
        selected_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

        pygame.draw.rect(screen, LIGHT_BLUE, selected_rect)

def initialize_grid():  # 3shan n3ml empty grid 9 fi 9 bns5tm numpy wa nmliha be zeros
    return np.full((9, 9), 0)

def draw_numbers(grid, initial_grid=None):
    for row in range(9):
        for col in range(9):
            value = grid[row][col]
            is_initial = initial_grid is not None and initial_grid[row][col] != 0
            color = BLACK if is_initial else GREEN
            if value != 0:
                text_surface = font.render(str(value), True, color)
                text_rect = text_surface.get_rect(center=(
                    board_start_x + col * (cell_size + cell_margin) + cell_size // 2,
                    board_start_y + row * (cell_size + cell_margin) + cell_size // 2
                ))
                screen.blit(text_surface, text_rect)

def get_clicked_cell(mouse_pos):
    row = (mouse_pos[1] - board_start_y) // (cell_size + cell_margin)
    col = (mouse_pos[0] - board_start_x) // (cell_size + cell_margin)
    # Check if the clicked position is within the grid
    if 0 <= row < 9 and 0 <= col < 9:
        return row, col
    else:
        return None
    
# 3 modes Functions 
def mode_1():
    print ("START MODE 1")
    initial_grid = generate_random_puzzle()  # 3shan n3ml elrandom puzzle
    grid = np.copy(initial_grid)  # bn3ml copy lel puzzle 3shan b3deen

    solving = False  # bns5tdmha 3shan n3rf nsolve wla laa wa da bbyb2a bsolve button aw by pressing a
    running = True  # used to make the loop work continuely until player quit
    

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers(grid, initial_grid)
        solve_button = pygame.Rect(700, 100, 200, 50)
        generate_button = pygame.Rect(700, 200, 200, 50)
        pygame.draw.rect(screen, GREY, solve_button)
        pygame.draw.rect(screen, GREY, generate_button)

        draw_button("Solve", solve_button, GREY, LIGHT_GREY)
        draw_button("Generate", generate_button, GREY, LIGHT_GREY)
        
        # Add note to press 'm' to go back to the main page
        note_font = pygame.font.Font(None, 20)
        note_text = note_font.render("Press 'm' to go back to the main page", True, BLACK)
        screen.blit(note_text, (700, 300))  # Adjust the position as needed


        note_font1 = pygame.font.Font(None, 20)
        note_text1 = note_font1.render("Press 'a' to solve", True, BLACK)
        screen.blit(note_text1, (700, 350))  # Adjust the position as needed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                elif event.key == pygame.K_a:  # AI begin to solve
                    solving = True
            # Check if Solve button is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if solve_button.collidepoint(mouse_pos):
                    solving = True
                elif generate_button.collidepoint(mouse_pos):
                    initial_grid = generate_random_puzzle()
                    grid = np.copy(initial_grid)
                    solving = False
        if solving:
            # solvable,_=backtracking(grid)
            start_time = time.time()  # Record start time
            solvable, _ = backtracking(grid)
            end_time = time.time()  # Record end time
            print("Time taken by backtracking:", end_time - start_time)
            if not solvable:
                show_notification("The generated puzzle is not solvable !!")
            # pygame.time.delay(100)  # Delaying to show the solved puzzle
            solving = False
        pygame.display.flip()

def mode_2():
    print("Start Mode 2")
    initial_grid = initialize_grid()
    grid = initialize_grid()
    selected_cell = None
    pygame.display.set_caption("Sudoku Game")
    text_solved = "The soduko may be solved"
    text_not_solved = "The soduko will not be solved !!"

    font = pygame.font.Font(None, 36)
    text_surface = font.render(text_solved, True, GREEN)  # Render text in green color
    # text_rect = text_surface.get_rect(center=(790, 200))  # Adjust Y position as needed
    # screen.blit(text_surface, text_rect)

    # To make user doesnot able to modify cell after ai solve
    can_modify=True

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(selected_cell)
        # draw_numbers(grid)
        draw_numbers(grid, initial_grid)

        regenerate_button = pygame.Rect(700, 100, 200, 50)
        pygame.draw.rect(screen, GREY, regenerate_button)
        draw_button("Regenerate", regenerate_button, GREY, LIGHT_GREY)
        text_rect = text_surface.get_rect(center=(790, 200))
        screen.blit(text_surface, text_rect)

        # Add note to press 'm' to go back to the main page
        note_font = pygame.font.Font(None, 20)
        note_text = note_font.render("Press 'm' to go back to the main page", True, BLACK)
        screen.blit(note_text, (700, 300))  # Adjust the position 
        
        # Add note to press 'start' to make ai solve
        note_text2 = note_font.render("Press 'space' to make AI solve", True, BLACK)
        screen.blit(note_text2, (700, 320))  # Adjust the position 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                elif event.key in (
                pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                pygame.K_9):
                    if can_modify and selected_cell:
                        row, col = selected_cell
                        number = int(event.unicode)
                        if is_valid_move(grid, row, col, number):
                            grid[row][col] = number
                            print(f"after make cell ({row},{col}) = {number}")
                            print("Start applying backtrack , to see if we can know that the puzzle isnot solved")
                            solv,_=backtracking(copy.deepcopy(grid))
                            if not solv:
                                text_surface = font.render(text_not_solved, True, RED)
                            else:
                                text_surface = font.render(text_solved, True, GREEN)
                            print("End of applying Backtracking.")
                elif event.key == pygame.K_BACKSPACE:
                    if can_modify and selected_cell:
                        row, col = selected_cell
                        grid[row][col] = 0
                        print(f"after make cell ({row},{col}) empty")
                        print("Start applying backtrack , to see if we can know that the puzzle isnot solved")
                        solv,_=backtracking(copy.deepcopy(grid))
                        if not solv:
                            text_surface = font.render(text_not_solved, True, RED)  # Render text in green color
                        else:
                            text_surface = font.render(text_solved, True, GREEN)  # Render text in green color
                        print("End of applying backtracking.")
                elif event.key == pygame.K_SPACE:  # Check solvability
                    if can_modify:
                        initial_grid = copy.deepcopy(grid)  # bn3ml copy lel puzzle 3shan b3deen
                        print ("AI Start Solving")
                        solved, _ = backtracking(grid)
                        print ("AI Finish Solving")
                        if not solved:  # this call the backtrackin to solve the Soduko
                            # print("The entered puzzle is not solvable.")
                            show_notification("The entered puzzle is not solvable.")
                            initial_grid = initialize_grid()
                            # grid = initialize_grid()  # Reset
                        if  solved:
                            can_modify=False
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if selected_cell:
                        selected_cell = handle_arrow_keys(selected_cell, event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if regenerate_button.collidepoint(mouse_pos):
                    grid = initialize_grid()  # for Clear the puzzle
                    selected_cell = None  # for Reset selected cell
                    can_modify=True
                    initial_grid = initialize_grid()
                else:
                    selected_cell = get_clicked_cell(mouse_pos)
        pygame.display.flip()

def mode_3():
    print("Start of mode 3 (Generating phase)")
    grid = initialize_grid()
    selected_cell = None
    solving_phase=False
    pygame.display.set_caption("Sudoku Game")
    text_solved = "The soduko can be solved"
    text_not_solved = "The soduko will not be solved !!"

    font = pygame.font.Font(None, 36)
    text_surface = font.render(text_solved, True, GREEN)  # Render text in green color
    # text_rect = text_surface.get_rect(center=(790, 200))  # Adjust Y position as needed
    # screen.blit(text_surface, text_rect)

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(selected_cell)
        draw_numbers(grid)
        star_solving_phase_button = pygame.Rect(660, 100, 270, 50)
        pygame.draw.rect(screen, GREY, star_solving_phase_button)
        draw_button("start solving phase", star_solving_phase_button, GREY, LIGHT_GREY)
        text_rect = text_surface.get_rect(center=(790, 200))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                elif event.key in (
                pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                pygame.K_9):
                    if selected_cell:
                        row, col = selected_cell
                        number = int(event.unicode)

                        if is_valid_move(grid, row, col, number):
                            grid[row][col] = number
                            copy_of_grid= copy.deepcopy(grid)
                            print(f"Start backtracking after put {number} in cell ({row},{col}) to check if the grid is solvable of not")
                            is_solvable,_ = backtracking(copy_of_grid)
                            print(f"End of backtracking")

                            if not is_solvable:
                                text_surface = font.render(text_not_solved, True, RED)
                            else:
                                text_surface = font.render(text_solved, True, GREEN)
                elif event.key == pygame.K_BACKSPACE:
                    if selected_cell:
                        row, col = selected_cell
                        grid[row][col] = 0
                        copy_of_grid= copy.deepcopy(grid)
                        print(f"Start backtracking after clear cell:({row},{col}) to check if the grid is solvable of not")
                        is_solvable,_ = backtracking(copy_of_grid)
                        print(f"End of backtracking")
                        if not is_solvable:
                            text_surface = font.render(text_not_solved, True, RED)  # Render text in green color
                        else:
                            text_surface = font.render(text_solved, True, GREEN)  # Render text in green color
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if selected_cell:
                        selected_cell = handle_arrow_keys(selected_cell, event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if star_solving_phase_button.collidepoint(mouse_pos):
                    solving_phase=True
                else:
                    selected_cell = get_clicked_cell(mouse_pos)
        if (solving_phase):
            print("Start of mode 3 (Solving phase)")
            mode_3_solvingphase(grid)

            break
        pygame.display.flip()

def mode_3_solvingphase(grid):
    grid_to_solve = grid
    player_grid = np.copy(grid_to_solve)
    lives = 3
    selected_cell=None
    start_time = time.time()  # Start 
    
    while True:
        elapsed_time = int(time.time() - start_time)  # Calculate elapsed time
        screen.fill(WHITE) # lazm di l awl , abl mktb text aw ahot swr

        draw_grid(selected_cell)
        draw_numbers(player_grid,grid_to_solve)

        time_text = font.render("Time: " + str(elapsed_time) + " seconds", True, BLACK)  # Time text
        screen.blit(time_text, (700, 200))  # Display time

        if lives==3 :
            screen.blit(three_image, (700 , 50))  
        if lives==2 :
            screen.blit(two_image, (700 , 50))  
        if lives==1 :
            screen.blit(one_heart_image, (700 , 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                elif event.key in (
                pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                pygame.K_9):
                    if selected_cell:
                        row, col = selected_cell
                        number = int(event.unicode)
                        if is_valid_move(player_grid, row, col, number):
                            if grid_to_solve[row][col] ==0 : # 3shan myn2sh l ragel lw 3yz yl3b f mkan f soduko aslya
                                player_grid[row][col] = number
                        else:
                            if grid_to_solve[row][col] ==0 : # 3shan myn2sh l ragel lw 3yz yl3b f mkan f soduko aslya
                                lives -= 1
                                if lives == 0:
                                    # print("Game over! You used all your lives.")
                                    show_notification("Game over! You used all your lives. start from beging")
                                    start_time = time.time()  # Start time
                                    player_grid = np.copy(grid_to_solve)
                                    lives =3
                elif event.key == pygame.K_BACKSPACE:
                    if selected_cell:
                        row, col = selected_cell
                        if grid_to_solve[row][col] ==0 : # 3shan myn2sh l ragel lw 3yz yl3b f mkan f soduko aslya
                            player_grid[row][col] = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if selected_cell:
                        selected_cell = handle_arrow_keys(selected_cell, event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                selected_cell = get_clicked_cell(mouse_pos)

        pygame.display.flip()

def mode4():
    grid = generate_random_puzzle()
    selected_cell = None
    solving_phase = False
    start_solving_button_pressed = False
    pygame.display.set_caption("Sudoku Game")
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(selected_cell)
        draw_numbers(grid)
        star_solving_phase_button = pygame.Rect(660, 100, 110, 50)
        pygame.draw.rect(screen, GREY, star_solving_phase_button)
        draw_button("start", star_solving_phase_button, GREY, LIGHT_GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                elif start_solving_button_pressed and event.key in (
                        pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                        pygame.K_8, pygame.K_9):
                    if selected_cell:
                        row, col = selected_cell
                        number = int(event.unicode)

                        if is_valid_move(grid, row, col, number):
                            grid[row][col] = number
                elif event.key == pygame.K_BACKSPACE:
                    if selected_cell:
                        row, col = selected_cell
                        grid[row][col] = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if selected_cell:
                        selected_cell = handle_arrow_keys(selected_cell, event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if star_solving_phase_button.collidepoint(mouse_pos):
                    solving_phase = True
                    start_solving_button_pressed = True
                else:
                    selected_cell = get_clicked_cell(mouse_pos)
        if solving_phase:
            print("Start of Solving phase")
            mode_3_solvingphase(grid)
            break
        pygame.display.flip()


# GUI main page
def main():
    mode_selected = False
    while not mode_selected:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))  # Draw the background image
        mode_1_button= pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
        mode_2_button= pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
        mode_3_button= pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)
        mode_4_button= pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GREY, mode_1_button)
        pygame.draw.rect(screen, GREY, mode_2_button)
        pygame.draw.rect(screen, GREY, mode_3_button)
        pygame.draw.rect(screen, GREY, mode_4_button)

        draw_button("Mode 1 _ AI (generate & solve)", mode_1_button, LIGHT_BLUE, LIGHT_GREY)
        draw_button("Mode 2 _ User generate & AI solve", mode_2_button, LIGHT_BLUE, LIGHT_GREY)
        draw_button("Mode 3 _ User (generate & solve)", mode_3_button, LIGHT_BLUE, LIGHT_GREY)
        draw_button("Mode 4 _ User (solve)", mode_4_button, LIGHT_BLUE, LIGHT_GREY)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if mode_1_button.collidepoint(mouse_pos):
                    mode_1()
                elif mode_2_button.collidepoint(mouse_pos):
                    mode_2()
                elif mode_3_button.collidepoint(mouse_pos):
                    mode_3()
                elif mode_4_button.collidepoint(mouse_pos):
                    mode4()

if __name__ == "__main__":
    main()