'''
Created on Jun 6, 2018

@author: 19ZhangA
'''

import pygame as p 
import GameEngine, Stats
import random as rand

WIDTH = HEIGHT = 504
SQ_SIZE = HEIGHT/8
MAX_FPS = 20
IMAGES = {}

def mainAI():
    icon = p.image.load('windowicon.png')
    p.init()
    p.display.set_icon(icon)
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Chess')
    screen.fill((255, 255, 255))
    clock = p.time.Clock()
    move = ''
    possibleMoves = ''
    currentRow = 0
    currentCol = 0
    promotion = False
    choice = ''
    moveR = 0
    moveC = 0
    gameOver = ''
    
    loadPieces()
    
    gameState = GameEngine.GameState()
    
    running = True
    while running:
        if gameState.whiteTurn:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                    
                #reset (r) or undo (z)  
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_r:
                        gameState.reset()
                    elif e.key == p.K_z:
                        if len(move) == 2:
                            move = ''
                            possibleMoves = ''
                        if len(gameState.moveHistory) > 0:
                            gameState.undo()
                            gameState.undo()
                                
                elif e.type == p.MOUSEBUTTONDOWN:
                    c, r = getSquareaClicked(p.mouse.get_pos())
                    location = gameState.getLocationString(c, r)
                    
                    if promotion == True:
    #                   #user console input choice
    #                     choice = input('queen, rook, bishop, or knight?')
    #                     while True: 
    #                         choice = input('queen, rook, bishop, or knight?')
    #                         if choice == 'queen' or choice == 'rook' or choice == 'bishop' or choice == 'knight':
    #                             break
                        #screen click input
                        if r == 3 and c == 3:
                            choice = 'queen'    
                        elif r == 3 and c == 4:
                            choice = 'rook'
                        elif r == 4 and c == 3:
                            choice = 'bishop'
                        elif r == 4 and c == 4:
                            choice = 'knight'    
    
                        if choice == 'queen' or choice == 'rook' or choice == 'bishop' or choice == 'knight':
                            gameState.movePiece(move)
                            if choice == 'queen':
                                if gameState.whiteTurn:
                                    gameState.board[moveR][moveC] = 'bQ'
                                else:
                                    gameState.board[moveR][moveC] = 'wQ'
                            elif choice == 'rook':
                                if gameState.whiteTurn:
                                    gameState.board[moveR][moveC] = 'bR'
                                else:
                                    gameState.board[moveR][moveC] = 'wR'
                            elif choice == 'bishop':
                                if gameState.whiteTurn:
                                    gameState.board[moveR][moveC] = 'bB'
                                else:
                                    gameState.board[moveR][moveC] = 'wB'
                            elif choice == 'knight':
                                if gameState.whiteTurn:
                                    gameState.board[moveR][moveC] = 'bN'
                                else:
                                    gameState.board[moveR][moveC] = 'wN'
                                
                            promotion = False
                            move = ''
                            possibleMoves = ''
                            choice = ''
                                    
                    else:
                        if len(move) == 0:
                            #if first click of move
                            if gameState.containsPiece(c, r) and ((gameState.whiteTurn and gameState.board[r][c][0] == 'w') or (not gameState.whiteTurn and gameState.board[r][c][0] == 'b')):
                                move += location
                                currentRow = r
                                currentCol = c
                                possibleMoves = gameState.getValidMoves(c, r)
                                
                        elif len(move) == 2:
                            #if second click of move
                            for m in possibleMoves:
                                if m == location:
                                    move += location
                            #if click on another friendly piece
                            if gameState.board[r][c][0] == gameState.board[currentRow][currentCol][0]:
                                move = location
                            currentCol = gameState.filesToCols[move[0]]
                            currentRow = gameState.ranksToRows[move[1]]
                            possibleMoves = gameState.getValidMoves(currentCol, currentRow)
                           
                        if len(move) == 4:
                            if (gameState.board[currentRow][currentCol] == 'wP' and currentRow == 1) or (gameState.board[currentRow][currentCol] == 'bP' and currentRow == 6):
                                promotion = True
                                moveC = gameState.filesToCols[move[2]]
                                moveR = gameState.ranksToRows[move[3]]                            
                                
                            if not promotion:
                                gameState.movePiece(move) 
                                move = ''
                                possibleMoves = ''
        
