import sys
import time

import pygame

import noughtsandcrosses as nac

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (192, 192, 192)
grayBk = (149, 148, 156, 61)
blue = (70, 130, 180)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Noughts and Crosses")

mediumFont = pygame.font.Font("SFProDisplay-Regular.ttf", 28)
largeFont = pygame.font.Font("SFProDisplay-Regular.ttf", 40)
moveFont = pygame.font.Font("SFProDisplay-Regular.ttf", 60)

user = None
board = nac.initial_state()
ai_turn = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(grayBk)

    # Let user choose a player.
    if user is None:
        # Draw title
        title = mediumFont.render("Welcome to the game of noughts and crosses.", True, white)
        titleRect = title.get_rect()
        titleRect.center = (width / 2, 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton, border_radius=10)
        screen.blit(playX, (playXRect.centerx - playXRect.width // 2, playXRect.centery - playXRect.height // 2))
        playXRect = playX.get_rect(center=playXRect.center)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton, border_radius=10)
        screen.blit(playO, (playORect.centerx - playORect.width // 2, playORect.centery - playORect.height // 2))
        playORect = playO.get_rect(center=playORect.center)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = nac.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = nac.O

    else:
        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, gray, rect)
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != nac.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = nac.terminal(board)
        player = nac.player(board)

        # Show title
        if game_over:
            winner = nac.winner(board)
            if winner is None:
                title = "Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = "Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = (width / 2, 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = nac.minimax(board)
                board = nac.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == nac.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = nac.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again!", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, blue, againButton, border_radius=10)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = nac.initial_state()
                    ai_turn = False

    pygame.display.flip()
