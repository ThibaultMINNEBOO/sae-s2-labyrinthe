from app.Maze import Maze

print("""
    _______       _______             __   
    |   _   .--.--|       .-----.-----|  |_ 
    |.  1   |  |  |.|   | |  -__|__ --|   _|
    |.  ____|___  `-|.  |-|_____|_____|____|
    |:  |   |_____| |:  |                   
    |::.|           |::.|                   
    `---'           `---'                   
    """)
print("Bienvenue sur l'interface de test")
print("Afin d'avoir la liste des commandes disponibles veuillez taper '/help'")

print()

lst_commands = {
    '/help': "Afficher la liste des commandes",
    '/gen_btree <height> <width>': "Générer un labyrinthe par arbre binaire",
    '/gen_sidewinder <height> <width>': "Générer un labyrinthe avec l'algorithme sidewinder",
    '/gen_fusion <height> <width>': "Générer un labyrinthe avec l'algorithme des fusions de chemins",
    '/gen_exploration <height> <width>': "Générer un labyrinthe avec l'algorithme de l'exploration exhaustive",
    '/gen_empty_maze <height> <width>': "Générer un labyrinthe vide",
    '/gen_full_maze <height> <width>': "Générer un labyrinthe plein",
    '/get_walls': "Récupère tous les murs du labyrinthe.",
    '/gen_fusion_maze <height> <width>': "Générer un labyrinthe par fusion de chemin",
    '/add_wall <cell1_posy> <cell1_posx> <cell2_posy> <cell2_posx>': "Ajoute un mur au labyrinthe",
    '/gen_wilson <height> <width>': "Générer un labyrinthe par l'algorithme de wilson",
    '/remove_wall <cell1_posy> <cell1_posx> <cell2_posy> <cell2_posx>': "Supprimer un mur entre deux cellules",
    '/solve_dfs': "Donne une solution au labyrinthe"
}

cache = None

