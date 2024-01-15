from __future__ import annotations
from typing import Optional
from support import UserInterface, TextInterface
from constants import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<Thuy Linh Nguyen>, <47277021>"
__email__ = "<s4727702@student.uq.edu.au>"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackboard changelog. 
__version__ = 2.3

# Uncomment this function when you have completed the Level class and are ready
# to attempt the Model class.

def load_game(filename: str) -> list['Level']:
    """ Reads a game file and creates a list of all the levels in order.
    
    Parameters:
        filename: The path to the game file
    
    Returns:
        A list of all Level instances to play in the game
    """
    levels = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Maze'):
                _, _, dimensions = line[5:].partition(' - ')
                dimensions = [int(item) for item in dimensions.split()]
                levels.append(Level(dimensions))
            elif len(line) > 0 and len(levels) > 0:
                levels[-1].add_row(line)
    return levels

# Write your classes here
class Tile(object):
    """ Class to represent a tile

    Attributes: 
        blocked (bool): blocking status of Tile
        tile_id (str): letter representing the type of Tile
        damage_taken (int): damage dealed by Tile
        open_door (bool): opening status of door

    Methods:
        is_blocking: Return blocking status
        damamge: Return damage dealed by Tile
        get_id: Return tile_id

    Examples:
    >>> tile = Tile()
    >>> tile.is_blocking()
    False
    >>> tile.damage()
    0
    >>> tile.get_id()
    'AT'
    >>> str(tile)
    'AT'
    >>> tile
    Tile()
    """
    def __init__(self) -> None: 
        """ The constructor to initialize the object """
        self.blocked = False
        self.tile_id = ABSTRACT_TILE
        self.damage_taken = 0
        self.open_door = False

    def is_blocking(self) -> bool: 
        """ Return blocking status """
        return self.blocked
    
    def damage(self) -> int:
        """ Return the damage_taken """
        return self.damage_taken
    
    def get_id(self) -> str:
        """ Return tile_id """
        return self.tile_id
        
    def __str__(self) -> str:
        return self.get_id()

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

class Wall(Tile):
    """ Extend Class 'Tile'. 
    
    Examples:
    >>> wall = Wall()
    >>> wall.is_blocking()
    True
    >>> wall.get_id()
    '#'
    >>> str(wall)
    '#'
    >>> wall
    Wall()
    """
    def __init__(self) -> None:
        """Overriden `Tile.__init__()`

        blocked (bool): set to True
        tile_id (str): set to WALL
        """
        self.blocked = True
        self.tile_id = WALL

class Empty(Tile):
    """ Extend Class 'Tile'

    Examples:
    >>> empty = Empty()
    >>> empty.is_blocking()
    False
    >>> empty.get_id()
    ' '
    >>> str(empty)
    ' '
    >>> empty
    Empty()
    """
    def __init__(self) -> None:
        """Overriden `Tile.__init__()`

        blocked (bool): set to False
        tile_id (str): set to EMPTY
        damage_taken (int): set to 0
        """
        self.tile_id = EMPTY
        self.blocked = False
        self.damage_taken = 0
    
class Lava(Tile):
    """ Extend Class 'Tile'

    Examples:
    >>> lava = Lava()
    >>> lava.is_blocking()
    False
    >>> lava.get_id()
    'L'
    >>> lava.damage()
    5
    >>> str(lava)
    'L'
    >>> lava
    Lava()
    """

    def __init__(self) -> None:
        """Overriden `Tile.__init__()`

        blocked (bool): set to False
        tile_id (str): set to EMPTY
        damage_taken (int): set to LAVA_DAMAGE
        """
        self.tile_id = LAVA
        self.blocked = False
        self.damage_taken = LAVA_DAMAGE

    def damage(self) -> int:
        """Extend `Tile.damage()`. Return Damage dealed by Lava tile

        Examples:
        >>> lava = Lava()
        >>> lava.damage()
        5
        """
        return self.damage_taken

class Door(Tile):
    """ Extend Class 'Tile'

    Examples:
    >>> door = Door()
    >>> door.is_blocking()
    True
    >>> door.get_id()
    'D'
    >>> str(door)
    'D'
    >>> door
    Door()
    >>> door.unlock()
    >>> door.is_blocking()
    False
    >>> door.get_id()
    ' '
    >>> str(door)
    ' '
    >>> door
    Door()
    """
    def is_blocking(self) -> bool:
        """Overriden `Tile.is_blocking()`. Return blocking status.

        Parameters: 
            blocked (bool): extend `Tile.blocked`
            open_door (bool): extend `Tile.open_door`
        
        Return:
            False if open_door is True 
            True if open_door is False
        """
        if self.open_door == False:
            self.blocked = True
            return self.blocked
        else:
            self.blocked = False
            return self.blocked

    def get_id(self) -> str:
        """Overriden `Tile.get_id()`. Return tile_id.

        Parameters:
            open_door (bool): door opening status
            tile_id (str): extend Tile.tile_id
        
        Return:
            'E' if open_door is True
            'D' if open_door is False
        """
        if self.open_door == True:
            self.tile_id = EMPTY
        else:
            self.tile_id = DOOR
        return self.tile_id

    def unlock(self) -> None:
        """ Unlock the door

        Parameter: 
            open_door (bool): set to true
        
        Return:
            None
        """
        self.open_door = True
        return

