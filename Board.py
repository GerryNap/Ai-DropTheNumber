class Board:
    def __init__(self, board, n, m):
        self.board = board
        self.n = n
        self.m = m

    def get_facts(self):
        facts = ""

        for i in range(0, self.n):
            for j in range(0, self.m):
                # FATTI: coordinata e valore
                facts += "c(" + str(i) + "," + str(j) + "," + str(self.board[i][j]) + "). "

        # FATTI: dimensioni matrice
        facts += "n(" + str(self.n) + "). m(" + str(self.m) + ")."
        
        return facts