from random import choice, randint, shuffle

class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height: int, width: int, empty: bool = False):
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large 
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)} if not empty else {(i,j): {(y, x) for y in range(i-1, i+2) for x in range(j-1, j+2) if (i, j) != (y, x) and 0 <= y <= height-1 and 0 <= x <= width-1} for i in range(height) for j in range(width)}
 
    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def add_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Ajoute un mur au labyrinthe entre la cellule c1 et la cellule c2.

        Arguments:
            - c1 (tuple): Un tuple contenant en première position la position y et en seconde position la position x de la cellule
            - c2 (tuple): Un tuple contenant en première position la position y et en seconde position la position x de la cellule
        """
    # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées ne sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire

    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Permet de supprimer un mur entre deux cellules.
        """
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les cordonnées ne sont pas comptabibles avec les dimensions du labyrinthe"
        
        if c2 not in self.neighbors[c1]:
            self.neighbors[c1].add(c2)
        if c1 not in self.neighbors[c2]:
            self.neighbors[c2].add(c1)

    def get_walls(self) -> list:
        """
        Permet de récupérer tous les murs du tableau.
        Le retour se présente sous la forme d'une liste contenant la liste de deux cellules.
        """
        walls = []

        for c1 in self.neighbors.keys():
            if (c1[0], c1[1]+1) in self.neighbors.keys() and (c1[0], c1[1]+1) not in self.neighbors[c1]:
                walls.append([c1, (c1[0], c1[1]+1)])
            if (c1[0]+1, c1[1]) in self.neighbors.keys() and (c1[0]+1, c1[1]) not in self.neighbors[c1]:
                walls.append([c1, (c1[0]+1, c1[1])])

        return walls 
    
    def fill(self) -> None:
        """
        Permet d'ajouter tous les murs possible au labyrinthe.
        """
        self.neighbors = {(i, j): set() for i in range(self.width) for j in range(self.height)}

    def empty(self) -> None:
        """
        Supprime tous les murs du labyrinthe.
        """
        {(i,j): {(y, x) for y in range(i-1, i+2) for x in range(j-1, j+2) if (i, j) != (y, x) and 0 <= y <= self.height-1 and 0 <= x <= self.width-1} for i in range(self.height) for j in range(self.width)}

    def get_contiguous_cells(self, cell: tuple) -> list: 
        """
        Récupère l'entièreté des cellules contiguë à une cellule passée en paramètre.

        Arguments:
            - cell (tuple): Représente une cellule (un couple contenant la coordonnée x et la coordonnée y)
        """
        cells = []

        if cell[0]-1 >= 0:
            cells.append((cell[0]-1, cell[1]))
        if cell[0]+1 < self.height:
            cells.append((cell[0]+1, cell[1]))
        if cell[1]-1 >= 0:
            cells.append((cell[0], cell[1]-1))
        if cell[1]+1 < self.width:
            cells.append((cell[0], cell[1]+1))

        return cells

    @classmethod
    def gen_btree(cls, height: int, width: int):
        """
        Génère un labyrinthe via l'algorithme de l'arbre binaire.

        Arguments:
            - height (int): représente la hauteur du labyrinthe
            - width (int): représente la largeur du labyrinthe
        """
        laby = cls(height, width)

        # On parcoure toutes les cellules du labyrinthe
        for i in range(height):
            for j in range(width):
                # On tire au hasard une direction entre SOUTH et EAST
                direction = choice(["SOUTH", "EAST"])

                if direction == "SOUTH":
                    # On regarde s'il y a un mur au sud de cette cellule
                    if [(i,j), (i+1,j)] in laby.get_walls():
                        # On supprime le mur au sud
                        laby.remove_wall((i,j), (i+1,j))
                    # Au contraire, on regarde s'il y a un mur à l'est de cette cellule
                    elif [(i,j),(i,j+1)] in laby.get_walls():
                        # On supprime le mur à l'est
                        laby.remove_wall((i,j), (i,j+1))
                else:
                    # On regarde s'il y a un mur à l'est de cette cellule
                    if [(i,j), (i,j+1)] in laby.get_walls():
                        # On supprime le mur à l'est
                        laby.remove_wall((i,j),(i,j+1))
                    # Au contraire, on regarde s'il y a un mur au sud de cette cellule
                    elif [(i,j), (i+1,j)] in laby.get_walls():
                        # On supprime le mur au sud
                        laby.remove_wall((i,j),(i+1,j))
                
        return laby

    @classmethod
    def gen_sidewinder(cls, height: int, width: int):
        """
        Permet de générer un labyrinthe avec l'algorithme sidewinder
        """
        laby = cls(height, width)

        for i in range(height-1):
            # On initialise une variable sequence à une liste vide
            sequence = []
            for j in range(width-1):
                # On ajoute la cellule à la sequence
                sequence.append((i,j))

                # On tire au hasard au pile ou face (PILE représente 0, FACE représente 1)
                piece = randint(0,1)

                # On vérifie si c'est face
                if piece:
                    # On choisie une cellule à casser parmi la séquence
                    cell = choice(sequence)
                    
                    # On vérifie que le mur au sud est accessible
                    if [cell, (cell[0]+1, cell[1])] in laby.get_walls():
                        # On supprime le mur au sud de la cellule
                        laby.remove_wall(cell, (cell[0]+1, cell[1]))

                    # On réinitialise la sequence à vide
                    sequence = []
                else:
                    # On vérifie que le mur à l'est est accessible
                    if [(i,j), (i,j+1)] in laby.get_walls():
                        # On supprime le mur à l'est de la cellule
                        laby.remove_wall((i,j), (i,j+1))

            # On ajoute le dernier mur à la séquence
            sequence.append((i, width-1))

            # On tire au sort une cellule parmi la séquence
            cell = choice(sequence)

            # On vérifie si son mur au sud est accessible
            if [cell, (cell[0]+1, cell[1])] in laby.get_walls():
                # On supprime le mur au sud de la cellule
                laby.remove_wall(cell, (cell[0]+1, cell[1]))

        # On casse tous les mur à l'est de la dernière ligne
        for cell_x in range(width-1):
            laby.remove_wall((height-1, cell_x), (height-1, cell_x+1))

        return laby
    
    @classmethod
    def gen_fusion(cls, height: int, width: int):
        """
        Permet de générer un labyrinthe avec l'algorithme de fusion de chemin.
        """
        laby = cls(height, width)

        # On labélise toutes les cellules de 1 à n
        label_cells = {}
        label = 1

        for cell in laby.neighbors.keys():
            label_cells[cell] = label
            label += 1

        # On extrait tous les murs dans une liste et on la mélange aléatoirement
        walls = laby.get_walls()
        shuffle(walls)

        # On itère sur les murs mélangés aléatoirement
        for w in walls:
            # On vérifie que les deux cellules séparées par le mur n'ont pas le même label
            if label_cells[w[0]] != label_cells[w[1]]:
                # On casse le mur présent entre ces deux cellules
                laby.remove_wall(w[0], w[1])
            
                # On récupère la liste des cellules ayant le même label que la deuxième cellule du mur
                same_labels = [cell for cell in laby.neighbors.keys() if cell != w[0] if label_cells[cell] == label_cells[w[1]]]

                # On ajoute le même label que la première cellules à toutes les cellules ayant le même label que la deuxième cellule incluse.
                for cell in same_labels:
                    label_cells[cell] = label_cells[w[0]]
                
        return laby
        
    @classmethod
    def gen_exploration(cls, height: int, width: int):
        """
        Cette méthode de classe permet de générer un labyrinthe parfait en utilisant l'algorithme de l'exploration exhaustive.
        Elle retourne un objet de type Maze.

        Args:
            height (int): la hauteur du labyrinthe à créer
            width (int): la largeur du labyrinthe à créer

        Returns:
            laby: un objet de type Maze représentant le labyrinthe généré.

        Raises:
            None

        Exemple d'utilisation :
            labyrinthe = Maze.gen_exploration(10, 10)
        """
        laby = cls(height, width)
        
        # On choisit une cellule au hasard dans le labyrinthe
        cell = choice(list(laby.neighbors.keys()))

        # On marque cette cellule comme étant visitée
        visite = [cell]

        # On ajoute cette cellule à une pile 
        pile = [cell]

        while pile:
            # On dépile la cellule
            c = pile.pop(0)

            # On regarde les cellules contiguës et qui n'ont pas encore été visitée à la cellule qui vient d'être dépilée
            no_visited = [cell for cell in laby.get_contiguous_cells(c) if cell not in visite]

            if no_visited:
                # On remet sur la pile la cellule qui vient d'être dépilée
                pile.insert(0, c)

                # On choisit au hasard l'une de ses cellules contiguës qui n'a pas été visité
                cell = choice(no_visited)

                # On casse le mur séparant les deux cellules
                laby.remove_wall(c, cell)

                # On marque la cellule choisie au hasard comme étant visitée
                visite.append(cell)

                # On rajoute sur la pile la cellule ayant été choisi
                pile.insert(0, cell)

        return laby

    @classmethod
    def gen_wilson(cls, height: int, width: int):
        """
        Permet de générer un labyrinthe par l'algorithme de wilson
        """
        laby = cls(height, width)
        cell = choice(list(laby.neighbors.keys()))
        visited = [cell]

        while len(visited) < len(laby.neighbors.keys()):
            cell = choice(list(laby.neighbors.keys()))
            while cell in visited:
                cell = choice(list(laby.neighbors.keys()))
            
            path = [cell]

            while path[-1] not in visited:
                contigous_cell = choice(laby.get_contiguous_cells(path[-1]))

                if contigous_cell in path:
                    path = path[:path.index(contigous_cell)+1]
                else:
                    path.append(contigous_cell)

            for i in range(len(path)-1):
                laby.remove_wall(path[i], path[i+1])

            visited += path[:-1]

        return laby


    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i,j):' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            #content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i,j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += " "+content[(0,j)]+" ┃" if (0,j+1) not in self.neighbors[(0,j)] else " "+content[(0,j)]+"  "
        txt += " "+content[(0,self.width-1)]+" ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " "+content[(i+1,j)]+" ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else " "+content[(i+1,j)]+"  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt
    

    def solve_dfs(self, start: tuple, end: tuple):
        """
        Permet de résoudre un labyrinthe avec le parcours en profondeur
        """
        visite = []
        pile = [start]
        predecesseurs = {start: None}

        while pile:
            cell = pile.pop(0)
            if cell == end:
                path = []
                while cell is not None:
                    path.append(cell)
                    cell = predecesseurs[cell]
                
                return path[::-1]
            
            visite.append(cell)
            for n in self.neighbors[cell]:
                if n not in visite:
                    pile.insert(0, n)
                    predecesseurs[n] = cell
        
        return visite


    def solve_bfs(self, start: tuple, end: tuple):
        """
        Permet de résoudre un labyrinthe avec le parcours en largeur
        """
        visite = []
        file = [start]
        predecesseurs = {start: None}

        while file:
            cell = file.pop(0)
            if cell == end:
                path = []
                while cell is not None:
                    path.append(cell)
                    cell = predecesseurs[cell]
                
                return path[::-1]
            
            visite.append(cell)
            for n in self.neighbors[cell]:
                if n not in visite:
                    file.append(n)
                    predecesseurs[n] = cell
        
        return visite
    

    def distance_man(self, c1: tuple, c2: tuple):
        """
        Retourne le nombre minimal de déplacement pour aller de la cellule c1 à la cellule c2 si il n'y avait pas de mur
        """
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt