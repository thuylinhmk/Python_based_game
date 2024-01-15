import tkinter as tk
from tkinter import messagebox, Menu
from tkinter.simpledialog import askstring
from PIL import  ImageTk, Image
from tkinter import filedialog 

from gui_support import AbstractGrid
from constants import GAME_FILE, TASK
from typing import Union, Callable
from gaming import *


# Write your classes here
class LevelView(AbstractGrid):
    """ Class Level inteface that uses different shapes of tk.Canvas to draw \
        the maze
    """
    def draw(
        self, 
        tiles: list[list[Tile]], 
        items: dict[tuple[int, int], 'Item'],
        player_pos: tuple[int, int]
        ) -> None:
        """ Draw the current level

            Parameters: 
                tiles: list of tiles of the current level
                items: dictionary of items' postion and items
                player_pos: current player's postion (row, column)
        """
        #clear all existing cell
        self.clear() 

        #draw the maze
        for row in range(self._dimensions[0]):
            for column in range(self._dimensions[1]):
                if tiles[row][column].get_id() in [WALL, LAVA, DOOR]:
                    self.create_rectangle(self.get_bbox((row, column)),\
                        fill = TILE_COLOURS[tiles[row][column].get_id()])
                #draw empty tiles and items if available
                elif tiles[row][column].get_id() == EMPTY:
                    self.create_rectangle(self.get_bbox((row, column)),\
                        fill = TILE_COLOURS[EMPTY], tags = EMPTY)
                    if (row, column) in items:
                        self.create_oval(self.get_bbox((row, column)),\
                            fill = ENTITY_COLOURS[items[(row, column)].get_id()])
                        self.annotate_position((row, column), 
                                            items[(row, column)].get_id())
                #if player in this position then draw player
                if (row, column) == player_pos:
                        self.create_rectangle(self.get_bbox(player_pos), 
                                            fill = TILE_COLOURS[EMPTY])
                        self.create_oval(self.get_bbox(player_pos), 
                                        fill = ENTITY_COLOURS[PLAYER])
                        self.annotate_position(player_pos, PLAYER)
                    
class StatsView(AbstractGrid):
    """ Class Stats inteface that uses tk.Canvas to draw player's status and \
        coins"""  

    def __init__(self, master: Union[tk.Tk, tk.Frame], width: int, **kwargs) -> None:
        super().__init__(
            master= master,
            dimensions= (2,4),
            size= (width, STATS_HEIGHT),
            **kwargs)
        #set backgroud color
        self['bg'] = THEME_COLOUR
        
    def draw_stats(self, player_stats: tuple[int, int, int]) -> None:
        """ Draw player status

            Parameters: 
            player_stats: Tuple (HP, hunger, thirst) of the player
        """
        stat_name = ('HP', 'Hunger', 'Thirst')
        for index in range(self._dimensions[1]-1):
            self.annotate_position((0, index), stat_name[index])
            self.annotate_position((1, index), player_stats[index])

    def draw_coins(self, num_coins: int) -> None:
        """ Draw number of coins player have

            Parameters:
            num_coins: number of coins in player inventory
        """
        self.annotate_position((0, 3), 'Coins')
        self.annotate_position((1, 3), str(num_coins))