class Entity(object):
    """ Class to represent an entity

    Attributes:
        location (tuple): location of entity
        _id (str): id of entity
    
    Methods:
        get_position: return location of entity
        get_name: return name of entity
        get_if: return id of entity
    
    Examples:
    >>> entity = Entity((2, 3))
    >>> entity.get_position()
    (2, 3)
    >>> entity.get_name()
    'Entity'
    >>> entity.get_id()
    'E'
    >>> str(entity)
    'E'
    >>> entity
    Entity((2, 3))
    """

    def __init__(self, position: tuple[row: int, column: int]) -> None:
        """ The constructor to initialize the object

        Parameters:
            position (tulple[int, int]): row and column index of entity
        """
        self.location = position
        self._id = 'E'

    def get_position(self) -> tuple[int, int]:
        """ Return location of entity """
        return self.location

    def get_name(self) -> str:
        """ Return name of entity """
        return type(self).__name__
    
    def get_id(self) -> str:
        """ Return id of entity """
        return self._id

    def __str__(self) -> str:
        return self.get_id()
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.location})"

class DynamicEntity(Entity):
    """ Extend Class 'Entity'

    Examples:
    >>> dynamic_entity = DynamicEntity((1, 1))
    >>> dynamic_entity.get_position()
    (1, 1)
    >>> dynamic_entity.set_position((2, 3))
    >>> dynamic_entity.get_position()
    (2, 3)
    >>> dynamic_entity.get_id()
    'DE'
    >>> str(dynamic_entity)
    'DE'
    >>> dynamic_entity
    DynamicEntity((2, 3))
    """
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `Entity.__init__()`

        _id (str): set to DYNAMIC_ENTITY
        """
        super().__init__(position)
        self._id = DYNAMIC_ENTITY

    def set_position(self, new_position: tuple[int, int]) -> None:
        """ Change location of entity to new position

        Parameters:
            new_position (tuple): new location
                set DynamicEntity.location to new_position

        Return:
            None
        """
        self.location = new_position

class Player(DynamicEntity):
    """ Extend Class 'DynamicEntity'

    Examples:
    >>> player = Player((2, 3))
    >>> player.get_hunger()
    0
    >>> player.get_thirst()
    0
    >>> player.get_health()
    100
    >>> player.change_hunger(4)
    >>> player.change_thirst(3)
    >>> player.change_health(-34)
    >>> player.get_hunger()
    4
    >>> player.get_thirst()
    3
    >>> player.get_health()
    66
    """
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `DynamicEntity.__init__()`

        _id (str): set to PLAYER
        hunger (int): hunger of player 
        thirst (int): thirst of player 
        hp (int): health of player 
        player_inventory: set to `Inventory()`
        """
        super().__init__(position)
        self._id = PLAYER
        self.hunger = 0
        self.thirst = 0
        self.hp = MAX_HEALTH
        self.player_inventory = Inventory()

    def get_hunger(self) -> int:
        """ Return player's hunger """
        return self.hunger
    
    def get_thirst(self) -> int:
        """ Return player's thirst """
        return self.thirst
    
    def get_health(self) -> int:
        """ Return player's health """
        return self.hp
    
    def change_hunger(self, amount: int) -> None:
        """ Change hunger of player

        Parameters:
            amount (int): amount of hunger want to change 
                hunger += amount
                0 <= hunger <= MAX_HUNGER

        Return:
            None
        """
        self.hunger += amount
        if self.hunger < 0:
            self.hunger = 0
        elif self.hunger >= MAX_HUNGER:
            self.hunger = MAX_HUNGER
    
    def change_thirst(self, amount: int) -> None:
        """ Change thirst of player

        Parameters:
            amount (int): amount of thirst want to change 
                thirst += amount
                0 <= thirst <= MAX_THIRST

        Return:
            None
        """
        self.thirst += amount
        if self.thirst < 0:
            self.thirst = 0
        elif self.hunger >= MAX_THIRST:
            self.hunger = MAX_THIRST
            
    def change_health(self, amount: int) -> None:
        """ Change health of player

        Parameters:
            amount (int): amount of health want to change 
                hp += amount
                0 <= hp <= MAX_HEALTH

        Return:
            None
        """
        self.hp += amount
        if self.hp > MAX_HEALTH:
            self.hp = MAX_HEALTH
        elif self.hp < 0:
            self.hp = 0
        
    def get_inventory(self) -> Inventory:
        """ Return player's inventory """
        return self.player_inventory

    def add_item(self, item: Item) -> None:
        """ Extend `Inventory.add_item()` """
        self.player_inventory.add_item(item)