#         elif not gameState.whiteTurn and gameOver == 'no':
        else:
            moves = gameState.getAllMoves()
            remove = []
            for m in moves:
                if len(m) == 1:
                    remove.append(m)
            for r in remove:
                moves.remove(r)
                    
            randPiece = moves[rand.randint(0, len(moves) - 1)]
            randMove = randPiece[rand.randint(1, len(randPiece) - 1)]
            gameState.movePiece(randPiece[0] + randMove)
            
        #draw board, pieces, highlight moves
        drawBoard(screen)          
        if len(move) == 2:
            for m in gameState.getValidMoves(currentCol, currentRow):
                p.draw.rect(screen, p.Color(0, 255, 0), p.Rect(gameState.filesToCols[m[0]]*SQ_SIZE, gameState.ranksToRows[m[1]]*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)     
            p.draw.rect(screen, p.Color(255, 0, 0), p.Rect(gameState.filesToCols[move[0]]*SQ_SIZE, gameState.ranksToRows[move[1]]*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)     
        drawPieces(screen, gameState.board)
        
        #draw pawn promotion screen
        if promotion:
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - SQ_SIZE, HEIGHT/2 - SQ_SIZE, SQ_SIZE*2, SQ_SIZE*2))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - SQ_SIZE, HEIGHT/2 - SQ_SIZE, SQ_SIZE*2, SQ_SIZE*2), 1)
            if gameState.whiteTurn:
                screen.blit(IMAGES['wQ'], p.Rect(3*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['wR'], p.Rect(4*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['wB'], p.Rect(3*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['wN'], p.Rect(4*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                screen.blit(IMAGES['bQ'], p.Rect(3*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['bR'], p.Rect(4*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['bB'], p.Rect(3*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['bN'], p.Rect(4*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        #check if game over
        gameOver = ''    
        if gameState.whiteTurn:
            #if white has no moves
            for r in range(len(gameState.board)):
                for c in range(len(gameState.board)):
                    if gameState.board[r][c][0] == 'w':
                        if len(gameState.getValidMoves(c, r)) != 0:
                            gameOver = 'no'
            #check stalemate or win
            gameState.whiteTurn = not gameState.whiteTurn
            if gameOver != 'no' and gameState.inCheck() == True:
                gameOver = 'black'
            elif gameOver != 'no':
                gameOver = 'stalemate'
            gameState.whiteTurn = not gameState.whiteTurn
        else:
            #if black has no moves
            for r in range(len(gameState.board)):
                for c in range(len(gameState.board)):
                    if gameState.board[r][c][0] == 'b':
                        if len(gameState.getValidMoves(c, r)) != 0:
                            gameOver = 'no'
            #check stalemate or win
            gameState.whiteTurn = not gameState.whiteTurn
            if gameOver != 'no' and gameState.inCheck() == True:
                gameOver = 'white'
            elif gameOver != 'no':
                gameOver = 'stalemate'
            gameState.whiteTurn = not gameState.whiteTurn
        
        #draw game over screen      
        if gameOver == 'black':
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            font = p.font.SysFont('Dubai', 48)
            text = [font.render('Checkmate, Black wins!', 0, p.Color('black')), font.render('Press r to restart or z to undo', 0, p.Color('black'))]
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height), 1)
            for i in range(len(text)):                                                                                                              
                screen.blit(text[i], p.Rect(WIDTH/2 - (text[i].get_rect().width)/2, HEIGHT/2 + (i - 1)*(text[i].get_rect().height), text[i].get_rect().width, text[i].get_rect().height))
        elif gameOver == 'white':
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            font = p.font.SysFont('Dubai', 32)
            text = [font.render('Checkmate, White wins!', 0, p.Color('black')), font.render('Press r to restart or z to undo', 0, p.Color('black'))]
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height), 1)
            for i in range(len(text)):                                                                                                              
                screen.blit(text[i], p.Rect(WIDTH/2 - (text[i].get_rect().width)/2, HEIGHT/2 + (i - 1)*(text[i].get_rect().height), text[i].get_rect().width, text[i].get_rect().height))
        elif gameOver == 'stalemate':
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            font = p.font.SysFont('Dubai', 32)
            text = [font.render('Stalemate', 0, p.Color('black')), font.render('Press r to restart or z to undo', 0, p.Color('black'))]
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height), 1)
            for i in range(len(text)):                                                                                                              
                screen.blit(text[i], p.Rect(WIDTH/2 - (text[i].get_rect().width)/2, HEIGHT/2 + (i - 1)*(text[i].get_rect().height), text[i].get_rect().width, text[i].get_rect().height))
                
        clock.tick(MAX_FPS)
        p.display.flip()


def main():
    icon = p.image.load('windowicon.png')
    p.init()
    p.display.set_icon(icon)
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Chess')
    screen.fill((255, 255, 255))
    clock = p.time.Clock()
    move = ''
    possibleMoves = ''
    currentRow = 0
    currentCol = 0
    promotion = False
    choice = ''
    moveR = 0
    moveC = 0
    gameOver = ''
    
    loadPieces()
    
    
    gameState = GameEngine.GameState()
    
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            #reset (r) or undo (z)  
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    gameState.reset()
                elif e.key == p.K_z:
                    if len(move) == 2:
                        move = ''
                        possibleMoves = ''
                    if len(gameState.moveHistory) > 0:
                        gameState.undo()
                            
            elif e.type == p.MOUSEBUTTONDOWN:
                c, r = getSquareaClicked(p.mouse.get_pos())
                location = gameState.getLocationString(c, r)
                
                if promotion == True:
#                   #user console input choice
#                     choice = input('queen, rook, bishop, or knight?')
#                     while True: 
#                         choice = input('queen, rook, bishop, or knight?')
#                         if choice == 'queen' or choice == 'rook' or choice == 'bishop' or choice == 'knight':
#                             break
                    #screen click input
                    if r == 3 and c == 3:
                        choice = 'queen'    
                    elif r == 3 and c == 4:
                        choice = 'rook'
                    elif r == 4 and c == 3:
                        choice = 'bishop'
                    elif r == 4 and c == 4:
                        choice = 'knight'    

                    if choice == 'queen' or choice == 'rook' or choice == 'bishop' or choice == 'knight':
                        gameState.movePiece(move)
                        if choice == 'queen':
                            if gameState.whiteTurn:
                                gameState.board[moveR][moveC] = 'bQ'
                            else:
                                gameState.board[moveR][moveC] = 'wQ'
                        elif choice == 'rook':
                            if gameState.whiteTurn:
                                gameState.board[moveR][moveC] = 'bR'
                            else:
                                gameState.board[moveR][moveC] = 'wR'
                        elif choice == 'bishop':
                            if gameState.whiteTurn:
                                gameState.board[moveR][moveC] = 'bB'
                            else:
                                gameState.board[moveR][moveC] = 'wB'
                        elif choice == 'knight':
                            if gameState.whiteTurn:
                                gameState.board[moveR][moveC] = 'bN'
                            else:
                                gameState.board[moveR][moveC] = 'wN'
                            
                        promotion = False
                        move = ''
                        possibleMoves = ''
                        choice = ''
                                
                else:
                    if len(move) == 0:
                        #if first click of move
                        if gameState.containsPiece(c, r) and ((gameState.whiteTurn and gameState.board[r][c][0] == 'w') or (not gameState.whiteTurn and gameState.board[r][c][0] == 'b')):
                            move += location
                            currentRow = r
                            currentCol = c
                            possibleMoves = gameState.getValidMoves(c, r)
                            
                    elif len(move) == 2:
                        #if second click of move
                        for m in possibleMoves:
                            if m == location:
                                move += location
                        #if click on another friendly piece
                        if gameState.board[r][c][0] == gameState.board[currentRow][currentCol][0]:
                            move = location
                        currentCol = gameState.filesToCols[move[0]]
                        currentRow = gameState.ranksToRows[move[1]]
                        possibleMoves = gameState.getValidMoves(currentCol, currentRow)
                       
                    if len(move) == 4:
                        if (gameState.board[currentRow][currentCol] == 'wP' and currentRow == 1) or (gameState.board[currentRow][currentCol] == 'bP' and currentRow == 6):
                            promotion = True
                            moveC = gameState.filesToCols[move[2]]
                            moveR = gameState.ranksToRows[move[3]]                            
                            
                        if not promotion:
                            gameState.movePiece(move) 
                            move = ''
                            possibleMoves = ''
        
        #draw board, pieces, highlight moves
        drawBoard(screen)          
        if len(move) == 2:
            for m in gameState.getValidMoves(currentCol, currentRow):
                p.draw.rect(screen, p.Color(0, 255, 0), p.Rect(gameState.filesToCols[m[0]]*SQ_SIZE, gameState.ranksToRows[m[1]]*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)     
            p.draw.rect(screen, p.Color(255, 0, 0), p.Rect(gameState.filesToCols[move[0]]*SQ_SIZE, gameState.ranksToRows[move[1]]*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)     
        drawPieces(screen, gameState.board)
        
        #draw pawn promotion screen
        if promotion:
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - SQ_SIZE, HEIGHT/2 - SQ_SIZE, SQ_SIZE*2, SQ_SIZE*2))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - SQ_SIZE, HEIGHT/2 - SQ_SIZE, SQ_SIZE*2, SQ_SIZE*2), 1)
            if gameState.whiteTurn:
                screen.blit(IMAGES['wQ'], p.Rect(3*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['wR'], p.Rect(4*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['wB'], p.Rect(3*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['wN'], p.Rect(4*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                screen.blit(IMAGES['bQ'], p.Rect(3*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['bR'], p.Rect(4*SQ_SIZE, 3*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['bB'], p.Rect(3*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES['bN'], p.Rect(4*SQ_SIZE, 4*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        #check if game over
        gameOver = ''    
        if gameState.whiteTurn:
            #if white has no moves
            for r in range(len(gameState.board)):
                for c in range(len(gameState.board)):
                    if gameState.board[r][c][0] == 'w':
                        if len(gameState.getValidMoves(c, r)) != 0:
                            gameOver = 'no'
            #check stalemate or win
            gameState.whiteTurn = not gameState.whiteTurn
            if gameOver != 'no' and gameState.inCheck() == True:
                gameOver = 'black'
            elif gameOver != 'no':
                gameOver = 'stalemate'
            gameState.whiteTurn = not gameState.whiteTurn
        else:
            #if black has no moves
            for r in range(len(gameState.board)):
                for c in range(len(gameState.board)):
                    if gameState.board[r][c][0] == 'b':
                        if len(gameState.getValidMoves(c, r)) != 0:
                            gameOver = 'no'
            #check stalemate or win
            gameState.whiteTurn = not gameState.whiteTurn
            if gameOver != 'no' and gameState.inCheck() == True:
                gameOver = 'white'
            elif gameOver != 'no':
                gameOver = 'stalemate'
            gameState.whiteTurn = not gameState.whiteTurn
        
        #draw game over screen      
        if gameOver == 'black':
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            font = p.font.SysFont('Dubai', 48)
            text = [font.render('Checkmate, Black wins!', 0, p.Color('black')), font.render('Press r to restart or z to undo', 0, p.Color('black'))]
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height), 1)
            for i in range(len(text)):                                                                                                              
                screen.blit(text[i], p.Rect(WIDTH/2 - (text[i].get_rect().width)/2, HEIGHT/2 + (i - 1)*(text[i].get_rect().height), text[i].get_rect().width, text[i].get_rect().height))
        elif gameOver == 'white':
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            font = p.font.SysFont('Dubai', 32)
            text = [font.render('Checkmate, White wins!', 0, p.Color('black')), font.render('Press r to restart or z to undo', 0, p.Color('black'))]
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height), 1)
            for i in range(len(text)):                                                                                                              
                screen.blit(text[i], p.Rect(WIDTH/2 - (text[i].get_rect().width)/2, HEIGHT/2 + (i - 1)*(text[i].get_rect().height), text[i].get_rect().width, text[i].get_rect().height))
        elif gameOver == 'stalemate':
            s = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            s.fill((255, 255, 255, 128))
            screen.blit(s, (0, 0))
            font = p.font.SysFont('Dubai', 32)
            text = [font.render('Stalemate', 0, p.Color('black')), font.render('Press r to restart or z to undo', 0, p.Color('black'))]
            p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height))
            p.draw.rect(screen, p.Color(0, 0, 0), p.Rect(WIDTH/2 - text[1].get_rect().width/2, HEIGHT/2 - text[1].get_rect().height, text[1].get_rect().width, 2*text[1].get_rect().height), 1)
            for i in range(len(text)):                                                                                                              
                screen.blit(text[i], p.Rect(WIDTH/2 - (text[i].get_rect().width)/2, HEIGHT/2 + (i - 1)*(text[i].get_rect().height), text[i].get_rect().width, text[i].get_rect().height))
                
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawBoard(screen):
    for i in range(8):
        for k in range(8):
            if k % 2 == i % 2:
                p.draw.rect(screen, p.Color(255, 255, 255), p.Rect(k*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, p.Color(150, 150, 150), p.Rect(k*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def loadPieces():
    global IMAGES
    pieces = ['wP', 'wB', 'wN', 'wR', 'wQ', 'wK', 'bP', 'bB', 'bN', 'bR', 'bQ', 'bK']
    imageNames = []
    for piece in pieces:
        imageNames.append('images/' + piece + '.png')
    for i in range(len(pieces)):
        IMAGES[pieces[i]] = p.image.load(imageNames[i])
    
def drawPieces(screen, board):
    for c in range(len(board)):
        for r in range(len(board)):
            if board[r][c] != '--':
                screen.blit(IMAGES[board[r][c]], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def getSquareaClicked(coords):
    c = coords[0]//SQ_SIZE
    r = coords[1]//SQ_SIZE
    return int(c), int(r)

#comment/uncomment for Player v Player or Player v AI          
# mainAI()
main()

