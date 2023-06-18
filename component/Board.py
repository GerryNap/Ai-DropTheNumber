class Board:
    def __init__(self, board):
        self.board = board

    def get_cell_facts(self):
        facts = ""

        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                facts += f"cell({i},{j},{self.board[i][j]}).\n"
        
        return facts
    
    def get_size_fact(self):
        row = len(self.board)
        col = len(self.board[0])
        return f"row({row}).\ncol({col}).\n"