class Item(Entity):
    """ Extend Class 'Entity'

    Examples:
    >>> player = Player((2, 3))
    >>> item = Item((4, 5))
    >>> item.apply(player)
    >>> item.get_position()
    (4, 5)
    >>> item.get_name()
    'Item'
    >>> item.get_id()
    'I'
    >>> str(item)
    'I'
    >>> item
    Item((4, 5))
    """
    def __init__(self, position: tuple[int, int]) -> None:
        """ Override `Entity.__init__()`

        _id (str): set to ITEM
        """
        super().__init__(position)
        self._id = ITEM

    def apply(self, player: Player) -> None:
        """ Apply item to player
        
        Parameters:
            player (Player()): extend from Class 'Player'
        
        Return: 
            Implemented later in subclasses

        Raise:
            NotImplementedError
        """
        raise NotImplementedError
        
class Potion(Item):
    """ Extend Class 'Item'

    Examples:
    >>> player = Player((1, 1))
    >>> potion = Potion((1, 1))
    >>> player.change_health(-50)
    >>> player.get_health()
    50
    >>> potion.apply(player)
    >>> player.get_health()
    70
    >>> potion
    Potion((1, 1))
    """
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `Item.__init__()`

        _id (str): set to POTION
        """
        super().__init__(position)
        self._id = POTION

    def apply(self, player: Player) -> None:
        """ Overriden `Item.aplly()`

        Parameters:
            player (Player): change health of player by POTION_AMOUNT

        Return:
            None
        """
        player.change_health(POTION_AMOUNT)

class Coin(Item):
    """ Extend Class 'Item'

    Examples:
    >>> player = Player((4, 4))
    >>> coin = Coin((4, 4))
    >>> print(player.get_health(), player.get_thirst(), player.get_hunger())
    100 0 0
    >>> player.get_inventory().get_items()
    {}
    >>> coin.apply(player)
    >>> print(player.get_health(), player.get_thirst(), player.get_hunger())
    100 0 0
    >>> player.get_inventory().get_items()
    {}
    """
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `Item.__init__()`
        
        _id (str): set to COIN
        """
        super().__init__(position)
        self._id = COIN

    def apply(self, player: Player) -> None:
        """ Don't have effect on player """
        pass

class Water(Item):
    """ Extend Class 'Item'

    Examples:
    >>> player = Player((1, 1))
    >>> player.change_thirst(8)
    >>> player.get_thirst()
    8
    >>> water = Water((1, 1))
    >>> water.apply(player)
    >>> player.get_thirst()
    3
    >>> water.get_id()
    'W'
    >>> str(water)
    'W'
    >>> water
    Water((1, 1))
    """
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `Item.__init__()`

        _id (str): set to WATER
        """
        super().__init__(position)
        self._id = WATER
    
    def apply(self, player: Player) -> None:
        """ Overriden `Item.apply()`
        
        Parameters:
            player (Player): change playe's thirst by WATER_AMOUNT
        
        Return:
            None
        """
        player.change_thirst(WATER_AMOUNT)  

class Food(Item):
    """ Extend Class 'Item'

    Examples:
    >>> player = Player((1, 1))
    >>> player.change_hunger(7)
    >>> apple = Apple((1, 1))
    >>> honey = Honey((2, 3))
    >>> player.get_hunger()
    7
    >>> apple.apply(player)
    >>> player.get_hunger()
    6
    >>> honey.apply(player)
    >>> player.get_hunger()
    1
    >>> apple.get_id()
    'A'
    >>> honey.get_id()
    'H'
    >>> honey
    Honey((2, 3))
    >>> apple
    Apple((1, 1))
    >>> honey.get_name()
    'Honey'
    """
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `Item.__init__()`

        _id (str): set to FOOD
        """
        super().__init__(position)
        self._id = FOOD
    
    def apply(self, player: Player) -> None:
        """ Extend `Item.apply()` """
        pass

