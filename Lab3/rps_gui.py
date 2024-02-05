# Import the pygame module
import pygame
import rps_ai as rps

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_RATE = 30

WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

rock_image = pygame.image.load("rock.png")
paper_image = pygame.image.load("paper.png")
scissors_image = pygame.image.load("scissors.png")

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fill the screen with white
screen.fill((255, 255, 255))

class Player(pygame.sprite.Sprite):
    def __init__(self, move):
        super(Player, self).__init__()
        self.move = move
        self.surf = pygame.image.load("{self.move}.png").convert()

class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.surf = pygame.Surface((150, 100))
        self.rect = self.surf.get_rect(
            center=(x, y)
        )
        self.surf.fill(GRAY)

    def draw(self):
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=(self.surf.get_width() / 2, self.surf.get_height() / 2))
        self.surf.blit(text_surf, text_rect)

        global screen
        screen.blit(self.surf, self.rect)

    def is_clicked(self, pos, group=None):
        if group is not None:
            return self.rect.collidepoint(pos) and self in group
        else:
            return self.rect.collidepoint(pos)
    
class Leaderboard:
    def __init__(self, x, y):
        self.player_score = 0
        self.AI_score = 0

moveButtons = pygame.sprite.Group()
otherButtons = pygame.sprite.Group()

rock = Button("rock", 200, 300)
paper = Button("paper", 400, 300)
scissors = Button("scissors", 600, 300)
play_again = Button("Play Again?", 400, 500)

# Create a font for the text box
font = pygame.font.Font(None, 36)

def drawMoveButtons(rock, paper, scissors, moveButtons, otherButtons):
    otherButtons.empty()
    screen.fill(WHITE)
    rock.draw()
    moveButtons.add(rock)
    paper.draw()
    moveButtons.add(paper)
    scissors.draw()
    moveButtons.add(scissors)
    text_surface = font.render("Select your move", True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(text_surface, text_rect)

drawMoveButtons(rock, paper, scissors, moveButtons, otherButtons)

def showResult(player_move, ai_move, play_again, moveButtons, otherButtons):
    # Reupdate screen with who won
    moveButtons.empty()
    screen.fill(WHITE)

    # Show player move's image
    player_image = pygame.image.load(f"{player_move}.png")
    player_rect = player_image.get_rect(center=(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    screen.blit(player_image, player_rect)

    # Show AI move's image
    ai_image = pygame.image.load(f"{ai_move}.png")
    ai_rect = ai_image.get_rect(center=(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2))
    screen.blit(ai_image, ai_rect)

    # Text showing which move was player and which one was ai
    player_text = font.render(f"Player: {player_move}", True, BLACK)
    player_text_rect = player_text.get_rect(center=(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 + 200))
    screen.blit(player_text, player_text_rect)

    ai_text = font.render(f"AI: {ai_move}", True, BLACK)
    ai_text_rect = ai_text.get_rect(center=(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 + 200))
    screen.blit(ai_text, ai_text_rect)

    # Show result
    result = rps.get_winner(player_move, ai_move)
    text_surface = font.render(result, True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(text_surface, text_rect)
    play_again.draw()
    otherButtons.add(play_again)

pygame.display.flip()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
clock.tick(30)

running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            player_move = None
            if rock.is_clicked(mouse_pos, moveButtons):
                print('*')
                player_move = "rock"
            elif paper.is_clicked(mouse_pos, moveButtons):
                print('**')
                player_move = "paper"
            elif scissors.is_clicked(mouse_pos, moveButtons):
                print('***')
                player_move = "scissors"
            
            if player_move is not None:
                print('****')
                ai_move = rps.get_ai_input()
                showResult(player_move, ai_move, play_again, moveButtons, otherButtons)

            elif play_again.is_clicked(mouse_pos):
                print('hi')
                drawMoveButtons(rock, paper, scissors, moveButtons, otherButtons)

    pygame.display.flip()

