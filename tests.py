import app.Maze

print("-------------------------------")
print("Test 1: Générer un labyrinthe totalement vide (avec aucun mur)")
print("-------------------------------")

laby = app.Maze.Maze(4, 4, empty=True)

print(laby)