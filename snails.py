import arcade

# Loading needed images
background = arcade.load_texture("Images/BC.jpg") # background image
humanSnail = arcade.load_texture("Images/snail1.png") # image of human's snail
botSnail = arcade.load_texture("Images/snail2.png") # image of bots's snail
humanSplash = arcade.load_texture("Images/splash_snail1.png") # image of Human's Splash
botSplash = arcade.load_texture("Images/splash_snail2.png") # image of Bot's Splash

ROWS = 10 # number of rows in the grid
COLUMNS = 10 # number of columns in the grid
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "--->SNAILS<---"
board = [] # 2D List for backEnd Matrix
G_SIZE = 60 # Size of one box

class Game(arcade.View):
    def __init__(self):
        super().__init__()

        self.initailizeBoard()
        
        #Identifiers of snails and Splashes locaions
        self.human = 1  
        self.bot = 2
        self.human_Splash = 10
        self.bot_Splash = 20

        self.state = 0 # Other states can be 50(for Draw), 100(Human Win), 200(Bot win)
        self.game_state = "GameMenu" #Setting this to show menu Screen 
        self.turn = 1000 #(Human Turn) if Turn = 2000 (Bot Turn) 
        self.human_score = 0 #counter
        self.bot_score= 0 # counter
        self.human_Location = (0,0) # Initial Position of Human Snail is (0,0)
        self.Bot_Location = (9,9) # Initial Position of Bot is (9,9)
    
    def initailizeBoard(self):
        #The function is making the back-end 2D matrix
        #for the front end interface Grid.
        for j in range(ROWS):
            row = []
            for i in range(COLUMNS):
                row.append(0)
            board.append(row)
        board[0][0] = 1          # marker of human in the backend matrix is 1
        board[ROWS-1][COLUMNS-1] = 2 # marker of bot in the backend matrix is 2
        print(board)
  
    def evaluateBoard(self):
        if self.bot_score == 50 and self.human_score == 50:
            self.game_state = "Draw"
           # return 5 # for Draw State
        elif self.bot_score > 50:
            self.game_state = "BotWon"
            #return 10 # for Bot Win
        elif self.human_score > 50:
            self.game_state = "HumanWon"
            #return 1 # for Human Win
        else:
            for i in range(10):
                for j in range(10):
                    if board[i][j] == 0:
                        self.state = 0  # Continue State
            #            return 0          game_state = "GameOn" is Continue State

    def on_key_press(self, key, modifiers):
        pass
            
    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.game_state == "GameMenu":
                self.game_state = "GameOn"
        
        elif self.game_state == "GameOn":
            box = (x//G_SIZE, y//G_SIZE)    #Location of box
            if(self.is_Legal_Move(box)):
                self.update_grid(box)       
                self.evaluateBoard()
            else:
                if self.turn == 1000:
                    self.human_score -= 1
                    self.turn = 2000

                elif self.turn == 2000:
                    self.bot_score -= 1
                    self.turn = 1000
            
    def is_Legal_Move(self,box):
        #Clicking on grid line (Not Checking right now)
        #Clicking on an area out of bounds(outside the GridWorld) (Checking)
        #Moving the Snail onto opponent’s Snail or Trail of Slime (Checking)
        #Playing a move by passing an empty Grid Square (Not Checking right now)

        if box[0] <= SCREEN_WIDTH and box[1] <= SCREEN_HEIGHT: #Checking if clicked out side screen
            if self.turn == 1000:
                if board[box[0]][box[1]] == 0 or board[box[0]][box[1]] == 10:
                    return True
                else:
                    return False
            elif self.turn == 2000:
                if board[box[0]][box[1]] == 0 or board[box[0]][box[1]] == 20:
                    return True
                else:
                    return False
        else:
            return False

    def update_grid(self,box):
        """
        This function is updating backend 2d matrix and player scores.
        box(x,y) is the location where Snail needs to be placed. 
        """
       # print("\n\n\n---box = {0}".format(box))
        if self.turn == 1000:
            board[self.human_Location[0]][self.human_Location[1]] = 10
            board[box[0]][box[1]] = 1
            self.turn = 2000
            self.human_Location = box
            self.human_score += 1        #Increasing Human Score
        elif self.turn == 2000:
            board[self.Bot_Location[0]][self.Bot_Location[1]] = 20
            board[box[0]][box[1]] = 2    
            self.turn = 1000
            self.Bot_Location = box     
            self.bot_score += 1         #Increasing Bot Score
        print("------------------------------------")
        print(board)
        
    def on_show(self):
        arcade.set_background_color(arcade.color.WOOD_BROWN) #Background color

    def on_draw(self):
        arcade.start_render()
        # self.shape_list = arcade.ShapeElementList()
        # self.shape_list.draw()

        if self.game_state == "GameMenu": 
            arcade.draw_text("Menu Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Click to Start Game", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

        elif self.game_state == "GameOn":

            # setting the background image
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, background)
            
            #Drawing Lines for playing Snail for Front End Grid.
            for x in range (0, 600, G_SIZE): 
                arcade.draw_line(0, x, 600, x, arcade.color.BLACK, 4)
            for y in range (0, 600, G_SIZE):
                arcade.draw_line(y, 0, y, 600, arcade.color.BLACK, 4)

            #These for loops are maping background 2D Matrix with Front End Grid.
            for i in range(10):  
                for j in range(10):
                    if board[i][j] == 1:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, humanSnail)
                    elif board[i][j] == 2:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, botSnail)
                    elif board[i][j] == 10:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, humanSplash)
                    elif board[i][j] == 20:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, botSplash)
        
        elif self.game_state == "GameOver":
            pass
        elif self.game_state == "Draw":
            pass
        elif self.game_state == "HumanWon":
            pass
        elif self.game_state == "BotWon":
            pass


def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    game_view = Game()
    window.show_view(game_view)
    arcade.run()

main()