class InventoryView(tk.Frame):
    """ Class Inventory inteface that uses different shapes of tk.Canvas to\
        draw the maze
    """
    _usage_item = ('Water', 'Potion', 'Apple', 'Honey', 'Candy')

    def __init__(self, master: Union[tk.Tk, tk.Frame], **kwargs) -> None:
        tk.Frame.__init__(self, master, width = INVENTORY_WIDTH, height = MAZE_HEIGHT)
        self.label1 = tk.Label(self, text="Inventory", font = HEADING_FONT)
        self.label1.pack(fill = tk.X)
        self.draw_an_i = tk.Label(self)
        self.draw_an_i.pack()
        
        
    def set_click_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback command 

            Parameters:
            callback: callable function name as str
        """
        self._command = callback
                        
    def clear(self) -> None:
        """ Delete all the labels except for the 'Inventory' label """
        for label in self.winfo_children():
            if label != self.label1:
                label.destroy()    
    
    def _draw_item(self, name: str, num: int, colour: str) -> None:
        """ Draw item label

            Parameters:
            name (str): name of the item 
            num (int): number of the item 
            colour (str): colour background for the item
        """
        draw_an_i = tk.Label(self, text = name + ': ' + str(num), bg = colour, relief = tk.RAISED) 
        draw_an_i.pack(fill = tk.X)
        draw_an_i.bind('<Button-1>', lambda i: self._command(name))

    def draw_inventory(self, inventory: Inventory) -> None:
        """ Draw all items in player's inventory

            Parameters: Player's inventory
        """
        self.clear()
        self._inventory = inventory
        self._inventory_item = inventory.get_items()
        if self._inventory_item != {}:
            for each_item in self._inventory_item:
                if each_item in self._usage_item:
                    self._draw_item(each_item,
                                len(self._inventory_item[each_item]),
                                ENTITY_COLOURS[self._inventory_item[each_item][0].get_id()])

class FileMenu(tk.Tk):
    """ Class FileMenu inteface that use Menu to draw task bar and menu """
    def __init__(self, master: Union[tk.Tk, tk.Frame], **kwargs) -> None:
        #create taskbar
        self._master = master
        self._taskbar = Menu(self._master)
        self._master.config(menu=self._taskbar)
        self._menu = Menu(self._taskbar, tearoff = False)

    def draw_filemenu(self) -> None:
        """ Draw task bar and menu """
        #create menu items in taskbar
        self._menu.add_command(label = 'Save game', 
                                command = self._save_cmd)
        self._menu.add_command(label = 'Load game',
                                command = self._load_cmd)
        self._menu.add_command(label = 'Restart game',
                                command = self._restart_cmd)
        self._menu.add_separator()
        self._menu.add_command(label = 'Quit', 
                                command = self._quit_cmd)
        
        #set menu items to 'File' in taskbar
        self._taskbar.add_cascade(label="File", menu = self._menu)
    
    def set_save_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Save game item """
        self._save_cmd = callback

    def set_load_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Load game item """
        self._load_cmd = callback

    def set_restart_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Restart game item """
        self._restart_cmd = callback
    
    def set_quit_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Quit game item """
        self._quit_cmd = callback
              
class ImageLevelView(LevelView):
    """ Class ImageLevel inherit from LevelView that draws the current level\
        with images """
    _image_storage=[]
    def draw(self, tiles, items, player_pos):
        """ Draw the current level """
        self.clear()
        image_path = 'images/'

        for row in range(self._dimensions[0]):
            for column in range(self._dimensions[1]):
                if tiles[row][column].get_id() in [WALL, LAVA, DOOR, EMPTY]:
                    tile_id = tiles[row][column].get_id()
                    #load, resize and save the image
                    tile_image = Image.open(image_path+ TILE_IMAGES[tile_id])
                    tile_resize = tile_image.resize(self.get_cell_size())
                    tile_ph = ImageTk.PhotoImage(tile_resize, master = self)
                    self._image_storage.append(tile_ph)
                    #draw image in the level canvas
                    self.create_image(self.get_midpoint((row, column)),
                                        image = tile_ph)
                    #draw item of level
                    if (row, column) in items:
                        item_id = items[(row, column)].get_id()
                        item_image = Image.open(image_path + ENTITY_IMAGES[item_id])
                        item_resize = item_image.resize(self.get_cell_size())
                        item_ph = ImageTk.PhotoImage(item_resize, master=self)
                        self._image_storage.append(item_ph)
                        self.create_image(self.get_midpoint((row, column)),
                                        image = item_ph)
                # draw player
                if (row, column) == player_pos:
                    player_image = Image.open(image_path + ENTITY_IMAGES[PLAYER])
                    player_resize = player_image.resize(self.get_cell_size())
                    player_ph = ImageTk.PhotoImage(player_resize, master=self)
                    self._image_storage.append(player_ph)
                    self.create_image(self.get_midpoint(player_pos), 
                                    image = player_ph)

class ControlsFrame(tk.Frame):
    """ Class ControlsFrame interface that draw control frame """
    first_line_item = {
        APPLE: '$1',
        WATER: '$1',
        HONEY: '$2'
        }
    second_line_item = {
        POTION: '$2', 
        CANDY: '$3'
        }
    _item_image = []
    def __init__(self, master: Union[tk.Tk, tk.Frame], **kwargs) -> None:
        tk.Frame.__init__(self, 
                        master, 
                        height = STATS_HEIGHT, 
                        width = MAZE_WIDTH + INVENTORY_WIDTH
                        )
        self._running = False #true if the game is playing
        self._sec_count = 0
        
    def create_button(self):
        """ Draw buttons """
        if TASK == 3:
            self._shop_button = tk.Button(self, text = 'Shop', 
                                    font = TEXT_FONT,
                                    relief = tk.GROOVE,
                                    command = self.shop_open)
            self._shop_button.pack(side = tk.LEFT, expand = tk.TRUE)

        self._rs_button = tk.Button(self, text = 'Restart game', 
                                    font = TEXT_FONT, 
                                    relief = tk.GROOVE,
                                    command = self._rs_cmd)
        self._rs_button.pack(side = tk.LEFT, expand = tk.TRUE)

        self._ng_button = tk.Button(self, text = 'New game', 
                                    font = TEXT_FONT,
                                    relief = tk.GROOVE,
                                    command = self._ng_cmd)
        self._ng_button.pack(side = tk.LEFT, expand = tk.TRUE)

    def timer_draw(self) -> None:
        """ Draw timer """
        #create frame for timer
        time_frame = tk.Frame(self)
        time_frame.pack(side = tk.RIGHT, expand = tk.TRUE)
        #'Timer' label
        time_label = tk.Label(time_frame, text = 'Timer', font = TEXT_FONT)
        time_label.pack(side = tk.TOP, expand = tk.TRUE)
        #time displaying label in minutes and seconds
        self._timer_view = tk.Label(time_frame, text = '0m ' + str(self._sec_count) + 's', font = TEXT_FONT)
        self._timer_view.pack(side = tk.TOP, expand = tk.TRUE)
        self._timer_view.after(1000, self.couting_time)

    def couting_time(self) -> None:
        """ Count time function and set it to the display """
        self._sec_count +=1 
        second = self._sec_count%60 # calculate second
        minute = int(self._sec_count/60) # calculate minute
        display_time = str(minute) + 'm ' + str(second) + 's'
        # change the display label into current minute and second
        self._timer_view.configure(text = display_time)
        self._timer_view.after(1000, self.couting_time)

    def draw(self):
        """ Draw the ControlFrame and set to running state"""
        if self._running == False:
            self.create_button()
            self.timer_draw()
            self._running = True

    def stop_running(self) -> None:
        """ Stop the timer and set running to false"""
        self._sec_count = 0
        self._running = False

    def set_restart_callback(self, callback: Callable[[str], None]) -> None:
        """ Set restart callback function """
        self._rs_cmd = callback
    
    def set_newgame_callback(self, callback: Callable[[str], None]) -> None:
        """ Set new game callback function """
        self._ng_cmd = callback
    
    def set_shop_callback(self, callback: Callable[[str], None]) -> None:
        """ Set shop callback function """
        self._shop_cmd = callback

    def shop_open(self) -> None:
        """ Draw popup window for shop with all items """
        def draw_item(item: str, price_list: dict, line_frame = tk.Frame) \
            -> 'Label':
            """ Draw item image """
            path_prefix = 'images/'
            size_image = (MAZE_WIDTH//3, MAZE_WIDTH//3)
            #load, rezise and save the items' images
            image = Image.open(path_prefix + ENTITY_IMAGES[item])
            image_resize = image.resize(size_image)
            image_save = ImageTk.PhotoImage(image_resize, 
                                            master = self._shop_window)
            self._item_image.append(image_save)
            #create label display item's image and price
            item_label = tk.Label(line_frame, width=MAZE_WIDTH//3, 
                                    text = price_list[item], 
                                    image=image_save, 
                                    compound = tk.TOP, 
                                    relief = tk.GROOVE,
                                    font = TEXT_FONT)
            item_label.bind('<Button-1>', lambda i: self._shop_cmd(item))
            return item_label
        #create popup Shop window    
        self._shop_window = tk.Toplevel(self, height=MAZE_HEIGHT, width = MAZE_WIDTH)
        self._shop_window.title('Shop')
        shop_label = tk.Label(self._shop_window, text = 'Shop', font = HEADING_FONT, bg = THEME_COLOUR)
        shop_label.pack(side = tk.TOP, fill = tk.X)
        #create Done button
        done_button = tk.Button(self._shop_window, text = 'Done', 
                                font = TEXT_FONT, 
                                relief= tk.GROOVE, 
                                command = self._shop_window.destroy)
        done_button.pack(side = tk.BOTTOM, expand = tk.TRUE)
        #Displaying items Shop
        second_line = tk.Frame(self._shop_window)
        second_line.pack(side = tk.BOTTOM, expand = tk.TRUE, fill = tk.X)

        for first_item in self.first_line_item:
            draw_item(first_item, self.first_line_item, self._shop_window).pack(side = tk.LEFT, expand = tk.TRUE)
        for sec_item in self.second_line_item:
            draw_item(sec_item, self.second_line_item, second_line).pack(side = tk.LEFT, expand = tk.TRUE)
        
    def clear(self):
        """ Delete all the widgets in ControlsFrame"""
        if self._running == False:
            for widget in self.winfo_children():
                widget.destroy()

class Candy(Food):
    """ A Candy restores player's hunger to 0 but reduces the health by 2 when\
        applied """
    _id = CANDY
    _amount_hp = -2
    _amount_hunger = 0 - MAX_HUNGER

    def apply(self, player: 'Player'):
        """ Decreases player's hunger to 0 and HP by 2 """
        player.change_hunger(self._amount_hunger)
        player.change_health(self._amount_hp)

