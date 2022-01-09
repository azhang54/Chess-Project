
'''
Created on May 17, 2018

@author: 19ZhangA
'''

class GameState(object):
    '''
    Object to keep track of current locations of pieces on the
    board, move history including captured pieces, possible
    valid moves, whose turn it is, etc.
    '''
    #dictionaries
    colsToFiles = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    filesToCols = {v:k for k,v in colsToFiles.items()}
    rowsToRanks = {0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1'}
    ranksToRows = {v:k for k,v in rowsToRanks.items()}
    
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        
        self.moveHistory = []
        self.whiteTurn = True #False if black turn
        self.whiteCaptured = []
        self.blackCaptured = []
        
    def reset(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.whiteTurn = True
        self.moveHistory = []
        self.whiteCaptured = []
        self.blackCaptured = []
     
    def undo(self):
        self.whiteTurn = not self.whiteTurn
        
        #undo castling
        if self.moveHistory[len(self.moveHistory) - 1] == 'wkcastle':
            self.board[7][4] = 'wK'
            self.board[7][5] = '--'
            self.board[7][6] = '--'
            self.board[7][7] = 'wR'
        elif self.moveHistory[len(self.moveHistory) - 1] == 'wqcastle':
            self.board[7][4] = 'wK'
            self.board[7][3] = '--'
            self.board[7][2] = '--'
            self.board[7][0] = 'wR'
        elif self.moveHistory[len(self.moveHistory) - 1] == 'bkcastle':
            self.board[0][4] = 'bK'
            self.board[0][5] = '--'
            self.board[0][6] = '--'
            self.board[0][7] = 'bR'
        elif self.moveHistory[len(self.moveHistory) - 1] == 'bqcastle':
            self.board[0][4] = 'bK'
            self.board[0][3] = '--'
            self.board[0][2] = '--'
            self.board[0][0] = 'bR'
        
        else:
            x2 = self.filesToCols[self.moveHistory[len(self.moveHistory) - 1][2]]
            y2 = self.ranksToRows[self.moveHistory[len(self.moveHistory) - 1][3]]
            x1 = self.filesToCols[self.moveHistory[len(self.moveHistory) - 1][0]]
            y1 = self.ranksToRows[self.moveHistory[len(self.moveHistory) - 1][1]]
            
            self.board[y1][x1] = self.board[y2][x2]
            self.board[y2][x2] = self.moveHistory[len(self.moveHistory) - 1][4:6]
            #en passant undo
            if self.moveHistory[len(self.moveHistory) - 1][8:10] == 'ep':
                if self.whiteTurn:
                    self.board[y1][x2] = 'bP'
                else:
                    self.board[y1][x2] = 'wP'
            elif self.moveHistory[len(self.moveHistory) - 1][7] == 'P':
                if self.whiteTurn and y2 == 0:
                    self.board[y1][x1] = 'wP'
                elif not self.whiteTurn and y2 == 7:
                    self.board[y1][x1] = 'bP'
            
        self.moveHistory.pop()
     
    def movePiece(self, moveString):
        #move for castling
        if self.board[7][4] == 'wK' and moveString == 'e1g1':
            self.board[7][4] = '--'
            self.board[7][5] = 'wR'
            self.board[7][6] = 'wK'
            self.board[7][7] = '--'
            self.moveHistory.append('wkcastle')
        elif self.board[7][4] == 'wK' and moveString == 'e1c1':
            self.board[7][4] = '--'
            self.board[7][3] = 'wR'
            self.board[7][2] = 'wK'
            self.board[7][0] = '--'
            self.moveHistory.append('wqcastle')
        elif self.board[0][4] == 'bK' and moveString == 'e8g8':
            self.board[0][4] = '--'
            self.board[0][5] = 'bR'
            self.board[0][6] = 'bK'
            self.board[0][7] = '--'
            self.moveHistory.append('bkcastle')
        elif self.board[0][4] == 'bK' and moveString == 'e8c8':
            self.board[0][4] = '--'
            self.board[0][3] = 'bR'
            self.board[0][2] = 'bK'
            self.board[0][0] = '--'
            self.moveHistory.append('bqcastle')
            
        else:
            x1 = self.filesToCols[moveString[0]]
            y1 =  self.ranksToRows[moveString[1]]
            x2 = self.filesToCols[moveString[2]]
            y2 = self.ranksToRows[moveString[3]]
            
            piece = self.board[y1][x1]
            captured = self.board[y2][x2] 
            moveString += captured
            enpassant = False
            
            #en passant and promotion
            if piece == 'wP':
                if (x2 == x1 + 1 and self.board[y1][x2] == 'bP' and self.board[y2][x2] == '--') or (x2 == x1 - 1 and self.board[y1][x2] == 'bP' and self.board[y2][x2] == '--'):
                    captured = self.board[y1][x2]
                    enpassant = True
                    
            elif piece == 'bP':
                if (x2 == x1 + 1 and self.board[y1][x2] == 'wP' and self.board[y2][x2] == '--') or (x2 == x1 - 1 and self.board[y1][x2] == 'wP' and self.board[y2][x2] == '--'):
                    captured = self.board[y1][x2]
                    enpassant = True
                    
            self.moveHistory.append(moveString + piece)
            
            if captured != '--':
                if captured[0] == 'w':
                    self.whiteCaptured.append(captured)
                else:
                    self.blackCaptured.append(captured)
                    
            if enpassant == True:
                self.moveHistory[len(self.moveHistory) - 1] = moveString + piece + 'ep'
                self.board[y2][x2] = piece
                self.board[y1][x1] = '--'
                self.board[y1][x2] = '--'
            else:
                self.board[y2][x2] = piece
                self.board[y1][x1] = '--'
        self.whiteTurn = not self.whiteTurn
        
    #given mouse x and y, returns chess notation of location
    def getLocationString(self, col, row):
        return self.colsToFiles[col] + self.rowsToRanks[row]
    
    def containsPiece(self, col, row):
        if self.getSquare(col, row) == '--':
            return False
        return True
    
    #returns value of a square - '--' if empty, otherwise name of piece
    def getSquare(self, col, row):
        location = self.getLocationString(col, row)
        return self.board[self.ranksToRows[location[1]]][self.filesToCols[location[0]]]
    
    def getAvailableMoves(self, col, row):
        availableMoves = []
        b = self.board
        #white pawn
        if self.getSquare(col, row) == 'wP':
            if b[row - 1][col] == '--':
                availableMoves.append(self.getLocationString(col, row - 1))
                if row == 6:
                    if b[row - 2][col] == '--':
                        availableMoves.append(self.getLocationString(col, row - 2))
            
            if col > 0:
                x2 = self.colsToFiles[col - 1]
                if b[row - 1][col - 1][0] == 'b':
                    availableMoves.append(self.getLocationString(col - 1, row - 1))
                if row == 3 and self.moveHistory[len(self.moveHistory) - 1][0:4] == x2 + '7' + x2 + '5':
                    availableMoves.append(self.getLocationString(col - 1, row - 1))
            if col < 7:
                x = self.colsToFiles[col + 1]
                if b[row - 1][col + 1][0] == 'b':
                    availableMoves.append(self.getLocationString(col + 1, row - 1))
                if row == 3 and self.moveHistory[len(self.moveHistory) - 1][0:4] == x + '7' + x + '5':
                    availableMoves.append(self.getLocationString(col + 1, row - 1))
                                 
        #black pawn                
        elif self.getSquare(col, row) == 'bP':
            if b[row + 1][col] == '--':
                availableMoves.append(self.getLocationString(col, row + 1))
                if row == 1:
                    if b[row + 2][col] == '--':
                        availableMoves.append(self.getLocationString(col, row + 2))
            if col > 0:
                x2 = self.colsToFiles[col - 1]
                if b[row + 1][col - 1][0] == 'w':
                    availableMoves.append(self.getLocationString(col - 1, row + 1))
                if row == 4 and self.moveHistory[len(self.moveHistory) - 1][0:4] == x2 + '2' + x2 + '4':
                    availableMoves.append(self.getLocationString(col - 1, row + 1))
            if col < 7:
                x = self.colsToFiles[col + 1]
                if b[row + 1][col + 1][0] == 'w':
                    availableMoves.append(self.getLocationString(col + 1, row + 1))
                if row == 4 and self.moveHistory[len(self.moveHistory) - 1][0:4] == x + '2' + x + '4':
                    availableMoves.append(self.getLocationString(col + 1, row + 1))
            
        #knight
        elif self.getSquare(col, row)[1] == 'N':
            if self.onBoard(col + 2, row + 1) and (b[row + 1][col + 2] == '--' or b[row + 1][col + 2][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col + 2, row + 1))
            if self.onBoard(col + 2, row - 1) and (b[row - 1][col + 2] == '--' or b[row - 1][col + 2][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col + 2, row - 1))
            if self.onBoard(col - 2, row + 1) and (b[row + 1][col - 2] == '--' or b[row + 1][col - 2][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col - 2, row + 1))
            if self.onBoard(col - 2, row - 1) and (b[row - 1][col - 2] == '--' or b[row - 1][col - 2][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col - 2, row - 1))
            if self.onBoard(col + 1, row + 2) and (b[row + 2][col + 1] == '--' or b[row + 2][col + 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col + 1, row + 2))
            if self.onBoard(col + 1, row - 2) and (b[row - 2][col + 1] == '--' or b[row - 2][col + 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col + 1, row - 2))
            if self.onBoard(col - 1, row  + 2) and (b[row  + 2][col - 1] == '--' or b[row  + 2][col - 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col - 1, row  + 2))
            if self.onBoard(col - 1, row  - 2) and (b[row  - 2][col - 1] == '--' or b[row  - 2][col - 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col - 1, row  - 2)) 
              
        #bishop
        elif self.getSquare(col, row)[1] == 'B':
            for move in self.checkDiagonals(col, row):
                availableMoves.append(move)
        
        #rook
        elif self.getSquare(col, row)[1] == 'R':
            for move in self.checkVertAndHor(col, row):
                availableMoves.append(move)
        
        #queen
        elif self.getSquare(col, row)[1] == 'Q':
            for move in self.checkDiagonals(col, row):
                availableMoves.append(move)
            for move in self.checkVertAndHor(col, row):
                availableMoves.append(move)
        
        #king
        elif self.getSquare(col, row)[1] == 'K':
            if self.onBoard(col + 1, row + 1) and (b[row + 1][col + 1] == '--' or b[row + 1][col + 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col + 1, row + 1))
            if self.onBoard(col + 1, row - 1) and (b[row - 1][col + 1] == '--' or b[row - 1][col + 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col + 1, row - 1))
            if self.onBoard(col - 1, row + 1) and (b[row + 1][col - 1] == '--' or b[row + 1][col - 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col - 1, row + 1))
            if self.onBoard(col - 1, row - 1) and (b[row - 1][col - 1] == '--' or b[row - 1][col - 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col - 1, row - 1))
            if self.onBoard(col + 1, row) and (b[row][col + 1] == '--' or b[row][col + 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col + 1, row))
            if self.onBoard(col - 1, row) and (b[row][col - 1] == '--' or b[row][col - 1][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col - 1, row))
            if self.onBoard(col, row  + 1) and (b[row  + 1][col] == '--' or b[row  + 1][col][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col, row  + 1))
            if self.onBoard(col, row  - 1) and (b[row  - 1][col] == '--' or b[row  - 1][col][0] != self.getSquare(col, row)[0]):
                availableMoves.append(self.getLocationString(col, row  - 1))
                
            #castling
            kingMove = False
            rightRookMove = False
            leftRookMove = False
            
            if self.whiteTurn:
                for m in self.moveHistory:
                    if m[6:8] == 'wK': #check for white king move
                        kingMove = True
                    #king side
                    if m[0:2] == 'h1': #check for bottom right rook move
                        rightRookMove = True
                    #queen side
                    if m[0:2] == 'a1': #check bottom left
                        leftRookMove = True
                #king side
                if self.board[7][6] == '--' and self.board[7][5] == '--' and kingMove == False and rightRookMove == False:
                    self.movePiece(self.colsToFiles[col] + self.rowsToRanks[row] + self.colsToFiles[col + 1] + self.rowsToRanks[row])
                    if not self.inCheck():
                        availableMoves.append(self.getLocationString(col + 2, row))
                    self.undo()
                #queen side    
                if self.board[7][3] == '--' and self.board[7][2] == '--' and self.board[7][1] == '--' and kingMove == False and leftRookMove == False:
                    self.movePiece(self.colsToFiles[col] + self.rowsToRanks[row] + self.colsToFiles[col - 1] + self.rowsToRanks[row])
                    if not self.inCheck():
                        availableMoves.append(self.getLocationString(col - 2, row))
                    self.undo()

            else:
                for m in self.moveHistory:
                    if m[6:8] == 'bK': #check for white king move
                        kingMove = True
                    #king side
                    if m[0:2] == 'h8': #check for top right rook move
                        rightRookMove = True
                    #queen side
                    if m[0:2] == 'a8': #check top left
                        leftRookMove = True
                #king side
                if self.board[0][6] == '--' and self.board[0][5] == '--' and kingMove == False and rightRookMove == False:
                    self.movePiece(self.colsToFiles[col] + self.rowsToRanks[row] + self.colsToFiles[col + 1] + self.rowsToRanks[row])
                    if not self.inCheck():
                        availableMoves.append(self.getLocationString(col + 2, row))
                    self.undo()
                #queen side    
                if self.board[0][3] == '--' and self.board[0][2] == '--' and self.board[0][1] == '--' and kingMove == False and leftRookMove == False:
                    self.movePiece(self.colsToFiles[col] + self.rowsToRanks[row] + self.colsToFiles[col - 1] + self.rowsToRanks[row])
                    if not self.inCheck():
                        availableMoves.append(self.getLocationString(col - 2, row))
                    self.undo()
                      
        return availableMoves
    
    def getValidMoves(self, col, row):
        validMoves = []
        moves = []
        for move in self.getAvailableMoves(col, row):
            moves.append(self.colsToFiles[col] + self.rowsToRanks[row] + move)
            
        for move in moves:
            self.movePiece(move)
            if self.inCheck():
                self.undo()
            else:
                validMoves.append(move[2:4])
                self.undo()
        return validMoves
    
    def checkVertAndHor(self, col, row):
        availableMoves = []
        
        r = row
        while (r > 0): #up
            if self.board[r - 1][col] == '--': #empty
                availableMoves.append(self.getLocationString(col, r - 1))
            elif self.board[r - 1][col][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(col, r - 1))
                break
            else: #friendly piece
                break
            r -= 1
            
        r = row    
        while (r < 7): #down
            if self.board[r + 1][col] == '--': #empty
                availableMoves.append(self.getLocationString(col, r + 1))
            elif self.board[r + 1][col][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(col, r + 1))
                break
            else: #friendly piece
                break
            r += 1
            
        c = col    
        while (c > 0): #left
            if self.board[row][c - 1] == '--': #empty
                availableMoves.append(self.getLocationString(c - 1, row))
            elif self.board[row][c - 1][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(c - 1, row))
                break
            else: #friendly piece
                break
            c -= 1
            
        c = col
        while (c < 7): #right
            if self.board[row][c + 1] == '--': #empty
                availableMoves.append(self.getLocationString(c + 1, row))
            elif self.board[row][c + 1][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(c + 1, row))
                break
            else: #friendly piece
                break
            c += 1
        return availableMoves
            
    def checkDiagonals(self, col, row):
        availableMoves = []
        
        c = col
        r = row
        while (c > 0 and r > 0): #up and left
            if self.board[r - 1][c - 1] == '--': #empty
                availableMoves.append(self.getLocationString(c - 1, r - 1))
            elif self.board[r - 1][c - 1][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(c - 1, r - 1))
                break
            else: #friendly piece
                break
            c -= 1
            r -= 1
        
        c = col
        r = row
        while (c < 7 and r > 0): #up and right
            if self.board[r - 1][c + 1] == '--': #empty
                availableMoves.append(self.getLocationString(c + 1, r - 1))
            elif self.board[r - 1][c + 1][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(c + 1, r - 1))
                break
            else: #friendly piece
                break
            c += 1
            r -= 1
        
        c = col
        r = row
        while (c > 0 and r < 7): #down and left
            if self.board[r + 1][c - 1] == '--': #empty
                availableMoves.append(self.getLocationString(c - 1, r + 1))
            elif self.board[r + 1][c - 1][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(c - 1, r + 1))
                break
            else: #friendly piece
                break
            c -= 1
            r += 1
            
        c = col
        r = row
        while (c < 7 and r < 7): #down and right
            if self.board[r + 1][c + 1] == '--': #empty
                availableMoves.append(self.getLocationString(c + 1, r + 1))
            elif self.board[r + 1][c + 1][0] != self.board[row][col][0]: #enemy piece
                availableMoves.append(self.getLocationString(c + 1, r + 1))
                break
            else: #friendly piece
                break
            c += 1
            r += 1
            
        return availableMoves
                
    
    def onBoard(self, col, row):
        if 0 <= col <= 7 and 0 <= row <= 7:
            return True
        return False
    
    
    def inCheck(self):
        whitePieces, blackPieces = self.getPieces()
        if self.whiteTurn:
            for piece in whitePieces:
                moves = self.getAvailableMoves(piece[1], piece[0])
                for m in moves:
                    if self.board[self.ranksToRows[m[1]]][self.filesToCols[m[0]]] == 'bK':
                        return True
        else:
            for piece in blackPieces:
                moves = self.getAvailableMoves(piece[1], piece[0])
                for m in moves:
                    if self.board[self.ranksToRows[m[1]]][self.filesToCols[m[0]]] == 'wK':
                        return True
        return False
    
    def pieceUnderAttack(self, col, row):
        whitePieces, blackPieces = self.getPieces()
        if self.whiteTurn:
            for piece in whitePieces:
                moves = self.getAvailableMoves(piece[1], piece[0])
                for m in moves:
                    if self.ranksToRows[m[1]] == row and self.filesToCols[m[0]] == col:
                        return True
        else:
            for piece in blackPieces:
                moves = self.getAvailableMoves(piece[1], piece[0])
                for m in moves:
                    if self.ranksToRows[m[1]] == row and self.filesToCols[m[0]] == col:
                        return True
        return False
    
    def getPieces(self):
        whitePieces = []
        blackPieces = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c][0] == 'w':
                    whitePieces.append([r, c])
                elif self.board[r][c][0] == 'b':
                    blackPieces.append([r, c])
                    
        return whitePieces, blackPieces
    
    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c][0] == 'b':
                    pieceMoves = self.getValidMoves(c, r)
                    pieceMoves.insert(0, self.colsToFiles[c] + self.rowsToRanks[r])
                    moves.append(pieceMoves)
        return moves
    
#     def evaluate
    
    
    
    
    
    
    
    
    