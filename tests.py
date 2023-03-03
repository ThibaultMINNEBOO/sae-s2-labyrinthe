from app.Maze import Maze

print("-------------------------------")
print("Test 1: Générer un labyrinthe totalement vide (avec aucun mur)")
print("-------------------------------")

laby = Maze(4, 4, empty=True)

print(laby)