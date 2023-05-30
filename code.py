import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Game:

    cell_data = []
    cell_values = []
    multipliers = {1: 1.0, 2: 1.0}

    remaining_resources = {1: 0, 2: 0}
    max_resources = {1: 0, 2: 0}
    ants = {1: 0, 2: 0}

    def _evaluate_cell(self, resources, resource_type, my_ants, opponent_ants):
    
        cell_value = 0
        cell_value += self._resource_specific_evaluate(resources, resource_type, my_ants, opponent_ants)
        
        return cell_value

    def _resource_specific_evaluate(self, resources, resource_type, my_ants, opponent_ants):
        if resource_type == 0:
            return self._evaluate_empty_cell(my_ants, opponent_ants)
        elif resource_type == 1:
            return self._evaluate_egg_cell(resources, my_ants, opponent_ants)
        elif resource_type == 2:
            return self._evaluate_crystal_cell(resources, my_ants, opponent_ants)
        return 0

    def _evaluate_egg_cell(self, resources, my_ants, opponent_ants):
        return (resources / self.max_resources[1]) * (self.multipliers[1] - (self.ants[1]/self.max_resources[1]))

    def _evaluate_crystal_cell(self, resources, my_ants, opponent_ants):
        return ((resources / self.max_resources[2]) * self.multipliers[2])

    def _evaluate_empty_cell(self, my_ants, opponent_ants):
        return 0


    def reset_remaining(self):
        self.remaining_resources = {1: 0, 2: 0}

    def reset_ants(self):
        self.ants = {1: 0, 2: 0}

    def track_remaining_resources(self, i, amount):
        if self.cell_data[i][0]:
            self.remaining_resources[self.cell_data[i][0]] += amount


    def track_max_resources(self, amount, resource_type):
        if resource_type:
            self.max_resources[resource_type] += amount

    def update(self, i, resources, my_ants, opponent_ants):
        self.update_cell_value(i, resources, my_ants, opponent_ants)
        self.update_ants(my_ants, opponent_ants)

    def update_cell_value(self, i, resources, my_ants, opponent_ants):
        resource_type = self.cell_data[i][0]
        value = self._evaluate_cell(resources, resource_type, my_ants, opponent_ants)
        if len(self.cell_values) <= i:
            self.cell_values.append(value)
        else:
            self.cell_values[i] = value

    def update_ants(self, mine, opponents):
            self.ants[1] += mine
            self.ants[2] += opponents

    def find_best_cell(self):
        return self.cell_values.index(max(self.cell_values))

    def update_cell_data(self, data):
        self.cell_data.append(data)

    def calculate_multipliers(self):
        self.multipliers[1] = 1 / (self.max_resources[1] / (self.max_resources[1] + self.max_resources[2]))
        self.multipliers[2] = 1 / (self.max_resources[2] / (self.max_resources[1] + self.max_resources[2]))
        print("Initial multipliers", self.multipliers, file=sys.stderr, flush=True)


game = Game()

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    game.track_max_resources(amount=initial_resources, resource_type=_type)
    game.update_cell_data(data=(_type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5))

game.calculate_multipliers()
number_of_bases = int(input())

for i in input().split():
    my_base_index = int(i)

for i in input().split():
    opp_base_index = int(i)


target = None
# game loop
while True:
    game.reset_remaining()
    game.reset_ants()
    keep_target = False
    for i in range(number_of_cells):
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        game.track_remaining_resources(i, resources)
        game.update(i, resources, my_ants, opp_ants)

        if i == target and resources > 0:
            keep_target = True

    if (target is None) or (not keep_target):
        target = game.find_best_cell()
    
    print("REMAINING", game.remaining_resources ,file=sys.stderr, flush=True)
    print("MAXIMUM", game.max_resources ,file=sys.stderr, flush=True)
    print("My ants", game.ants ,file=sys.stderr, flush=True)

    print(f"LINE {my_base_index} {target} {1}")
        



    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>

