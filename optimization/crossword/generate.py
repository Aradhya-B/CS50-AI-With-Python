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
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            words = self.domains[v].copy()
            for word in words:
                if len(word) != v.length:
                    self.domains[v].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False
        res = False
        wordx = self.domains[x].copy()
        for word1 in wordx:
            flag = False
            for word2 in self.domains[y]:
                if word1[overlap[0]] == word2[overlap[1]]:
                    flag = True
                    break
            if flag:
                res = True
            else:
                self.domains[x].remove(word1)
        return res

        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            for xVal in self.domains[x].copy():
                if not any(xVal[overlap[0]] == yVal[overlap[1]] for yVal in self.domains[y]):
                    self.domains[x].remove(xVal)
                    revised = True
        return revised
        """

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs:
            queue = copy.deepcopy(arcs)
        else:
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y:
                        queue.append((x, y))

        while len(queue) != 0:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
#        return self.crossword.variables == set(assignment.keys())
        isComplete = len(set(self.crossword.variables)) == len(set(assignment))
        return isComplete

    def consistent_helper(self, x, y, assignment):
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return True
        
        xVal = assignment[x]
        yVal = assignment[y]

        return xVal[overlap[0]] == yVal[overlap[1]]

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for x in assignment:
            for y in assignment:
                if x != y:
                    if not self.consistent_helper(x, y, assignment):
                        return False
        return True

        """
        isConsistent = False

        vals = list(assignment.values())
        areDistinct = len(vals) == len(set(vals))
        areCorrectLength = all(var.length == len(assignment[var]) for var in assignment)
        areNoConflicts = True
        for var in assignment:
            foundInconsistency = False
            for neighbor in self.crossword.neighbors(var):
                if self.crossword.overlaps[var, neighbor] is not None:
                    (i, j) = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        find = True
                        areNoConflicts = False
                        break
            if foundInconsistency:
                break
        if areDistinct and areCorrectLength and areNoConflicts:
            isConsistent = True
        return isConsistent
        """

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        if var:
            words = self.domains[var]
            neighbors = self.crossword.neighbors(var)
            cnts = []
            for word in words:
                cnt = 0
                for neighbor in neighbors:
                    if neighbor not in assignment and word in self.domains[neighbor]:
                        cnt += 1
                cnts.append(cnt)
                tmp = list(zip(words, cnts))
                tmp.sort(key=lambda x: -x[1])

                return [word[0] for word in tmp]
        return []

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        variable = list(self.crossword.variables - set(assignment.keys()))
        num_remain = [len(self.domains[var]) for var in variable]
        degree = [len(self.crossword.neighbors(var)) for var in variable]
        tmp = list(zip(variable, num_remain, degree))
        def cmp(x, y):
            if x[1] != y[1]:
                if x[1] > y[1]:
                    return 1
                else:
                    return -1
            else:
                if x[2] < y[2]:
                    return 1
                elif x[2] > y[2]:
                    return -1
                else:
                    return 0

            sorted(tmp, key=functools.cmp_to_key(cmp))

            return tmp[0][0]

        """
        unassignedVar = None
        for var in assignment:
            if assignment[var] is None:
                unassignedVar = var
                break
        return unassignedVar
        """

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
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            if self.consistent(assignment):
                result = self.Backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None

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
