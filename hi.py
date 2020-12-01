import arcade
import random
import copy

# Loading needed images
background = arcade.load_texture("Images/BC.jpg") # background image
humanSnail = arcade.load_texture("Images/snail1.png") # image of human's snail
botSnail = arcade.load_texture("Images/snail2.png") # image of bots's snail
HumanSplash = arcade.load_texture("Images/splash_snail1.png") # image of Human's Splash
BotSplash = arcade.load_texture("Images/splash_snail2.png") # image of Bot's Splash
drawEmoji = arcade.load_texture("Images/thinking.png") # image of Draw State Emoji
menuEmoji = arcade.load_texture("Images/menuBack.jpg") # image of menu_screen

ROWS = 4 # number of rows in the grid
COLUMNS = 4 # number of columns in the grid

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

game_SCREEN_WIDTH = 600
game_SCREEN_HEIGHT = 600

SCREEN_TITLE = "--->SNAILS<---"

board = [] # 2D List for backEnd Matrix

G_SIZE = 150 # Size of one box

class Game(arcade.View):
    def __init__(self):
        super().__init__()

        self.initailizeBoard()
        
        #Identifiers of snails and Splashes locaions
        self.human = 1
        self.bot = 2
        self.humanSplash = 10
        self.botSplash = 20

        self.state = 0 # Other states can be 50(for Draw), 100(Human Win), 200(Bot win)
        self.game_state = "GameMenu" #Setting this to show menu Screen 
        self.turn = 1000 #(Human Turn) if Turn = 2000 (Bot Turn) 
        self.human_score = 0 #counter
        self.bot_score = 0 # counter

        self.human_Location = [0,0] # Initial Position of Human Snail is (0,0)
        self.Bot_Location = [3,3] # Initial Position of Bot is (9,9)
        
    
    def initailizeBoard(self):
        #The function is making the back-end 2D matrix
        #for the front end interface Grid.
        for j in range(ROWS):
            row = []
            for i in range(COLUMNS):
                row.append(0)
            board.append(row)
        board[0][0] = 1          # marker of human in the backend matrix is 1
        board[ROWS-1][COLUMNS-1] = 2 # marker of bot in the backend matrix is 2\
        for j in range(ROWS):
            print()
            for i in range(COLUMNS):
                print(board[i][j], end="\t")
        print()

    def evaluateBoard_AI(self, board):
        if self.bot_score == 14 and self.human_score == 14:
            self.game_state = "Draw"
            return 0
           # return 5 # for Draw State
        elif self.bot_score > 14:
            self.game_state = "BotWon"
            return 1
            #return 10 # for Bot Win
        elif self.human_score > 14:
            self.game_state = "HumanWon"
            return -1
            #return 1 # for Human Win
        else:
            for i in range(4):
                for j in range(4):
                    if board[i][j] == 0:
                        self.state = 0
                        return None  # Continue State
            #            return 0          game_state = "GameOn" is Continue State

    def evaluate(self, temp_board):
        h_count, b_count = 0, 0
        for i in range(4):
            for j in range(4):
                if temp_board[i][j] == 10:
                    h_count += 1
        for i in range(4):
            for j in range(4):
                if temp_board[i][j] == 20:
                    b_count += 1
        
        if b_count == 14 and h_count == 14:
            return 0
           # return 0 # for Draw State
        elif b_count > 14:
            return 1
            #return 1 # for Bot Win
        elif h_count > 14:
            return -1
            #return -1 # for Human Win                    


    def isMoveLeft(self, board):
        for i in range(ROWS):
            for j in range(COLUMNS):

                if board[i][j] == 0:
                    return True
        return False

    def minimax(self, temp_board, depth, maxLevel, isAgentTurn):
        win = 1
        draw = 0
        lose = -1

        result = self.evaluate(temp_board)


        if result == win or result == lose or result == draw:
            bestScore = result
        
        # elif depth == 6:
        #     for i in range(4):
        #         for j in range(4):
        #             if temp_board[i][j] == self.bot:
        #                 if self.heuristic(temp_board) > 2:
        #                     return 1

        if isAgentTurn:
            x, y = 0, 0
            for i in range(ROWS):
                for j in range(COLUMNS):
                    if temp_board[i][j] == self.bot:
                        x, y = i, j
                        break

            bestScore = -1000

            left, right, top, bottom = -1, -1, -1, -1
            try:
                left = temp_board[x-1][y]
            except:
                pass
            try:
                right = temp_board[x+1][y]
            except:
                pass
            try:
                top = temp_board[x][y+1]
            except:
                pass
            try:
                bottom = temp_board[x][y-1]
            except:
                pass

            if left == 0:
                temp_board[x][y] = 20
                temp_board[x-1][y] = 2

            if right == 0:
                temp_board[x][y] = 20
                temp_board[x+1][y] = 2

            if top == 0:
                temp_board[x][y] = 20
                temp_board[x][y+1] = 2

            if bottom == 0:
                temp_board[x][y] = 20
                temp_board[x][y-1] = 2

            score = self.minimax(temp_board, depth+1, maxLevel, False)
            
            bestScore = max(score, bestScore)
        
            return bestScore
        
        else:
            x, y = 0, 0
            
            for i in range(ROWS):
                for j in range(COLUMNS):
                    if temp_board[i][j] == self.human:
                        x, y = i, j
                        break

            bestScore = 1000

            left, right, top, bottom = -1, -1, -1, -1
            try:
                left = temp_board[x-1][y]
            except:
                pass
            try:
                right = temp_board[x+1][y]
            except:
                pass
            try:
                top = temp_board[x][y+1]
            except:
                pass
            try:
                bottom = temp_board[x][y-1]
            except:
                pass

            if left == 0:
                temp_board[x][y] = 10
                temp_board[x-1][y] = 1

            if right == 0:
                temp_board[x][y] = 10
                temp_board[x+1][y] = 1

            if top == 0:
                temp_board[x][y] = 10
                temp_board[x][y+1] = 1

            if bottom == 0:
                temp_board[x][y] = 10
                temp_board[x][y-1] = 1

            score = self.minimax(temp_board, depth+1, maxLevel, True)
            
            bestScore = min(score, bestScore)
            
            return bestScore

    def heuristic(self, board):
        
        x, y, visitedBoxes, rightBoxes, leftBoxes, topBoxes, bottomBoxes, winningChances = 0, 0, 0, 0, 0, 0, 0, 0
        
        # Calculate the number of visited boxes by AI Agent and add them to the variable ‘winnigChances’.
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == self.botSplash:
                    visitedBoxes += 1
        winningChances += visitedBoxes
        
        #giving index of bot position
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == self.bot:
                    x, y = j, i
                    break
        
        #below loops are counting zero boxes on all four sides of the bot
        for i in range(x+1, 4, 1):
            if board[i][y] == 0:
                rightBoxes += 1
            else:
                break
        for i in range(x-1, -1, -1):
            if board[i][y] == 0:
                leftBoxes += 1
            else:
                break
        for j in range(y+1, 4, 1):
            if board[x][j] == 0:
                topBoxes += 1
            else:
                break
        for j in range(y-1, -1, -1):
            if board[x][j] == 0:
                bottomBoxes += 1
            else:
                break
        
        #The number of empty boxes will be added to the variable ‘winnigChances’
        winningChances += max(rightBoxes, leftBoxes, topBoxes, bottomBoxes)
        
        # 10 will be added to the variable ‘winnigChances’ if bot is in central area.
        if((x != 0 and x != 4) and (y != 0 and y != 4)):
            winningChances += 10
        
        return winningChances

    def bot_move(self):
        if self.game_state == "GameOn":
            self.temp = []
            self.temp_board = copy.deepcopy(board)
            self.bestScore = -1000
            
            bx = self.Bot_Location[0]
            by = self.Bot_Location[1]
            
            left, right, top, bottom = -1, -1, -1, -1

            try:
                left = board[bx-1][by]
            except:
                pass
            try:
                right = board[bx+1][by]
            except:
                pass
            try:
                top = board[bx][by+1]
            except:
                pass
            try:
                bottom = board[bx][by-1]
            except:
                pass

            left_score, right_score, top_score, bottom_score = 0, 0, 0, 0
            if left == 0:
                self.temp_board[bx][by] = 20
                self.temp_board[bx-1][by] = 2
                left_score = self.minimax(self.temp_board, 0, 0, True)
                self.temp_board[bx][by] = 2
                self.temp_board[bx-1][by] = 0

            if right == 0:
                self.temp_board[bx][by] = 20
                self.temp_board[bx+1][by] = 2
                right_score = self.minimax(self.temp_board, 0, 0, True)
                self.temp_board[bx][by] = 2
                self.temp_board[bx+1][by] = 0

            if top == 0:
                self.temp_board[bx][by] = 20
                self.temp_board[bx][by+1] = 2
                top_score = self.minimax(self.temp_board, 0, 0, True)
                self.temp_board[bx][by] = 2
                self.temp_board[bx][by+1] = 0

            if bottom == 0:
                self.temp_board[bx][by] = 20
                self.temp_board[bx][by-1] = 2
                bottom_score = self.minimax(self.temp_board, 0, 0, True)
                self.temp_board[bx][by] = 2
                self.temp_board[bx][by-1] = 0

            if left_score == max(left_score, right_score, top_score, bottom_score) and left == 0:
                board[bx][by] = 20
                board[bx-1][by] = 2
                self.Bot_Location[0] = bx-1
                self.Bot_Location[1] = by

            elif right_score == max(left_score, right_score, top_score, bottom_score) and right == 0:
                board[bx][by] = 20
                board[bx+1][by] = 2
                self.Bot_Location[0] = bx+1
                self.Bot_Location[1] = by
            
            elif top_score == max(left_score, right_score, top_score, bottom_score) and top == 0:
                board[bx][by] = 20
                board[bx][by+1] = 2
                self.Bot_Location[0] = bx
                self.Bot_Location[1] = by+1

            elif bottom_score == max(left_score, right_score, top_score, bottom_score) and bottom == 0:
                board[bx][by] = 20
                board[bx][by-1] = 2
                self.Bot_Location[0] = bx
                self.Bot_Location[1] = by-1

            elif left_score == max(left_score, right_score, top_score, bottom_score) and left == 20:
                board[bx][by] = 20
                for i in range(bx-1, -1, -1):
                        if board[i][by] == 0 or board[i][by] == self.human or board[i][by] == self.humanSplash:
                            board[i+1][by] = 2
                            self.Bot_Location[0] = i+1
                            self.Bot_Location[1] = by
                            self.bot_score -= 1
                            break
                        elif i == 0:
                            board[i][by] = 2
                            self.Bot_Location[0] = i
                            self.Bot_Location[1] = by
                            self.bot_score -= 1
                            break
            elif right_score == max(left_score, right_score, top_score, bottom_score) and right == 20:
                board[bx][by] = 20
                for i in range(bx+1, 4, 1):
                        if board[i][by] == 0 or board[i][by] == self.human or board[i][by] == self.humanSplash:
                            board[i-1][by] = 2
                            self.Bot_Location[0] = i-1
                            self.Bot_Location[1] = by
                            self.bot_score -= 1
                            break
                        elif i == 4:
                            board[i][by] = 2
                            self.Bot_Location[0] = i
                            self.Bot_Location[1] = by
                            self.bot_score -= 1
                            break
            elif top_score == max(left_score, right_score, top_score, bottom_score) and top == 20:
                board[bx][by] = 20
                for j in range(by+1, 4, 1):
                        if board[bx][j] == 0 or board[bx][j] == self.human or board[bx][j] == self.humanSplash:
                            board[bx][j-1] = 2
                            self.Bot_Location[0] = bx
                            self.Bot_Location[1] = j-1
                            self.bot_score -= 1
                            break
                        elif j == 4:
                            board[bx][j] = 2
                            self.Bot_Location[0] = bx
                            self.Bot_Location[1] = j
                            self.bot_score -= 1
                            break
            elif bottom_score == max(left_score, right_score, top_score, bottom_score) and bottom == 20:
                board[bx][by] = 20
                for j in range(by-1, -1, -1):
                        if board[bx][j] == 0 or board[bx][j] == self.human or board[bx][j] == self.humanSplash:
                            board[bx][j+1] = 2
                            self.Bot_Location[0] = bx
                            self.Bot_Location[1] = j+1
                            self.bot_score -= 1
                            break
                        elif j == 0:
                            board[bx][j] = 2
                            self.Bot_Location[0] = bx
                            self.Bot_Location[1] = j
                            self.bot_score -= 1
                            break

    def on_key_press(self, key, modifiers):
        pass
            
    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.game_state == "GameMenu":
                self.game_state = "GameOn"
        
        elif self.game_state == "GameOn":
            box = [x//G_SIZE, y//G_SIZE]    #Location of box(x,y)
            if(self.is_Legal_Move(box)):
                self.update_grid(box)
                self.evaluateBoard_AI(board)
                self.bot_move()
                self.update_grid(box)
                self.evaluateBoard_AI(board)
            else: #This else will execute in case the move is illegal. 
                if self.turn == 1000:
                    self.human_score -= 1
                    self.turn = 2000
                    self.bot_move()
                    self.update_grid(box)
                    self.evaluateBoard_AI(board)

                
            
    def is_Legal_Move(self,box):
        #Clicking on grid line (Not Checking and not needed)
        #Clicking on an area out of bounds(outside the GridWorld) (Checking)
        #Moving the Snail onto opponent’s Snail or Trail of Slime (Checking)
        #Playing a move by passing an empty Grid Square (Checking)
        x = box[0]
        y = box[1]
        if x <= game_SCREEN_WIDTH and y <= game_SCREEN_HEIGHT: #Checking if clicked out side screen
            
            #The following long if is checking moving on the opponent's slime
            if self.turn == 1000 and (board[x][y] == 0 or board[x][y] == 10):
                left, right, top, bottom = 0, 0, 0, 0
               
                #--------Checking Snail is not bypassing a square Start--------------#
                try: # Using these try and except blocks to ignore index error 
                    left = board[x-1][y]
                except:
                    pass
                try:
                    right = board[x+1][y]
                except:
                    pass
                try:
                    top = board[x][y+1]
                except:
                    pass
                try:
                    bottom = board[box[0]][box[1]-1]
                except:
                    pass
                if self.turn == 1000:
                    if x == 0 and y == 4:
                        if (right == 1 or bottom == 1):
                            return True
                        return False
                    elif x == 4 and y == 0:
                        if (top == 1 or left == 1):
                            return True
                        return False
                    elif x == 4 or x == 0 or y == 0 or y == 4:
                        if x == 0:
                            if (top == 1 or bottom == 1 or right == 1):
                                return True
                            return False
                        elif x == 4:
                            if (top == 1 or bottom == 1 or left == 1):
                                return True
                            return False
                        elif y == 0:
                            if (left == 1 or top == 1 or right == 1):
                                return True
                            return False
                        elif y == 4:
                            if (left == 1 or bottom == 1 or right == 1):
                                return True
                            return False
                        else:
                            return False
                    elif (x > 0 or x < 4) and (y > 0 or y < 4):
                        if (left == 1 or right == 1 or top == 1 or bottom == 1 ):
                            return True
                        return False

                    #--------Checking Snail is not bypassing a square End--------------#
            else:
                return False


        else:
            return False

    def update_grid(self,box):
        
        """
        This function is updating backend 2d matrix and player scores.
        box[x,y] is the location where Snail needs to be placed. 
        """

        #Present Location of Bot 
        bx = self.Bot_Location[0] 
        by = self.Bot_Location[1]
        #Present Location of Human 
        hx = self.human_Location[0]
        hy = self.human_Location[1]
        #Desired Location where the mouse is clicked 
        cx = box[0]
        cy = box[1]
        #----------------------------------------------------
        if self.turn == 1000:     #-------> HUMAN's TURN <------------
            board[hx][hy] = 10    #Placing Splash on the Present human Location 
            self.human_score += 1 #Increasing Human Score     
            self.turn = 2000      #Changing Turn
            if board[cx][cy] == 10: #This will execute when the Human clicks on his Splash(Slippery Functionality for Human)
                self.human_score -= 1 #No Score should be increased if clicked on splash 
                if hx == cx and cy > hy:
                    for y in range(hy+1, 4, 1):
                        if y == 4 and board[cx][y] == 10:
                            board[cx][y] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y
                            break
                        elif board[cx][y] == 0 or board[cx][y] == 20 or board[cx][y] == 2:
                            board[cx][y-1] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y-1
                            break
                elif hx == cx and cy < hy:
                    for y in range(hy-1, -1, -1):
                        if y == 0 and board[cx][y] == 10:
                            board[cx][y] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y
                            break
                        elif board[cx][y] == 0 or board[cx][y] == 20 or board[cx][y] == 2:
                            board[cx][y+1] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y+1
                            break
                elif cx > hx and cy == hy:
                    if cx == 4:              #Right Side Corner case
                        board[cx][cy] = 1
                        self.human_Location = box
                        return
                    for x in range(cx+1, 4, 1):
                        if x == 4 and board[x][cy] == 10:
                            board[x][cy] = 1 
                            self.human_Location[0] = x
                            self.human_Location[1] = cy
                            break
                        elif board[x][cy] == 0 or board[x][cy] == 20 or board[x][cy] == 2:
                            board[x-1][cy] = 1
                            self.human_Location[0] = x-1
                            self.human_Location[1] = cy
                            break
                elif cx < hx and cy == hy:
                    if cx == 0:             #Left Side Corner case
                        board[cx][cy] = 1
                        self.human_Location = box
                        return
                    for x in range(cx-1, -1, -1):
                        if x == 0 and board[x][cy] == 10:
                            board[x][cy] = 1
                            self.human_Location[0] = x
                            self.human_Location[1] = cy
                            break
                        elif board[x][cy] == 0 or board[x][cy] == 20 or board[x][cy] == 2:
                            board[x+1][cy] = 1
                            self.human_Location[0] = x+1
                            self.human_Location[1] = cy
                            break
                elif cx == hx and cy == hy: #When Player will click on itself it will lose the turn and scores will remain the same
                    self.human_score -= 1 
                #----------------------------------------------------------------------------
                
            else:                   #This will execute When Human clicks Empty Square
                board[hx][hy] = 10
                board[cx][cy] = 1
                self.human_Location = box
                #----------------------------------------------------------------------------
                #----------------------------------------------------------------------------
        elif self.turn == 2000:      #-----> BOT's TURN <-----
            # board[bx][by] = 20       #Putting Splash on the Bot Location
            self.bot_score += 1      #Increasing Bot Score 
            self.turn = 1000         #Fliping turn       

        print("-----------------------------------------------")
        for j in range(ROWS):
            print()
            for i in range(COLUMNS):
                print(board[i][j], end="\t")
        print()
        
    def on_show(self):
        arcade.set_background_color(arcade.color.SKY_BLUE) #Background color
        
    def on_draw(self):
        arcade.start_render()

        if self.game_state == "GameMenu":
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, menuEmoji)
            arcade.draw_text("Well Come :)", SCREEN_WIDTH-400, SCREEN_HEIGHT-100,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Start Game(Click here)", SCREEN_WIDTH-400, SCREEN_HEIGHT/2-200,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
            

        elif self.game_state == "GameOn":
            
            

            # setting the background image
            arcade.draw_lrwh_rectangle_textured(0, 0, game_SCREEN_WIDTH, game_SCREEN_HEIGHT, background)
            
            #Drawing Lines for playing Snail for Front End Grid.
            for x in range (0, 600, G_SIZE):
                arcade.draw_line(0, x, 600, x, arcade.color.BLACK, 4)
            for y in range (0, 600, G_SIZE):
                arcade.draw_line(y, 0, y, 600, arcade.color.BLACK, 4)

            # arcade.draw_lrwh_rectangle_textured(0, 0, game_SCREEN_WIDTH, game_SCREEN_HEIGHT, background)
            arcade.set_background_color(arcade.color.WOOD_BROWN) #Background color
            arcade.draw_text("Human Score", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+150,
                         arcade.color.DEEP_SKY_BLUE, font_size=20, anchor_x="center")
            arcade.draw_text(str(self.human_score), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+100,
                 arcade.color.DEEP_SKY_BLUE, font_size=15, anchor_x="center")
            arcade.draw_text(str("Bot Score"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+50,
                        arcade.color.DARK_RED, font_size=20, anchor_x="center")
            arcade.draw_text(str(self.bot_score), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2),
                 arcade.color.DARK_RED, font_size=15, anchor_x="center")
            
            
            if self.turn == 1000:
                
                arcade.draw_text(str("-->Turn<--"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-50,
                        arcade.color.DEEP_SKY_BLUE, font_size=25, anchor_x="center")
                arcade.draw_text("Human", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-100,
                 arcade.color.DEEP_SKY_BLUE, font_size=20, font_name='comic', anchor_x="center")
            
            else:
                arcade.draw_text(str("-->Turn<--"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-50,
                        arcade.color.DARK_RED, font_size=25, anchor_x="center")
                arcade.draw_text("Bot", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-100,
                 arcade.color.DARK_RED, font_size=20, font_name='comic', anchor_x="center")
            
            #These for loops are maping background 2D Matrix with Front End Grid.
            for i in range(4):
                
                for j in range(4):
                    
                    if board[i][j] == 1:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, humanSnail)
                    
                    elif board[i][j] == 2:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, botSnail)
                    
                    elif board[i][j] == 10:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, HumanSplash)
                    
                    elif board[i][j] == 20:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, BotSplash)
        
        elif self.game_state == "Draw":

            arcade.set_background_color(arcade.color.BISQUE)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("It's a Draw :(", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, bold=True, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, drawEmoji)
        
        elif self.game_state == "HumanWon":
            
            arcade.set_background_color(arcade.color.DEEP_SKY_BLUE)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Human Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, humanSnail)
        
        elif self.game_state == "BotWon":
            
            arcade.set_background_color(arcade.color.LIGHT_PINK)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Bot Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, botSnail)             

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    game_view = Game()
    window.show_view(game_view)
    arcade.run()
    
main()