class GraphicalInterface(UserInterface):
    """ A MazeRunner interface that uses color shapes or images to present\
        maze """
    def __init__(self, master: tk.Tk) -> None:
        self._master = master
        master.title('MazeRunner')
        self.game_label = tk.Label(master, 
                                    text = 'MazeRunner', 
                                    font = BANNER_FONT,
                                    bg = THEME_COLOUR)
        self.game_label.pack(side = tk.TOP, expand = tk.TRUE, fill = tk.BOTH)
        self._inventory = Inventory()
        self._menu = False
    
    def create_interface(self, dimensions: tuple[int, int]) -> None:
        """ Set up display for level, inventory, controlsframe, filemenu """
        #create controlsframe
        if TASK in [2, 3]:
            self._controller_hud = ControlsFrame(self._master)
            self._controller_hud.pack(side = tk.BOTTOM, expand = tk.TRUE, fill = tk.X)
            self._filemenu_hud = FileMenu(self._master)
            
        #create status
        self._stat_hud = StatsView(self._master, MAZE_WIDTH + INVENTORY_WIDTH)
        self._stat_hud.pack(side = tk.BOTTOM, expand = tk.TRUE)
        
        #create level
        if TASK == 1:
            self._level_hud = LevelView(self._master, dimensions, (MAZE_WIDTH, MAZE_HEIGHT))
        elif TASK in [2, 3]:
            self._level_hud = ImageLevelView(self._master, dimensions, (MAZE_WIDTH, MAZE_HEIGHT)) 
        self._level_hud.pack(side = tk.LEFT, anchor = tk.NE)

        #create inventory
        self._inventory_hud = InventoryView(self._master)
        self._inventory_hud.pack(side = tk.LEFT, anchor = tk.NW,
                                 expand = tk.TRUE, fill = tk.BOTH)
        
    def clear_all(self) -> None:
        """ Clear all widgets in the game for redraw the current gameplay """
        self._level_hud.clear()
        self._inventory_hud.clear()
        self._stat_hud.clear()
        if TASK in [2, 3]:
            self._controller_hud.clear()
    
    def clear_for_reset(self) -> None:
        """ Clear all widgets for the new gameplay"""
        self._level_hud.clear()
        self._inventory_hud.clear()
        self._stat_hud.clear()
        self._controller_hud.stop_running()
        self._controller_hud.clear()
    
    def set_maze_dimensions(self, dimensions: tuple[int, int]) -> None:
        """ Set the maze dimemsions:

            Parameters:
            dimensions: tuple (number of rows, number of columns)
        """
        self._level_hud.set_dimensions(dimensions)

    def bind_keypress(self, command: Callable[[tk.Event], None]) -> None:
        """ Bind key press to callable function for gameplay main window"""
        self._master.bind('<Key>', command)
    
    def set_inventory_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Inventory interface """
        self._inventory_hud.set_click_callback(callback)
    
    def set_restart_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to restart in Controlsframe and FileMenu\
            interface"""
        self._controller_hud.set_restart_callback(callback)
        self._filemenu_hud.set_restart_callback(callback)
    
    def set_newgame_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Newgame button """
        self._controller_hud.set_newgame_callback(callback)
    
    def set_load_callback(self, callback: Callable[[None], None]) -> None:
        """ Set callback function to Load game in FileMenu """
        self._filemenu_hud.set_load_callback(callback)

    def set_quit_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Quit in FileMenu """
        self._filemenu_hud.set_quit_callback(callback)
    
    def set_save_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Save game in FileMenu """
        self._filemenu_hud.set_save_callback(callback)
    
    def set_shop_callback(self, callback: Callable[[str], None]) -> None:
        """ Set callback function to Shop """
        self._controller_hud.set_shop_callback(callback)
        
    def draw_inventory(self, inventory: Inventory):
        """ Draw inventory

            Parameters:
            inventory: Inventory()
        """
        self._inventory_hud.draw_inventory(inventory)
    
    def draw(self, 
        maze: Maze, items: dict[tuple[int, int], Item],
        player_position: tuple[int, int], 
        inventory: Inventory,
        player_stats: tuple[int, int, int]
        ) -> None:
        """ Draw gameplay interface"""
        #clear all existing widgets
        self.clear_all()
        #set maze dimension 
        self.set_maze_dimensions(maze.get_dimensions())
        #draw the maze and other information interface
        self._draw_level(maze, items, player_position)
        self._draw_inventory(inventory)
        self._draw_player_stats(player_stats)
        if TASK in [2, 3]:
            self._draw_control()
            if self._menu == False:
                self._menu = True
                self._draw_filemenu()

    def _draw_inventory(self, inventory: Inventory) -> None:
        """ Draws the inventory information and coin
        
            Parameters:
            inventory: Inventory 
        """
        self._inventory = inventory
        self._items = inventory.get_items()
        if self._items != {}:
            self.draw_inventory(inventory)
        if 'Coin' in self._items:
            num_coin = len(self._items['Coin'])
        else:
            num_coin = 0
        self._stat_hud.draw_coins(num_coin)

    def _draw_level(self, 
                    maze: Maze, 
                    items: dict[tuple[int, int], Item],
                    player_position: tuple[int, int]
                    ) -> None:
        """ Draws the maze and all its items.
        
            Parameters:
            maze: The maze for the level
            items: Maps locations to the items currently at those locations
            player_position: The position of the player
        """
        self._level_hud.draw(maze.get_tiles(), items, player_position)
    
    def _draw_player_stats(self, player_stats: tuple[int, int, int]):
        """ Draws the maze and all its items.
        
            Parameters:
            player_stats: tuple (HP, hunger, thisrt) as player's status
        """
        self._stat_hud.draw_stats(player_stats)

    def _draw_control(self):
        """ Draw the Controlsframe """
        self._controller_hud.draw()
    
    def _draw_filemenu(self):
        """ Draw FileMenu """
        self._filemenu_hud.draw_filemenu()

class ModelSaveMode(Model):
    """ Extended class from class Model() to handle the save gameplay """
    def __init__(self, game_file: str):
        super().__init__(game_file)
        self._levels = self.load_save_game(game_file)
        self._player = Player(self.get_level().get_player_start())

        hp_change = self._save_stat[0] - MAX_HEALTH
        hunger_change = self._save_stat[1]
        thirst_change = self._save_stat[2]
        self._player.change_health(hp_change)
        self._player.change_hunger(hunger_change)
        self._player.change_thirst(thirst_change)

        for a_item in self._save_items:
            self._player.get_inventory().add_item(a_item)

        self._level_num = 0
        self._won = False
        self._did_level_up = False
        self._num_moves = 0
        self._game_file = game_file

        self.get_level().attempt_unlock_door()
              
    def load_save_game(self, game_file) -> list['Level']:
        """ Reading the save game file 
        
            Parameters:
            game_file(str): path to save game file

            Returns:
            A list of all Level instances to recreate the save game maze
        """
        ITEM = {'Coin': Coin,
                'Water': Water, 
                'Honey': Honey,
                'Apple': Apple,
                'Potion': Potion,
                'Candy': Candy}
        self._save_items = []
        levels = []
        with open(game_file, 'r') as file:
            for line in file:
                if line.startswith('Current Position'):
                    _, _, position = line.partition(' - ')
                    save_pos = tuple(map(int, position.split(', ')))

                elif line.startswith('Inventory'):
                    _, _, inventory = line.partition(' - ')
                    if inventory != '\n':
                        save_inv = tuple(inventory.split('+'))
                        for item in save_inv:
                            item_name, position = item.split(':')
                            position = tuple(map(int, position.split(',')))
                            if item_name in ITEM:
                                self._save_items.append(ITEM[item_name](position))

                elif line.startswith('Stat'):
                    _, _, stat = line.partition(' - ')
                    self._save_stat = tuple(map(int, stat.split(', ')))

                else:
                    if line.startswith('Maze'):
                        _, _, dimensions = line[5:].partition(' - ')
                        dimensions = [int(item) for item in dimensions.split()]
                        levels.append(Level(dimensions))
                    elif len(line) > 0 and len(self._levels) > 0:
                        levels[-1].add_row(line)
        return levels

class GraphicalMazeRunner(MazeRunner):
    """ Extend from MazeRunner class for a gameplay """
    def __init__(self, game_file: str, root: tk.Tk) -> None:
        """ Sets up initial game state
        
            Parameters:
            game_file: Path to the file from which the game levels are loaded
            root:  starting Interface to manage the display of information
        """
        self._game_file = game_file
        self._model = Model(self._game_file)
        self._master = root 
        self._game_start = GraphicalInterface(self._master)
        self._game_start.create_interface(self._model.get_current_maze().get_dimensions())
        if TASK in [2, 3]:
            self._isloadgame = False #False if this is an orignal gamefile
            #second model for saving purpose
            self.save_model = Model(self._game_file)
            

    def _handle_keypress(self, e: tk.Event) -> None:
        """ Handle the update for player movement """
        #player move
        if e.char in ('w', 'a', 's', 'd'):
            self._model.move_player(MOVE_DELTAS.get(e.char))
            
            #update the saving model to be the same as current model
            if TASK in [2, 3]:
                if self.save_model.has_won() == False:
                    self.save_model.attempt_collect_item(self._model.get_player().get_position())
                    self.save_model.get_player().set_position(self._model.get_player().get_position())
                if self._model.has_won() == False and \
                    self._model.did_level_up() == True:
                    self.save_model.level_up()
            #checking wining and losing condition   
            if self._model.has_won():
                messagebox.showinfo('Game Status', WIN_MESSAGE) 
            elif self._model.has_lost():
                messagebox.showinfo('Game Status', LOSS_MESSAGE)
            else:
                self._redraw() # continue game play if not winning/losing
        
        
    def _redraw(self) -> None:
        """ Redraws the entire view based on the current model state. """
        model = self._model
        maze = model.get_current_maze()
        items = model.get_current_items()
        player_position = model.get_player().get_position()
        inventory = model.get_player_inventory()
        player_stats = model.get_player_stats()
        self._game_start.draw(maze, items, player_position, inventory, player_stats)

    def _apply_item(self, item_name: str) -> None:
        """ Apply item to player

            Parameters:
            item_name(str) : name of item want to apply
        """
        player = self._model.get_player()
        #get and remove the item from player inventory 
        item = self._model.get_player().get_inventory().remove_item(item_name)
        #apply the item if exists
        if item is not None:
            item.apply(self._model.get_player())
            self._redraw()
    
    def _restart(self) -> None:
        """ Restart the whole maze from the beginning """
        self._game_start.clear_for_reset()
        if TASK == 1:
            self._model = Model(self._game_file)
        elif TASK in [2, 3]:
            if self._isloadgame == False:
                self._model = Model(self._game_file)
                self.save_model = Model(self._game_file)
            else: 
                self._model = ModelSaveMode(self._game_file)
                self.save_model = ModelSaveMode(self._game_file)
        self._redraw()
    
    def _newgame(self) -> None:
        """ Create newgame popup windown to get user input for file path """
        self._ng_window = tk.Toplevel(self._master)
        self._ng_window.title('New Game?')
        self._ng_window.geometry('400x200')

        text_mess = tk.Label(self._ng_window, text = 'Please input path to a new game file', font = ('Courier', 13))
        text_mess.pack(side = tk.TOP, anchor = tk.CENTER, expand = tk.TRUE)
        
        #get user input through text box
        self.user_file = tk.Entry(self._ng_window, width=50)
        self.user_file.pack(side = tk.TOP, anchor = tk.CENTER, expand = tk.TRUE)

        #load button
        load_button = tk.Button(self._ng_window, 
                                text = "Load", 
                                command = self._handle_new_game)
        load_button.pack(side = tk.BOTTOM, anchor = tk.CENTER, expand = tk.TRUE)

    
    def _handle_new_game(self, event=None) -> None:
        """ Handle the inputing path of new game file (orginal gamefile)  """

        new_game = self.user_file.get()
        
        if new_game.startswith('games') and new_game.endswith('.txt'):
            self._isloadgame = False #not a save game file
            # file_game = open(new_game, 'r')
            # file_game.close()
            self._ng_window.destroy()
            self._game_file = new_game
            self._restart()
        
        #Invalid path; showing error message
        else:
            messagebox.showinfo('Error', 'The game file was not valid')
            self._ng_window.destroy()

    def _savegame(self) -> None:
        """ Save the current gameplay """
        #create popup window to get user prompt for save path
        self._create_file = filedialog.asksaveasfilename(
                                parent = self._master)
        #create save file
        if self._create_file is not None and self._create_file.endswith('.txt'):
            self._create_save_file()
        
        #invalid and show error message
        else:
            messagebox.showinfo('Error', 'The save game file was not valid')
    

    def _create_save_file(self, event=None) -> None:
        """ Write a savegame file base on the game model """

        game_path = self._create_file
        
        def save_current_level(
            maze: 'Maze',
            items: dict[tuple[int, int], 'Item'],
            player_position: tuple[int, int]) -> str:
            """ Set up the save level 

                Parameters:
                maze: current maze level
                items: current items in the level
                player_position: player current positon

                Return:
                string form of the level
            """
            num_rows, num_cols = maze.get_dimensions()
            level_construct = '\nMaze x - ' + str(f'{num_rows} {num_cols}') + '\n'
            for row in range(num_rows):    
                for col in range(num_cols):
                    if (row, col) == player_position:
                        level_construct += PLAYER
                    elif (row, col) in items:
                        level_construct += items.get((row, col)).get_id()
                    else:
                        if repr(maze.get_tile((row, col))) == 'Door()':
                            level_construct += DOOR
                        else: 
                            level_construct += maze.get_tile((row, col)).get_id()
                level_construct += '\n'
            return level_construct    
        
        def save_current_inventory(inventory: 'Inventory') -> str:
            """ Set up the save player inventory 
            
                Parameters:
                inventory: Inventory()

                Return:
                save string form of inventory
            """
            current_inventory = inventory.get_items()
            current_item = []
            for item_name in current_inventory:
                for item in current_inventory[item_name]:
                    save_item = str(item.get_name()) + ':' + str(item.get_position()[0]) + ', ' + str(item.get_position()[1]) 
                    current_item.append(save_item)
            to_save = '+'.join(current_item)
            saved_inv = 'Inventory - ' + str(to_save) + '\n'
            return saved_inv
        
        def save_player_position(position: tuple[int, int]) -> str:
            """ Set up the save player inventory 
            
                Parameters:
                position: tuple of player's position

                Return:
                save string form of player's position
            """
            row, col = position
            save_pos = 'Current Position - ' + str(row) + ', ' + str(col) + '\n'
            return save_pos

        def save_player_stat(player_stats: tuple[int, int, int]) -> str:
            """ Set up the save player inventory 
            
                Parameters:
                player_stats: tuple (hp, hunger, thirst) status of player

                Return:
                save string form of player status
            """
            hp, hunger, thirst = player_stats
            saved_player_stat = 'Stat - ' +  f'{hp}, {hunger}, {thirst}'
            return saved_player_stat


        #create the text file to save game
        if game_path.endswith('.txt'):
            save_game = open(game_path,'w+')
            p_inv = save_current_inventory(self._model.get_player_inventory())
            p_pos = save_player_position(self._model.get_player().get_position())
            p_stat = save_player_stat(self._model.get_player_stats())
            save_write = [p_inv, p_pos, p_stat]
            while self.save_model.has_won() == False:
                level = save_current_level(
                    maze = self.save_model.get_current_maze(), 
                    items = self.save_model.get_current_items(), 
                    player_position = self.save_model.get_player().get_position())
                save_write.append(level)
                self.save_model.level_up()
            save_game.writelines(save_write)
            save_game.close()

        #invalid path; show error message
        else:
            messagebox.showinfo('Error', 'The game file was not valid')
        

    def _load_game(self):
        """ Recreate the maze game with save file """
        def read_save_file(game_file: str) -> None:
            """ Set up the model to the savegame 

                Parameters:
                game_file(str): path to the save game file            
            """
            self._game_start.clear_for_reset()
            self._model = ModelSaveMode(game_file)
            self.save_model = ModelSaveMode(game_file)
            self._redraw()
        
        #create popup window to get the savegame path
        self._save_file = filedialog.askopenfilename(
                                parent = self._master)

        #load the savegame path and run the save game
        if self._save_file != '' and self._save_file.endswith('.txt'):
            self._game_file = self._save_file
            read_save_file(self._save_file)
            self._isloadgame = True #set True as this is the save game

        #invalid; showing the error message
        else:
            messagebox.showinfo('Error', 'The save game file was not valid')


    def _quit(self) -> None:
        #create popup window
        self._quit_window = tk.Toplevel(self._master)
        self._quit_window.title('Quit')
        text_mess = tk.Label(self._quit_window, text = 'Are you sure you want to quit the same :< ?')
        text_mess.pack()

        #yes button
        yes_button = tk.Button(self._quit_window, 
                                text = "Yes", 
                                command = self.bye_game)
        yes_button.pack(side = tk.LEFT, ipadx = 5, expand = tk.TRUE)
        
        #no button 
        no_button = tk.Button(self._quit_window, 
                                text = 'No', 
                                command = self._quit_window.destroy)
        no_button.pack(side = tk.RIGHT, ipadx = 5, expand = tk.TRUE)
    
    def bye_game(self) -> None:
        """ Quit the game """
        self._quit_window.destroy()
        exit()
    
    def _handle_shop(self, item_name: str) -> None:
        """ Handle buying function of Shop 

            Parameters:
            item_name(str): name of item want to buy
        """
        item_price = {
            APPLE: (1, Apple),
            WATER: (1, Water),
            HONEY: (2, Honey),
            POTION: (2, Potion),
            CANDY: (3, Candy)
            }
        player_inventory = self._model.get_player_inventory()
        pseudo_position = (0, 0) #a fake position to call class Item()
        paid_price = item_price[item_name][0] #price of item

        #get how many coins player have
        if 'Coin' in player_inventory.get_items():
            money = len(player_inventory.get_items()['Coin'])
        else:
            money = 0
        money_left = money - paid_price #number of coins left after buying

        #buy item if having enough coin
        if money_left >= 0:
            while paid_price > 0:
                player_inventory.remove_item('Coin')
                paid_price -= 1
            item = item_price[item_name][1](pseudo_position)
            player_inventory.add_item(item)
        # print(self._model.get_player_inventory())    
        self._redraw()


    def play(self) -> None:
        """ Bind all the callback function. Set up game to play"""
        self._game_start.bind_keypress(self._handle_keypress)
        self._game_start.set_inventory_callback(self._apply_item)
        if TASK in [2, 3]:
            self._game_start.set_newgame_callback(self._newgame)
            self._game_start.set_restart_callback(self._restart)
            self._game_start.set_quit_callback(self._quit)
            self._game_start.set_save_callback(self._savegame)
            self._game_start.set_load_callback(self._load_game)
            if TASK == 3:
                self._game_start.set_shop_callback(self._handle_shop)
        self._game_start.clear_all()
        self._redraw()

   

def play_game(root: tk.Tk):
    """ Create main game window and execute the game """
    maze_game = GraphicalMazeRunner(GAME_FILE, root)
    maze_game.play()
        
def main():
    """ Entry-point to gameplay """
    root = tk.Tk()
    play_game(root)
    root.mainloop()
    

if __name__ == '__main__':
    TASK = 3
    main()





