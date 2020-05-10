import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def isEmpty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.isEmpty():
            raise Exception('Empty frontier')
        else:
            node = self.frontier.pop()
            return node

class QueueFrontier(StackFrontier):

    def remove(self):
        if self.isEmpty():
            raise Exception('Empty frontier')
        else:
            node = self.frontier.pop(0)
            return node

class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count('A') != 1:
            raise Exception('The maze must have exactly one start point')
        if contents.count('B') != 1:
            raise Exception('The maze must have exactly one end point')

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents))

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print(unichr(0x2588), end='')
                elif (i, j) == self.start:
                    print('A', end='')
                elif (i, j) == self.goal:
                    print('B', end='')
                elif solution is not None and (i, j) in solution:
                    print('*', end='')
                else:
                    print(' ', end='')
            print()
        print()

    def neighbours(self, state):
        row, col = state
        candidates = [
                ('up', (row - 1, col)),
                ('down', (row + 1, col)),
                ('left', (row, col - 1)),
                ('right', (row, col + 1)),
        ]

        result = []
        for action, (i, j) in candidates:
            if 0 <= i < self.height and 0 <= j < self.width and not self.walls[i][j]:
                result.append((action, (i, j)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize the frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep logging until solution is found
        while True:
            if frontier.isEmpty():
                raise Exception('No solution')
            currNode = frontier.remove()
            self.explored += 1

            if currNode.state = self.goal:
                actions = []
                cells = []
                while currNode.parent is not None:
                    actions.append(currNode.action)
                    cells.append(currNode.state)
                    currNode = currNode.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbours to the frontier
            for action, state in self.neighbours(currNode):
                if not frontier.contains_state(state) and state not in self.explored:
                    neighbour = Node(state=state, parent=currNode, action=action)
                    frontier.add(neighbour)
