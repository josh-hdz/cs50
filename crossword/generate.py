import sys
import copy
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Rem
         any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Iterates through all the variables(keys) in domains(dictionary). 
        for var in self.domains:
            wasteland = set() # Holds values out of domain.

            # Iterates through all items in the domain of each variable(keys).
            for word in self.domains[var]:
                if len(word) != var.length:
                    wasteland.add(word)

            # Updates domain.
            self.domains[var] -= wasteland

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        wasteland = self.find_conflict(x, y)
        
        if len(wasteland) == 0:
            revision = False
        else:
            revision = True

        # Updates x's domin to comply with arc consistency.
        self.domains[x] -= wasteland

        return revision 

        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            q = self.create_queue()
        else:
            q = arcs

        while len(q) > 0:
            x, y, q = self.dequeue(q)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                neighbors = self.crossword.neighbors(x)
                neighbors.remove(y)
                for neighbor in neighbors:
                    q.append((neighbor, x))
        
        return True
        
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        if len(assignment) == len(self.crossword.variables):
            for var in assignment:
                if len(assignment[var]) == 0:
                    return False

            return True
        return False

        raise NotImplementedError


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Ensures all answeres comply with legth for assigned variable.
        for variable in assignment:
            if variable.length != len(assignment[variable]):
                return False
        
        # Searches for replicas in assignmet.
        for current in assignment.values():
            ans = set(word for word in assignment.values())
            current = set((current,))
            ans.difference_update(current)
            if len(ans) != len(assignment) - 1:
                return False

        # Ensures arc consistant with assigned variables in assignment.
        for word in assignment:
            for neighbor in self.crossword.neighbors(word):
                if neighbor in assignment.keys():
                    intersect = self.crossword.overlaps[word, neighbor]
                    if assignment[word][intersect[0]] != assignment[neighbor][intersect[1]]:
                      return False

        return True

        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        domain = copy.deepcopy(list(self.domains[var]))
        self.quickSort(domain, var, 0, len(domain) - 1, assignment)
        return domain

        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Popuates list with unassigned variables.
        not_used = [
            var
            for var in self.crossword.variables
            if var not in assignment
        ]
        choosen = [not_used[0]]

        # Finds smallest unassigned variable's domain size and populates list with such varible.  
        for var in not_used:
            if len(self.domains[var]) < len(self.domains[choosen[0]]):
                choosen.clear()
                choosen.append(var)

        # Populates with unassigned variables with equal domain size.
        choosen += [
            var
            for var in not_used
            if var != choosen[0] and len(self.domains[var]) == len(self.domains[choosen[0]])
        ]

        # iterates through `choosen` to get the variable with the most neighbors.
        if len(choosen) > 1:
            for var in choosen:
                for compare in choosen:
                    if len(self.crossword.neighbors(compare)) > len(self.crossword.neighbors(var)):
                        choosen.remove(var)
                        choosen.remove(compare)
                        choosen.insert(0, compare)
                        break

        return choosen[0]


        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)

                if result is not None:
                    return assignment
            assignment.pop(var)

        return None

        raise NotImplementedError

    def create_queue(self):
        """
        OUTPUT:
            - q: list.

        creates a list(q) with all posible arcs 
        """
        q = []

        # Populates queue(q) with all posible arcs.
        for variable in self.crossword.variables:
            for posible in self.crossword.variables:
                if variable != posible and self.crossword.overlaps[variable,posible] is not None:
                    q.append([variable,posible])

        # find and removes replicates in queue(q).
        # for arc in q:
        #     for rev in q:
        #         if arc != rev and arc == rev[::-1]:
        #             q.remove(rev)

        # Converts q's items to tuples.
        q = [tuple(arc) for arc in q]
        
        return q

    def dequeue(self, q):
        """
        Returns two variables(x,y) that overlap found in queue(q) 
        and an updated version of queue(q).
        """
        arc_pair = q[:1]
        x = arc_pair[0][0]
        y = arc_pair[0][1]

        #Removes 1st item in queue(q).
        q = q[1:] 

        return x, y, q

    def find_conflict(self, x, y):
        """
        INPUT:
            - x: Variable object.
            - y: Variable object.

        Output:
            - wasteland: set.

        finds all words in x's domain that create conflict. Returns a
        set(wasteland) with such words.
        """

        intersect = self.crossword.overlaps[x, y]
        wasteland = set()
        friend_word = {
            word: False
            for word in self.domains[x]
        }

        # Iterates throguh all words in x's domain
        for word_x in self.domains[x]:
            
            # Iterates through y's domain marking words in x's domain that do not create conflict.
            for word_y in self.domains[y]:
                if word_x[intersect[0]] == word_y[intersect[1]]:
                    friend_word[word_x] = True
                    break
            
        # Populates wasteland with words not marked.
        for word in friend_word:
            if not friend_word[word]:
                wasteland.add(word)
                    
        return wasteland

    def quickSort(self, domain, var, low, high, assignment):
        """
        INPUT: 
            - domain: list.
            - var: Variable object.
            - low: int.
            - high: int.
            - assignment: dictionary.

        Orders the given list(domain) in acending order for number of future
        conflicts a word in such list may create.
        """
        
        if low < high:
            # pi ---> partitioning index 
            pi = self.partition(domain, var, low,high, assignment)  
            self.quickSort(domain, var, low, pi - 1, assignment) 
            self.quickSort(domain, var, pi + 1, high, assignment)


    def partition(self, domain, var, low, high, assignment): 
        i = low - 1   # index of smaller element
    
        for j in range(low, high):
            
            wasteland_pivot = self.num_conflicts(var, domain[high], assignment)
            wasteland = self.num_conflicts(var, domain[j], assignment)
                
            if  wasteland <= wasteland_pivot:
                i = i + 1 
                domain[i], domain[j] = domain[j], domain[i] 
    
        domain[i + 1], domain[high] = domain[high], domain[i + 1] 
        return ( i + 1 ) 


    def num_conflicts(self, var, word_x, assignment):
        """
        INPUT:
            - var: Variable object.
            - word_x: string.
            - assignment: Dictionary.
        OUTPUT:
            - wasteland: int

        Counts the possible conflicts `word_x` may create with words
        in all the variables' domains not int assignmet.
        """

        wasteland = 0

        for y in self.crossword.neighbors(var):
            if y not in assignment:
                intersect = self.crossword.overlaps[var, y]
                    
                # counts how many conflict there are
                # when 'x' and 'y' overlap
                for word_y in self.domains[y]:
                    if word_x[intersect[0]] != word_y[intersect[1]]:
                        wasteland += 1

        return wasteland


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)

if __name__ == "__main__":
    main()