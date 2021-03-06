import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count:
            return self.cells

        return set()

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            return self.cells

        return set()

        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        
        return None


        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        self.cells.discard(cell)
        
        return None

        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made.
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        new_safes = set()
        new_mines = set()
        

        # Marks cell as a move that has been made.
        self.moves_made.add(cell)

        # Marks cell as safe and removes cell from any sentence in knowledge.
        if cell not in self.safes:
            self.mark_safe(cell)
   
        # Add a new sentence to the AI's knowledge base with valid surrounding cells.
        self.knowledge.append(Sentence(self.valid_surroundings(cell), count))

        # Iterates through all sentences in AI's knowledge base for new known safe or mine cells.
        for sentence in self.knowledge:
            new_safes.update(sentence.known_safes())
            new_mines.update(sentence.known_mines())

        # Marks all new safe and mine cells.
        for safe_cell in new_safes:
            self.mark_safe(safe_cell)
        for mine_cell in new_mines:
            self.mark_mine(mine_cell)

        # Removes sentences with no cells.
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

        #adds infered sentences to AI's knowledge base
        self.knowledge += self.inferences()

        return None
    
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > 0:
            for move in self.safes:
                if move not in self.moves_made:
                    return move
        
        return None

        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Stores random moves already checked.
        searched = []

        # Iterates through all posible moves in the board.
        while len(searched) <= self.height * self.width:
            move = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if move not in self.mines and move not in self.moves_made:
                print(move)
                return move
            else:
                searched.append(move)

        return None

        raise NotImplementedError

    def in_board(self, i, j):
        """
        Takes a cell's cordenates and returns:
           * True when a cell cordenates are inside the bouard.
           * False when a cell cordenates are out of the board.
        """
        # West limit crossed.
        if i < 0:
            return False
        # South limit crossed.
        if j < 0:
            return False
        # East limit crossed.
        if i >= self.width:
            return False
        # North limit crossed.
        if j >= self.height:
            return False

        return True

    def valid_surroundings(self, cell):
        """
        Returns a set of tuples with the following characteristics:
            - within board.
            - not original cell.
            - not known mine cell.
            - not a known safe cell.
        """
        valid = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and self.in_board(i, j):
                    valid.add((i, j))
        valid -= self.safes | self.moves_made

        return valid

    def inferences(self):
        """
        Returns all new posible inferences.
        """
        inferences = []
        new_sentences = []
        old_sentences = []

        # Compares each sentence in knowledge with all others to infere new sentences.
        for sentence1 in self.knowledge:
            if len(sentence1.cells) != 0:
                for sentence2 in self.knowledge:
                    if len(sentence2.cells) != 0 and sentence1 != sentence2 and sentence1.cells <= sentence2.cells:
                        inferences.append(
                            Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count)
                        )

        #Checks for repeated sentences. 
        old_sentences = [
            repeated 
            for repeated in inferences 
            if repeated in self.knowledge
        ]

        # Gets
        new_sentences  = [
            new
            for new in inferences
            if new not in old_sentences
        ]

        return new_sentences