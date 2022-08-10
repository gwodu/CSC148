from pokemon import Pokemon, Trainer, World, PokeCenter, load_trainers
import pokemon_data

# f = open('/Users/g.l.wodu/Desktop/CSC148/csc148/assignments/a0/a1/pokemon_data/pokemon_trainers.txt')
# g = open('/Users/g.l.wodu/Desktop/CSC148/csc148/assignments/a0/a1/pokemon_data/pokemon_names.txt')
# h = open('/Users/g.l.wodu/Desktop/CSC148/csc148/assignments/a0/a1/pokemon_data/pokemon_weaknesses.txt')
# josh = Trainer('Josh')
# world = World(josh)
# print(load_trainers(f, world))

pikachu = Pokemon("pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
print(pikachu.weakness)
pikachu.curr_hp == 0
print(pikachu.fainted)