class Apple(Food):
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `Item.__init__()`

        _id (str): set to APPLE
        """
        super().__init__(position)
        self._id = APPLE

    def apply(self, player: Player) -> None:
        """ Overriden `Food.apply()`

        Parameters:
            player (Player): change hunger of player by APLLE_AMOUNT
        
        Return: 
            None
        """
        player.change_hunger(APPLE_AMOUNT)
    
class Honey(Food):
    def __init__(self, position: tuple[int, int]) -> None:
        """ Overriden `Food.__init__()`

        _id (str): set to HONEY
        """
        super().__init__(position)
        self._id = HONEY
    
    def apply(self, player) -> None:
        """ Overriden `Food.apply()`
        
        Parameters: 
            player (Player): change player's health by HOMEY_AMOUNT
        
        Return:
            None
        """
        player.change_hunger(HONEY_AMOUNT)

class Inventory():
    """ Class to represent Inventory

    Attributes:
        _initial_items (list[Item,...], optional): set to initial_items
        inventory (dict): dictionary with key is the name of item and value is
        list of Item 
    
    Methods:
        add_item(item: Item): add item into inventory
        get_items: return inventory
        remove_item (item_name: str): remove item with item_name from inventory
        and return the removed item (if item does not exist return None)

    Examples:
    >>> inventory = Inventory([Water((1, 2)), Honey((2, 3)), Water((3, 4))])
    >>> inventory
    Inventory(initial_items=[[Water((1, 2)), Honey((2, 3)), Water((3, 4))])
    >>> inventory.get_items()
    {'Water': [Water((1, 2)), Water((3, 4))], 'Honey': [Honey((2, 3))]}
    >>> inventory.add_item(Honey((3, 4)))
    >>> inventory.add_item(Coin((1, 1)))
    >>> inventory.get_items()
    {'Water': [Water((1, 2)), Water((3, 4))], 'Honey': [Honey((2, 3)), Honey((3, 4))], 'Coin': [Coin((1, 1))]}
    >>> inventory.remove_item('Honey')
    Honey((2, 3))
    >>> inventory.get_items()
    {'Water': [Water((1, 2)), Water((3, 4))], 'Honey': [Honey((3, 4))], 'Coin': [Coin((1, 1))]}
    >>> inventory.remove_item('Coin')
    Coin((1, 1))
    >>> non_existant_coin = inventory.remove_item('Coin')
    >>> print(non_existant_coin)
    None
    >>> inventory.get_items()
    {'Water': [Water((1, 2)), Water((3, 4))], 'Honey': [Honey((3, 4))]}
    >>> print(inventory)
    Water: 2
    Honey: 1
    >>> inventory
    Inventory(initial_items=[Water((1, 2)), Honey((2, 3)), Water((3, 4))])
    """
    def __init__(self, initial_items: Optional[list[Item,...]] = None) -> None:
        """ The constructor to initialize the class

        Parameters: 
            initial_items (list, optional): list of tiems
        """
        self.inventory = {}
        self._initial_items = initial_items
        #loop through initial items to add into inventory
        if self._initial_items != None:
            for each_item in self._initial_items:
                self.inventory[each_item.get_name()] = []
            for each_item in self._initial_items:
                self.inventory[each_item.get_name()].append(each_item)
    
    def add_item(self, item: Item) -> None:
        """ Add item into inventory
        
        Parameters:
            item (Item): 
                if item exist in inventory: add new Item() into inventory[item
                name]
                if item does not exist: create new key with item name and add
                item
        
        Return: 
            None
        """
        if item.get_name() in self.inventory:
            self.inventory[item.get_name()].append(item)
        else:
            self.inventory[item.get_name()] = []
            self.inventory[item.get_name()].append(item)
    
    def get_items(self) -> dict[str, list[Item, ...]]:
        """ Return inventory """
        return self.inventory
    
    def remove_item(self, item_name: str) -> Optional[Item]:
        """ Remove item from inventory

        Parameters:
            item_name (str): name of item 
        
        Return:
            if item_name in inventory:
                    if only 1 Item() in item_name: remove item_name from
                    Inventory and return Item()
                    else pop the first Item() in inventory[item_name]
                else:
                    None
        """
        if item_name in self.inventory:
            if len(self.inventory[item_name]) == 1:
                return self.inventory.pop(item_name)[0]
            else:
                return self.inventory[item_name].pop(0)
        else:
            return None
    
    def __str__(self) -> str:
        printing = []
        for item in self.inventory:
            printing.append(f"{item}: {len(self.inventory[item])}")
        return str("\n".join(printing))
    
    def __repr__(self):
        return f'{type(self).__name__}(initial_items={self._initial_items})'
         
class Maze():
    """ Class to represent Maze

    Attributes:
        _dimemsions (tuple[int, int]): number of rows and columns in maze
        _maze: list of rows in Maze
    
    Methods:
        get_dimemsions: return dimemsions of maze
        add_row (row: str): add row in _maze
        get_tiles: return list of tiles in rows 
        unlock_door: unlock maze's door
        get_tile (position: tuple[int, int]): return the tile at position

    Examples:
    >>> maze = Maze((5, 5))
    >>> maze.get_dimensions()
    (5, 5)
    >>> maze.get_tiles()
    []
    >>> str(maze)
    ''
    >>> maze.add_row('#####')
    >>> maze.add_row('# C D')
    >>> maze.add_row('# C #')
    >>> maze.add_row('P C #')
    >>> maze.add_row('#####')
    >>> from pprint import pprint
    >>> pprint(maze.get_tiles()) 
    [[Wall(), Wall(), Wall(), Wall(), Wall()],
     [Wall(), Empty(), Empty(), Empty(), Door()],
     [Wall(), Empty(), Empty(), Empty(), Wall()],
     [Empty(), Empty(), Empty(), Empty(), Wall()],
     [Wall(), Wall(), Wall(), Wall(), Wall()]]
    >>> print(maze)
    #####
    #   D
    #   #
        #
    #####
    >>> maze
    Maze((5, 5))
    >>> maze.get_tile((2, 3))
    Empty()
    >>> maze.unlock_door()
    >>> print(maze)
    #####
    #    
    #   #
        #
    #####
    >>> pprint(maze.get_tiles())
    [[Wall(), Wall(), Wall(), Wall(), Wall()],
     [Wall(), Empty(), Empty(), Empty(), Door()],
     [Wall(), Empty(), Empty(), Empty(), Wall()],
     [Empty(), Empty(), Empty(), Empty(), Wall()],
     [Wall(), Wall(), Wall(), Wall(), Wall()]]
    """
    def __init__(self, dimensions: tuple[int, int]) -> None:
        """ The constructor to initialize the class
        
        Parameters: 
            dimensions (tuple[int, int]): number of rows and columns in maze
        """
        self._dimensions = dimensions
        self._maze = []

    def get_dimensions(self) -> tuple[int, int]:
        """ Return maze's dimensions """
        return self._dimensions

    def add_row(self, row: str) -> None:
        """ Add row in _maze and set to Tile()

        Parameters:
            row (str): str of tiles id
                for each tile id in row, add Tile() corresponding to id in
                _maze
        
        Return:
            None
        """
        #create temporary list of tiles corresponding to row 
        tile_of_row = []
        #check for row valid for maze's dimemsion
        if len(row) <= self._dimensions[1] and len(self._maze) <= \
           self._dimensions[0]:
        #loop through tiles in row to create Tile() matching id and add to the
        #list
            for tile in row:
                if tile == WALL:
                    tile_of_row.append(Wall())
                elif tile == DOOR:
                    tile_of_row.append(Door())
                elif tile == LAVA:
                    tile_of_row.append(Lava())
                else:
                    tile_of_row.append(Empty())
            self._maze.append(tile_of_row) #add the list of tiles to maze
        #print error if row is invalid
        else:
            print("error")
    
    def get_tiles(self) -> list[list[Tile]]:
        """ Return list of tiles of maze """
        return self._maze
    
    def unlock_door(self) -> None:
        """ Unlock maze's door """
        #find door and unlock it
        for row in self._maze:
            for tile in row:
                if tile.get_id() == DOOR:
                    tile = tile.unlock()

    def get_tile(self, position: tuple[int, int]) -> Tile:
        """ Return the tils at position """
        row, col = position
        return self._maze[row][col]
    
    def __str__(self) -> str:
        maze_printing = ''
        printing_result = []
        for row in self._maze:
            for tile in row:
                maze_printing += tile.get_id()
        for char in range(0, len(maze_printing), self._dimensions[1]):
            printing_result.append(maze_printing[char: char + \
                                                 self._dimensions[1]])
        return str('\n'.join(printing_result))
        
    def __repr__(self):
        return f'{type(self).__name__}({self._dimensions})'

class Level():
    """ Class to represent Level

    Attributes:
        _level_dimen (tuple[int, int]): number of rows, columns in level
        _level_structure (Maze): return maze of level
        level_items (dict): return dictionary of items in level
        _player_position (tuple[int, int], optional): player's start position
        (default is None)
        _level_row_numb (int): row index in maze (default set to -1)

    Methods:
        get_maze: return _level_structure
        attempt_unlock_door: try to unlock maze's door
        add_row (row: str): add row in _level_structure, get player's start
        position, get item and item's position
        add_entity (position: tuple[int, int], entity_id: str): add postion
        and item in level_items
        get_dimemsions: return level's dimemsion
        get_items: return all items in this level
        remove_item (position: tuple[int, int]): remove item at postion from
        level_items
        add_player_start (position: tuple[int, int]): set _player_position to
        position
        get_player_start: return _player_position


    Examples:
    >>> level = Level((5, 5))
    >>> level
    Level((5, 5))
    >>> level.get_maze()
    Maze((5, 5))
    >>> level.get_maze().get_tiles()
    []
    >>> level.get_items()
    {}
    >>> level.get_player_start()
    >>> level.get_dimensions()
    (5, 5)
    >>> level.add_row('#####')
    >>> level.add_row('# C D')
    >>> level.add_row('# C #')
    >>> level.add_row('P C #')
    >>> level.add_row('#####')
    >>> print(level.get_maze())
    #####
    #   D
    #   #
        #
    #####
    >>> level.get_items()
    {(1, 2): Coin((1, 2)), (2, 2): Coin((2, 2)), (3, 2): Coin((3, 2))}
    >>> level.get_player_start()
    (3, 0)
    >>> level.add_entity((2, 3), 'M')
    >>> level.get_items()
    {(1, 2): Coin((1, 2)), (2, 2): Coin((2, 2)), (3, 2): Coin((3, 2)), (2, 3): Potion((2, 3))}
    >>> level.attempt_unlock_door()
    >>> print(level.get_maze())
    #####
    #   D
    #   #
        #
    #####
    >>> level.remove_item((1, 2))
    >>> level.remove_item((2, 2))
    >>> level.remove_item((3, 2))
    >>> level.get_items()
    {(2, 3): Potion((2, 3))}
    >>> level.attempt_unlock_door()
    >>> print(level.get_maze())
    #####
    #    
    #   #
        #
    #####
    >>> from pprint import pprint
    >>> pprint(level.get_maze().get_tiles())
    [[Wall(), Wall(), Wall(), Wall(), Wall()],
     [Wall(), Empty(), Empty(), Empty(), Door()],
     [Wall(), Empty(), Empty(), Empty(), Wall()],
     [Empty(), Empty(), Empty(), Empty(), Wall()],
     [Wall(), Wall(), Wall(), Wall(), Wall()]]
    >>> print(level)
    Maze: #####
    #    
    #   #
        #
    #####
    Items: {(2, 3): Potion((2, 3))}
    Player start: (3, 0)
    """
    def __init__(self, dimensions: tuple[int, int]) -> None:
        """ The constructor to initialize the class

        Parameters: 
            dimentsions (tuple[int, int]): number of rows and columns in level
        """
        self._level_dimen = dimensions
        self._level_structure = Maze(self._level_dimen)
        self.level_items = {}
        self._player_position = None
        self._level_row_numb = -1

    def get_maze(self) -> Maze:
        """ Return _level_structure """
        return self._level_structure
    
    def attempt_unlock_door(self) -> None:
        """ Try to unlock maze's door

        Parameters: 
            number_coins: number of coint in level_item
                if there is no coins in level_items, unlock the Door
        
        Return: 
            None
        """
        number_coins = 0
        #count number of coins in level items
        for position in self.level_items:
            if self.level_items[position].get_id() == COIN:
                number_coins +=1
        #no coin in level then door is unlocked
        if number_coins == 0:
            self._level_structure.unlock_door()

    def add_row(self, row: str) -> None:
        """ Add row in _level_structure. Add item in level_items using
        `Level.add_entity()`. Set player start position to _player_position

        Parameters:
            row (str): str of tile id 
                add row in _level_structure using `Maze().add_row`

        Return: 
            None    
        """
        self._level_structure.add_row(row)
        self._level_row_numb += 1
        #loop through the row to get item and player's positon
        for tile_numb in range(len(row)):
            if row[tile_numb] in [HONEY, WATER, POTION, APPLE, COIN]:
                self.add_entity((self._level_row_numb, tile_numb), \
                                row[tile_numb])
            elif row[tile_numb] == PLAYER:
                self.add_player_start((self._level_row_numb, tile_numb))

    def add_entity(self, position: tuple[int, int], entity_id: str) -> None:
        """ Add item to level_item
        
        Parameters:
            position (tuple[int, int]): position of item
            entity_id (str): entity id 
                add key = postion, value = Item(postion) corresponding to its
                id
        
        Return:
            None
        """
        if entity_id == POTION:
            self.level_items[position] = Potion(position)
        elif entity_id == WATER:
            self.level_items[position] = Water(position)
        elif entity_id == APPLE:
            self.level_items[position] = Apple(position)
        elif entity_id == COIN:
            self.level_items[position] = Coin(position)
        elif entity_id == HONEY:
            self.level_items[position] = Honey(position)

    def get_dimensions(self) -> tuple[int, int]:
        """ Return dismension of level """
        return self._level_dimen
    
    def get_items(self) -> dict[tuple[int, int], Item]:
        """ Return dictionary level_items"""
        return self.level_items
    
    def remove_item(self, position: tuple[int, int]) -> None:
        """ Remove item from level_items
        
        Parameters:
            position (tuple[int, int]): position of the item wanted to remove

        Return:
            None
        """
        del self.level_items[position]
    
    def add_player_start(self, position:tuple[int, int]) -> None:
        """ Set _play_position to posotion
        
        Parameters: 
            position(tuple[int, int]): player's position
        
        Return: 
            None
        """
        self._player_position = position
    
    def get_player_start(self) -> Optional[tuple[int, int]]:
        """ Return player start position in level """
        return self._player_position

    def __str__(self) -> str:
        return 'Maze: ' + str(self.get_maze()) + '\n' + 'Items: ' + \
               str(self.level_items) + '\n' + 'Player start: ' + \
               str(self._player_position)
    
    def __repr__(self):
        return f'{type(self).__name__}({self._level_dimen})'
        
class Model():
    """ Class to represent Model

    Attributes:
        _file_name (str): path of game text file
        _game: load text file using function `load_game()`
        _winning (bool): winning status
        _losing (bool): losing status 
        _current_levet (int): the current level of the game 
        _level_up (bool): whether users finish this level and move to next level
        in the game 
        number_of_moves (int): number of user's moves (default is 0)
        _player (Player): get player in the game

    Methods:
        has_won: return winning status
        has_los: return losing status
        get_level: get the current level of the game
        level_up: move users to next level of the game if any
        did_level_up: check if users level up
        move_player (delta: tuple[int, int]): change player position accoring to
        delta
        attempt_collect_item (position: tuple[int, int]): colect item at
        position
        get_player: return _player 
        get_player_stats: return player's status (hp, hunger, thirst)
        get_player_inventory: return player's inventory
        get_current_maze: return Maze() of current level 
        get_current_items: return dictionary of currrent item in the current
        level 
    
    Examples:
    >>> model = Model('a2\games\game1.txt')
    >>> print(model.get_level())
    Maze: #####
    #   D
    #   #
        #
    #####
    Items: {(1, 2): Coin((1, 2)), (2, 2): Coin((2, 2)), (3, 2): Coin((3, 2))}
    Player start: (3, 0)
    >>> model.has_won()
    False
    >>> model.has_lost()
    False
    >>> model.did_level_up()
    False
    >>> model.move_player((0, 1))
    >>> model.move_player((0, 1))
    >>> model.move_player((-1, 0))
    >>> print(model.get_level())
    Maze: #####
    #   D
    #   #
        #
    #####
    Items: {(1, 2): Coin((1, 2))}
    Player start: (3, 0)
    >>> print(model.get_player().get_position())
    (2, 2)
    >>> model.get_player_inventory().get_items()
    {'Coin': [Coin((3, 2)), Coin((2, 2))]}
    >>> model.get_current_items()
    {(1, 2): Coin((1, 2))}
    >>> model.get_player_stats()
    (97, 0, 0)
    >>> print(model.get_current_maze())
    #####
    #   D
    #   #
        #
    #####
    >>> model.attempt_collect_item((1, 2))
    >>> model.get_current_items()
    {}
    >>> print(model.get_current_maze())
    #####
    #    
    #   #
        #
    #####
    >>> model.level_up()
    >>> model.did_level_up()
    True
    >>> print(model.get_current_maze())
    ########
           #
    ###### #
    #      #
    # ######
    #      #
    ######D#
    >>> str(model)
    "Model('a2\games\game1.txt')"
    >>> model
    Model('a2\games\game1.txt')
    """
    def __init__(self, game_file: str) -> None:
        """ The constructor to initialize the class
        
        Parameters:
            game_file (str): path of game text file
        """
        self._file_name = game_file
        self._game = load_game(game_file)
        self._winning = False
        self._losing = False
        self._current_level = 0
        self._level_up = False
        self.number_of_moves = 0
        self._player = Player(self._game[self._current_level].get_player_start())

    def has_won(self) -> bool:
        """ Return wining status

        Parameters: 
            _current_level (int)
        
        Return: 
            True if _current_level is the last level"""
        if self._current_level == len(self._game):
            self._winning = True
        return self._winning
    
    def has_lost(self) -> bool:
        """ Return losing status

        Parameters:
            _player.get_health() (int): player's health
            _player.get_hunger() (int): player's hunger
            _player.get_thirst() (int): player's thirst
        
        Return: 
            True if player's health is 0 or player's hunger or thirt is max
        """
        if self._player.get_health() == 0 or self._player.get_hunger() == \
           MAX_HUNGER or self._player.get_thirst() == MAX_THIRST:
            self._losing = True
        return self._losing
    
    def get_level(self) -> Level:
        """ Return the current level of game"""
        return self._game[self._current_level]
    
    def level_up(self) -> None:
        """ Get users to level up. Set _player to the starting position of
        next level
        
        Parameters: 
            _current_level (int): 
                set _current_level to the next level index by + 1
            _level_up (bool): set to True
            
        Return:
            None
        """
        self._current_level += 1
        self._level_up = True
        #check if _current_level index in length of _game
        if self._current_level < len(self._game): 
            self._player.set_position(self.get_level().get_player_start())

    
    def did_level_up(self) -> bool:
        """ Return did_level_up status """
        return self._level_up

    def move_player(self, delta: tuple[int, int]) -> None:
        """ Try to change player position based on  the requested (row, column)
        change (delta). Try to level up. Collect items. Update player's status
        and inventory
        
        Parameters: 
            delta (tuple[int, int]): number of rows and columns to move
            next_location (tuple[int, int]): the new position of player if able
            to move 
        
        Return: 
            None        
        """
        #get new postion after move is made (if avaibale)
        next_location = tuple(map(sum, zip(self._player.get_position(), delta)))
        #check if player move through the door and get outside of the current
        #level's maze
        if next_location[0] == self.get_current_maze().get_dimensions()[0] or\
           next_location[1] == self.get_current_maze().get_dimensions()[1]:
            #if player next row or column position equals to the dimennsion of
            #level then player moves out of current level
            self.level_up() #user level up and move to next level
        else:
            #player move withtin current level
            if self.get_current_maze().get_tile(next_location).is_blocking() ==\
               False:
                self._player.set_position(next_location)
                self.attempt_collect_item(next_location)
                self.number_of_moves += 1
                if self.get_current_maze().get_tile(next_location).get_id() ==\
                   LAVA:
                    self._player.change_health(-1 - self.get_current_maze().\
                                               get_tile(next_location).damage())
                else: 
                    self._player.change_health(self.get_current_maze().\
                                               get_tile(next_location).damage()-1)
                if self.number_of_moves % 5 == 0:
                    self._player.change_hunger(1)
                    self._player.change_thirst(1) 
            
    
    def attempt_collect_item(self, position: tuple[int, int]) -> None:
        """ Collect item at the position 

        Parameters: 
            position (tuple[int, int]): row and column index of level
                if this position of current level has an item, remove it from
                the current item in level and add it to player inventory
        
        Return:
            None
        """
        if position in self._game[self._current_level].get_items():
            self._player.get_inventory().add_item(self._game[self._current_level]\
                                                  .get_items()[position])
            self._game[self._current_level].remove_item(position)
        self._game[self._current_level].attempt_unlock_door()    

    def get_player(self):
        """ Return _player"""
        return self._player 
    
    def get_player_stats(self) -> tuple[int, int, int]:
        """ Return player's health, hunger and thirst """
        return (self._player.get_health(), self._player.get_hunger(), \
                self._player.get_thirst())
    
    def get_player_inventory(self) -> Inventory:
        """ Return player's current inventory """
        return self._player.get_inventory()
    
    def get_current_maze(self) -> Maze:
        """ Return the maze of current level """
        return self._game[self._current_level].get_maze()
    
    def get_current_items(self) -> dict[tuple[int, int], Item]:
        """ Return the current items in the current level"""
        return self._game[self._current_level].get_items()
    
    def __str__(self):
        str_printing = str(type(self).__name__) + "('" + self._file_name + "')"
        return str_printing
    
    def __repr__(self):
        return f"{type(self).__name__}('{self._file_name}')"

class MazeRunner():
    """ Class to represent MazeRunner (gameplay)

    Attributes:
        _create_game (Model): set to Model(game_file) to set up the game
        _user_move: user input instruction for the game
        _game_play: set to view

    Methods: 
        play: main while loop of the game

    """
    def __init__(self, game_file: str, view: UserInterface) -> None:
        """ The constructor to initialize the class

        Parameters: 
            game_file (str): path to game text file
            view (UserInterface): get class 'UserInterface'
        """
        self._create_game = Model(game_file)
        self._user_move = None
        self._game_play = view


    def play(self) -> None:
        """ While loop of to run the game """
        #main while loop
        while not self._create_game.has_lost() and not \
              self._create_game.has_won():
            #draw the game interface 
            self._game_play.draw(self._create_game.get_level().get_maze(), \
                                 self._create_game.get_current_items(), \
                                 self._create_game.get_player().get_position(), \
                                 self._create_game.get_player_inventory(), \
                                 self._create_game.get_player_stats())
            #take user command
            self._user_move = str(input("\nEnter a move: "))
            #move player base on user's instruction
            if self._user_move in  ['w', 's', 'a', 'd']:
                self._create_game.move_player(MOVE_DELTAS[self._user_move])
            #Use item if user's input is 'i item_name'
            elif self._user_move.startswith("i"): 
                command, item = self._user_move.split(' ') #get item_name
                #check in user have the item in the inventory 
                if item in ['Apple', 'Honey', 'Water', 'Potion']:
                    item_used = self._create_game.get_player_inventory().\
                                remove_item(item)
                    item_used.apply(self._create_game.get_player())
                else:
                    #if there is no item in user's inventory
                    #print the message
                    print(ITEM_UNAVAILABLE_MESSAGE) 

        if self._create_game.has_lost() == True: #check for winning condition 
            print("You lose :(")
        elif self._create_game.has_won() == True: #check for losing condition
            print("Congratulations! You have finished all levels and won the game!")    
            

def main():
    file_name = str(input("Enter game file: ")) 
    let_play = MazeRunner(file_name, TextInterface())
    let_play.play()
    
    
    

if __name__ == '__main__':
    main()

# import doctest
# doctest.testmod()