while True:
    try:
        user_input = input('> ').split(" ")
        cmd = user_input[0]
        args = user_input[1:]

        if cmd == '/help':
            print("Voici la liste des commandes : ")
            for command in lst_commands:
                print(f"    {command} : {lst_commands[command]}")
        elif cmd == '/gen_empty_maze':
            if len(args) == 0:
                print("Veuillez entrer la hauteur et la largeur du labyrinthe")
            elif len(args) == 1:
                print("Veuillez entrer la largeur du labyrinthe")
            else:
                laby = Maze(int(args[0]), int(args[1]), empty=True)
                print(laby)
                cache = laby
        elif cmd == '/gen_full_maze':
            if len(args) == 0:
                print("Veuillez entrer la hauteur et la largeur du labyrinthe")
            elif len(args) == 1:
                print("Veuillez entrer la largeur du labyrinthe")
            else:
                laby = Maze(int(args[0]), int(args[1]))
                print(laby)
                cache = laby
        elif cmd == '/gen_btree':
            if len(args) == 0 or not args[0]:
                print("Veuillez entrer la hauteur et la largeur du labyrinthe")
            elif len(args) == 1 or not args[1]:
                print("Veuillez entrer la largeur du labyrinthe")
            else:
                laby = Maze.gen_btree(int(args[0]), int(args[1]))
                print(laby)
                cache = laby
        elif cmd == '/get_walls':
            if cache is None:
                print("Vous n'avez encore généré aucun labyrinthe. De ce fait, le labyrinthe n'est pas dans le cache")
            else:
                print("====== Murs du labyrinthe ======")
                print(cache.get_walls())
                print("================================")
        elif cmd == '/add_wall':
            if len(args) < 4:
                print("Veuillez entrer la valeur y de la cellule 1, puis la valeur x de la cellule 1 et faire de même pour la cellule 2")
            elif cache is None:
                print("Vous n'avez encore généré aucun labyrinthe. De ce fait, le labyrinthe n'est pas dans le cache")
            elif not (0 <= int(args[0]) < cache.height and 0 <= int(args[1]) < cache.width and 0 <= int(args[2]) < cache.height and 0 <= int(args[3]) < cache.width):
                print(f"Les valeurs rentrées sont incorrectes, veuillez rentrer des valeurs possibles dans un labyrinthe {cache.height} x {cache.width}")
            elif (int(args[2]), int(args[3])) not in cache.get_contiguous_cells((int(args[0]), int(args[1]))):
                print("Veuillez entrer comme cellule 2 une cellule contiguë à la cellule 1")
            else:
                cache.add_wall((int(args[0]), int(args[1])), (int(args[2]), int(args[3])))
                print(f"Le mur ({args[0]}, {args[1]}), ({args[2]}, {args[3]}) a été ajouté avec succès")
                print(laby)
        elif cmd == '/remove_wall':
            if len(args) < 4:
                print("Veuillez entrer la valeur y de la cellule 1, puis la valeur x de la cellule 1 et faire de même pour la cellule 2")
            elif cache is None:
                print("Vous n'avez encore généré aucun labyrinthe. De ce fait, le labyrinthe n'est pas dans le cache")
            elif not (0 <= int(args[0]) < cache.height and 0 <= int(args[1]) < cache.width and 0 <= int(args[2]) < cache.height and 0 <= int(args[3]) < cache.width):
                print(f"Les valeurs rentrées sont incorrectes, veuillez rentrer des valeurs possibles dans un labyrinthe {cache.height} x {cache.width}")
            elif (int(args[2]), int(args[3])) not in cache.get_contiguous_cells((int(args[0]), int(args[1]))):
                print("Veuillez entrer comme cellule 2 une cellule contiguë à la cellule 1")
            else:
                cache.remove_wall((int(args[0]), int(args[1])), (int(args[2]), int(args[3])))
                print(f"Le mur ({args[0]}, {args[1]}), ({args[2]}, {args[3]}) a été supprimé avec succès")
                print(laby)
        elif cmd == '/gen_sidewinder':
            if len(args) == 0 or not args[0]:
                print("Veuillez entrer la hauteur et la largeur du labyrinthe")
            elif len(args) == 1 or not args[1]:
                print("Veuillez entrer la largeur du labyrinthe")
            else:
                laby = Maze.gen_sidewinder(int(args[0]), int(args[1]))
                print(laby)
                cache = laby
        elif cmd == '/gen_fusion':
            if len(args) == 0 or not args[0]:
                print("Veuillez entrer la hauteur et la largeur du labyrinthe")
            elif len(args) == 1 or not args[1]:
                print("Veuillez entrer la largeur du labyrinthe")
            else:
                laby = Maze.gen_fusion(int(args[0]), int(args[1]))
                print(laby)
                cache = laby
        elif cmd == '/gen_exploration':
            if len(args) == 0 or not args[0]:
                print("Veuillez entrer la hauteur et la largeur du labyrinthe")
            elif len(args) == 1 or not args[1]:
                print("Veuillez entrer la largeur du labyrinthe")
            else:
                laby = Maze.gen_exploration(int(args[0]), int(args[1]))
                print(laby)
                cache = laby
        elif cmd == '/gen_wilson':
            if len(args) == 0 or not args[0]:
                print("Veuillez entrer la hauteur et la largeur du labyrinthe")
            elif len(args) == 1 or not args[1]:
                print("Veuillez entrer la largeur du labyrinthe")
            else:
                laby = Maze.gen_wilson(int(args[0]), int(args[1]))
                print(laby)
                cache = laby
        elif cmd == '/solve_dfs':
            if cache is None:
                print("Vous n'avez encore généré aucun labyrinthe. De ce fait, le labyrinthe n'est pas dans le cache")
            else:
                start = (0,0)
                end = (cache.height-1, cache.width-1)

                solution = cache.solve_dfs(start, end)
                str_solution = {c: '*' for c in solution}
                str_solution[start] = 'D'
                str_solution[end] = 'A'

                print(cache.overlay(str_solution))
        elif cmd == '/solve_bfs':
            if cache is None:
                print("Vous n'avez encore généré aucun labyrinthe. De ce fait, le labyrinthe n'est pas dans le cache")
            else:
                start = (0,0)
                end = (cache.height-1, cache.width-1)

                solution = cache.solve_bfs(start, end)
                str_solution = {c: '*' for c in solution}
                str_solution[start] = 'D'
                str_solution[end] = 'A'

                print(cache.overlay(str_solution))
        elif cmd == "exit":
            exit(0)
        else:
            print(f"La commande {cmd} n'existe pas")
    except:
        exit(0)