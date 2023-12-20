# Author: Mackenzie Anderson
# GitHub username: mkenzieanderson
# Date: December 7, 2023
# Description: Programs a variant form of chess. In this form of chess, a team wins once all that team has captured
# all of the pieces of a single type. The board starting position and the restrictions on each piece type movement
# remains the same as standard chess. Special moves, such as castling, en passant, and pawn promotion, are not
# permitted in this version of chess. There is no check or checkmate. The ChessVar class contains private data members
# for two ChessTeam objects (Black and White team), a data member to keep track of whose turn it is, and a data
# member to track the state of the game (unfinished vs. a team has won). The ChessVar methods contain various get
# and set methods for its data members, and methods for making and validating moves and captures. The ChessTeam
# class has a dictionary data member to keep track of a team's pieces and their specific locations, and a list that
# tracks current squares that are occupied by that team's pieces. The ChessTeam methods include various get and set
# methods for its data members, and methods to check whether pieces of one type have all been captured

class ChessTeam:
    """The ChessTeam class holds information about a team’s pieces. Its three data members include the team color, a
    list of all the squares (coordinates) that are currently occupied by this team’s pieces, and a dictionary that stores
    each piece by name (key) and each piece’s current location, type, and number of times moved (value, which is a list
    with these three information pieces). This class has get and set methods for both of its data members, a method that
    checks the list of occupied squares to determine whether a certain square is currently occupied, and two methods
    that work in conjunction to determine whether all pieces of a single type have been captured. There is also a method
    that specifically checks whether a pawn move is valid"""


    def __init__(self, team_color, starting_squares_list):
        """A string of the team color (BLACK or WHITE) and a  list containing the 16 piece starting square coordinates
        (eg. ‘a1’) will be the passed parameters. The _team_color data member is assigned to the team_color passed
        parameter, and the _squares_in_use data member will be set equal to this passed list.  The _pieces data member
        will be a dictionary with piece names as the key (eg. “PAWN7”) and their type (eg. “pawn”), number of times the
        piece has moved (eg. 3) and current square location (eg. ‘a7’) all in a list as the value. This dictionary is
        created by iterating through the passed list of starting_spaces to assign each piece with its starting value"""

        self._team_color = team_color
        self._squares_in_use = starting_squares_list

        self._pieces = {
            "PAWN1"   : ["pawn", 0],
            "PAWN2"   : ["pawn", 0],
            "PAWN3"   : ["pawn", 0],
            "PAWN4"   : ["pawn", 0],
            "PAWN5"   : ["pawn", 0],
            "PAWN6"   : ["pawn", 0],
            "PAWN7"   : ["pawn", 0],
            "PAWN8"   : ["pawn", 0],
            "ROOK1"   : ["rook", 0],
            "ROOK2"   : ["rook", 0],
            "KNIGHT1" : ["knight", 0],
            "KNIGHT2" : ["knight", 0],
            "BISHOP1" : ["bishop", 0],
            "BISHOP2" : ["bishop", 0],
            "QUEEN"   : ["queen", 0],
            "KING"    : ["king", 0]
        }

        counter = 0
        for piece in self._pieces:
            self._pieces[piece].append(starting_squares_list[counter])
            counter += 1


    def identify_piece_by_location(self, square):
        """This method will receive a square coordinate (eg. 'a2') and will iterate through the _pieces dictionary until
        it finds a piece that is on that square. The method will return the name (which is a _pieces key) of that piece"""

        for piece in self._pieces:
            if self._pieces[piece][2] == square:
                return piece


    def get_piece_type(self, piece_name):
        """This method will return the piece type given the name of the piece. This information is stored as the first
        value list item in the _pieces dictionary"""

        return self._pieces[piece_name][0]


    def update_piece_location(self, source_square, destination_square):
        """Updates the location of a single piece in the _pieces dictionary. It takes in the source_square, which are
        the coordinates (eg. ‘a1’) of where the piece currently is. The other passed parameter is destination_square,
        which is where the user wants the piece to move. It will iterate through the _pieces dictionary until it finds
        a current location value that matches the value of source_square. This current location value is changed to
        that of destination_square. Additionally, update_squares_in_use is called to remove the source_square from
        the squares_in_use list, and add the destination_square to this list. That piece's number of moves is also
        increased by one, unless the piece is captured."""

        for piece in self._pieces:
            if source_square == self._pieces[piece][2]:
                moving_piece = piece

        self._pieces[moving_piece][2] = destination_square
        self.update_squares_in_use(source_square, destination_square)

        if destination_square != "CAPTURED":
            self._pieces[moving_piece][1] += 1


    def check_square_for_piece(self, this_square):
        """Takes in a specific square location (eg. ‘a7’). Returns True if that specific square has that team’s piece
        on it (is in _squares_in_use). Returns False if that space is not occupied by one of this team’s pieces."""

        for square in self._squares_in_use:
            if this_square == square:
                return True

        return False


    def update_squares_in_use(self, old_square, new_square):
        """Takes in the coordinate of square that a piece is already on, and the coordinate of a square that this
        piece will move to. Removes the old_square coordinate from _squares_in_use list, and adds the new_square
        coordinate to the squares_in_use list. If new_square is None, then this implies that the piece has been
        captured. In this case, remove the old_square value from the list, but do not add new_square to the list"""

        self._squares_in_use.remove(old_square)

        if new_square == "CAPTURED":
            return

        self._squares_in_use.append(new_square)


    def check_type_for_captured_pieces(self, piece_type):
        """This method will iterate through each of the piece types in the _pieces dictionary and checks each piece's
        location for CAPTURED. If all pieces of one type are captured, then this method will return True. If there still
        exists pieces on the board of every type, then this method will return False"""

        for piece in self._pieces:
            if piece_type == self._pieces[piece][0]:
                if "CAPTURED" != self._pieces[piece][2]:
                    return False

        return True


    def check_for_captured_pieces(self):
        """This method will call check_type_for_captured_pieces for each of the six chess piece types. If any of these
        calls returns True (meaning, all pieces of that type are captured), then immediately return True to indicate
        that all pieces of one type have been captured, and this team has been defeated. Return False if all calls
        return a False value, indicating that there exists pieces of all type that are still on the board"""

        if self.check_type_for_captured_pieces("pawn") == True:
            return True

        if self.check_type_for_captured_pieces("rook") == True:
            return True

        if self.check_type_for_captured_pieces("knight") == True:
            return True

        if self.check_type_for_captured_pieces("bishop") == True:
            return True

        if self.check_type_for_captured_pieces("queen") == True:
            return True

        if self.check_type_for_captured_pieces("king") == True:
            return True

        return False


    def check_pawn_move(self, piece_name, other_team, source_row, source_column, destination_square, destination_row,
                        destination_column):
        """This method will check whether the (source_row, source_column) to (destination_row, destination_column) move
        represents a valid move. First, use the team color to determine whether the move attempts to move backwards,
        which would be invalid (return False). Then, check that a piece of the opposite team exists on the destination
        square if the pawn attempts to move diagonally by 1. Return True if both of these conditions are met (valid pawn
        capture), or return False if not. Next, check for valid non-capture pawn moves If the pawn attempts to move
        2 spaces forward, it must be the first time that pawn has moved (check moves portion of the pieces dictionary
        to validate this). Or, the pawn can move just one space forward. Return True if either of these conditions are
        met. At this point, if the attempted move did not meet any of the above conditions, it is not a valid pawn move
        and False will be returned."""

        if self._team_color == "WHITE":
            if destination_column - source_column < 1:
                return False                        # attempted to move backwards or sideways - invalid move

        else:
            if source_column - destination_column < 1:
                return False                        # attempted to move backwards or sideways - invalid move

        # check that a piece from the other team is in the destination square if pawn attempts to move diagonally
        if abs(destination_row - source_row) == 1 and abs(destination_column - source_column) == 1:
            if other_team.check_square_for_piece(destination_square) == True:
                return True
            else:
                return False

        if other_team.check_square_for_piece(destination_square) == False and source_row == destination_row:
            # A pawn can only move two spaces forward if it is the first time that pawn has moved in the game
            if abs(destination_column - source_column) == 2 and self._pieces[piece_name][1] == 0:
                return True
            if abs(destination_column - source_column) == 1:
                return True

        return False



class ChessVar:
    """ ChessVar, in conjunction with ChessTeam, carries out the functions of a Chess (variant form) game. Its data
    members include _black_team and _white_team, which are both ChessTeam objects, _turn which tracks whoevers turn it
    is, and _game_state which stores the current state of the game. There are also two static data members dictionaries
    that contain row letters and their corresponding integer values. The __init__ method is the first place where
    ChessVar will need to communicate with ChessTeam in order to initialize the two ChessTeam object data members. The
    ChessVar class has get and set methods for the _turn and _game_state data members. There is a method to check whether
    a move resulted in a victory (uses ChessTeam methods to determine whether all pieces of a certain type are gone).
    The majority of these methods in this class are dedicated to determining whether a move (and possibly capture) are
    valid. Methods from ChessTeam are called on multiple occasions during the process of checking the validity of move
    in order to determine whether there are pieces on certain squares, and to extract information about pieces being
    moved or captured."""

    def __init__(self):
        """ All data members will be private. The _black_team data member will be a ChessTeam object and will need to
        pass a list of starting square positions of its 16 pieces. The _white_team data member will be a ChessTeam object
        and will likewise need to pass a list of its 16 starting squares. The _turn data member tracks whose turn it is.
        _turn will be initialized to “WHITE” since White always goes first in chess. The _game_state data member will
        track the status of the game. It will be initialized to “UNFINISHED” as the game just started. The letter_to_int
        and int_to_letters data members use dictionaries to track how each row letter pairs with an integer value, and
        will be used to translate the row letters into integer values and vice versa for the purpose of checking move
        validity"""

        black_starting_squares = ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "a8", "h8", "b8", "g8", "c8", "f8", "d8", "e8"]
        white_starting_squares = ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "a1", "h1", "b1", "g1", "c1", "f1", "d1", "e1"]
        self._black_team = ChessTeam("BLACK", black_starting_squares)
        self._white_team = ChessTeam("WHITE", white_starting_squares)
        self._turn = "WHITE"
        self._game_state = "UNFINISHED"

        self._letter_to_int = {
                                'a' : 1,
                                'b' : 2,
                                'c' : 3,
                                'd' : 4,
                                'e' : 5,
                                'f' : 6,
                                'g' : 7,
                                'h' : 8
                            }

        self._int_to_letter = {
                                1 : 'a',
                                2 : 'b',
                                3 : 'c',
                                4 : 'd',
                                5 : 'e',
                                6 : 'f',
                                7 : 'g',
                                8 : 'h'
                            }


    def set_turn(self):
        """Changes the value of the _turn private data member from WHITE to BLACK or from BLACK to WHITE depending on
        the current value of _turn"""

        if self._turn == "WHITE":
            self._turn = "BLACK"

        else:
            self._turn = "WHITE"


    def get_game_state(self):
        """Returns the value of the _game_state private data member, which can be UNFINISHED, WHITE_WON or BLACK_WON"""

        return self._game_state


    def set_game_state(self, new_state):
        """ Changes the value of the _game_state data member. Expected to only be called by the check_for_victory method,
         and only once per game. It must receive either BLACK_WON or WHITE_WON, which will be assigned as the new value
         for _game_state """

        self._game_state = new_state


    def generate_pawn_path(self, source_row, source_column, destination_column):
        """Given the (source_row, source_column) and (destination_row, destination_column) coordinates, this method will
        return a list of each square (eg. 'a2') that the pawn passes on its way to the destination square. This list does
        not include the source and destination squares"""

        pawn_path = []
        if source_column - destination_column == 2:     # A black pawn is moving two spaces on its first turn
            this_square = self._int_to_letter[source_row] + str(source_column-1)
            pawn_path.append(this_square)

        if source_column - destination_column == -2:    # A white pawn is moving two spaces on its first turn
            this_square = self._int_to_letter[source_row] + str(source_column+1)
            pawn_path.append(this_square)

        return pawn_path


    def check_rook_move(self, source_row, source_column, destination_row, destination_column):
        """This method will check whether the passed (source_row, source_column) and (destination_row, destination_column)
         coordinates represents a valid move for a rook. One (but not both) of these conditions must be true: either the
         two column values of source_square and destination_square must be equivalent, or the two row values. Returns True
         if it is a valid move, False otherwise."""

        if source_row == destination_row and source_column != destination_column:
            return True

        if source_row != destination_row and source_column == destination_column:
            return True

        return False


    def generate_rook_path(self, source_row, source_column, destination_row, destination_column):
        """Given the (source_row, source_column) and (destination_row, destination_column) coordinates, this method will
        return a list of each square (eg. 'a2') that the rook passes on its way to the destination square. This list does
        not include the source and destination squares"""

        rook_path = []
        if source_row == destination_row:
            this_row = self._int_to_letter[source_row]
            if source_column > destination_column:      # rook is moving backwards (from white side POV)
                this_column = source_column - 1
                while this_column > destination_column:
                    this_square = this_row + str(this_column)
                    rook_path.append(this_square)
                    this_column -= 1

            else:                                       # rook is moving forwards (from white side POV)
                this_column = source_column + 1
                while this_column < destination_column:
                    this_square = this_row + str(this_column)
                    rook_path.append(this_square)
                    this_column += 1
        else:
            this_column = str(source_column)
            if source_row > destination_row:            # rook is moving to the left (from white side POV)
                this_row = source_row - 1
                while this_row > destination_row:
                    this_square = self._int_to_letter[this_row] + this_column
                    rook_path.append(this_square)
                    this_row -= 1
            else:                                       # rook is moving to the right (from white side POV)
                this_row = source_row + 1
                while this_row < destination_row:
                    this_square = self._int_to_letter[this_row] + this_column
                    rook_path.append(this_square)
                    this_row += 1

        return rook_path


    def check_knight_move(self, source_row, source_column, destination_row, destination_column):
        """This method will check whether the passed (source_row, source_column) and (destination_row, destination_column)
        coordinates represent a valid move for a Knight. One of the following conditions must be met. If the source
        coordinate is (x,y), then the destination coordinate can only be (x +/- 1, y +/- 2) or (x +/- 2, y +/- 1) in
        order for the move to be valid. Return True if valid move, False otherwise."""

        if abs(source_row - destination_row) == 1 and abs(source_column - destination_column) == 2:
            return True

        if abs(source_row - destination_row) == 2 and abs(source_column - destination_column) == 1:
            return True

        return False


    def check_bishop_move(self, source_row, source_column, destination_row, destination_column):
        """This method will check whether the passed (source_row, source_column) and (destination_row, destination_column)
        coordinates represent a valid move for a Bishop. If the source coordinate is (x,y) and p is some integer, then
        the destination coordinate can only be (x +/- p, y +/- p) in order for the move to be valid. Return True if
        valid move, False otherwise."""

        if abs(source_row - destination_row) == abs(source_column - destination_column):
            return True

        return False


    def generate_bishop_path(self, source_row, source_column, destination_row, destination_column):
        """Given the (source_row, source_column) and (destination_row, destination_column) coordinates, this method will
        return a list of each square (eg. 'a2') that the bishop passes on its way to the destination square. This list does
        not include the source and destination squares"""

        bishop_path = []

        if source_row > destination_row and source_column > destination_column:     # moving backward, left (white POV)
            this_row = source_row - 1
            this_column = source_column - 1
            while this_row > destination_row:
                this_square = self._int_to_letter[this_row] + str(this_column)
                bishop_path.append(this_square)
                this_row -= 1
                this_column -= 1

        if source_row > destination_row and source_column < destination_column:     # moving backward, right (white POV)
            this_row = source_row - 1
            this_column = source_column + 1
            while this_row > destination_row:
                this_square = self._int_to_letter[this_row] + str(this_column)
                bishop_path.append(this_square)
                this_row -= 1
                this_column += 1

        if source_row < destination_row and source_column > destination_column:     # moving forward, left (white POV)
            this_row = source_row + 1
            this_column = source_column - 1
            while this_row < destination_row:
                this_square = self._int_to_letter[this_row] + str(this_column)
                bishop_path.append(this_square)
                this_row += 1
                this_column -= 1

        if source_row < destination_row and source_column < destination_column:     # moving forward, right (white POV)
            this_row = source_row + 1
            this_column = source_column + 1
            while this_row < destination_row:
                this_square = self._int_to_letter[this_row] + str(this_column)
                bishop_path.append(this_square)
                this_row += 1
                this_column += 1

        return bishop_path


    def check_queen_move(self, source_row, source_column, destination_row, destination_column):
        """This method will check whether the passed (source_row, source_column) and (destination_row, destination_column)
        coordinates represent a valid move for a Queen. This method will call check_rook_move and check_bishop_move. If
        one of these method calls returns True, then the move is valid (the queen can move like a rook or a bishop).
        Return true if valid move, False otherwise"""

        if self.check_rook_move(source_row, source_column, destination_row, destination_column) == True:
            return True

        if self.check_bishop_move(source_row, source_column, destination_row, destination_column) == True:
            return True

        return False


    def generate_queen_path(self, source_row, source_column, destination_row, destination_column):
        """Given the (source_row, source_column) and (destination_row, destination_column) coordinates, this method will
        return a list of each square (eg. 'a2') that the queen passes on its way to the destination square. This list does
        not include the source and destination squares"""

        queen_path = self.generate_bishop_path(source_row, source_column, destination_row, destination_column)
        if queen_path == []:
            queen_path = self.generate_rook_path(source_row, source_column, destination_row, destination_column)

        return queen_path


    def check_king_move(self, source_row, source_column, destination_row, destination_column):
        """This method will check whether the passed (source_row, source_column) and (destination_row, destination_column)
        coordinates represent a valid move for a King. If the source coordinate is (x,y), then the destination coordinate
        can only be (x +/- 1 , y) or (x , y +/- 1) or (x +/- 1, y +/- 1) for the move to be valid. Return True is the
        move is valid, False otherwise."""

        if abs(source_row - destination_row) == 1 and source_column == destination_column:
            return True

        if source_row == destination_row and abs(source_column - destination_column) == 1:
            return True

        if abs(source_row - destination_row) == 1 and abs(source_column - destination_column) == 1:
            return True

        return False


    def check_for_victory(self):
        """This method will call the ChessTeam check_for_captured_pieces method for whatever team is passed to this
         method. If this method is called, that means that one of the passed team's pieces has just been captured.
         If check_for_captured_pieces returns True, that means that all pieces of one type have been captured, and
         the other team has won. Call set_game_state to update the game state accordingly, and return True. A False
         return implies there still exists at least one piece of each type on the board for that team - return False"""

        if self._turn == "BLACK":
            if self._white_team.check_for_captured_pieces() == True:
                self.set_game_state("BLACK_WON")
                return True
            else:
                return False

        else:
            if self._black_team.check_for_captured_pieces() == True:
                self.set_game_state("WHITE_WON")
                return True
            else:
                return False


    def check_path_for_pieces(self, list_of_squares):
        """This method will be called by the is_valid_move method. It will receive a list of square (coordinates). Then,
        it will need to iterate through each square in the list and call check_square_for_pieces() each iteration for both
        teams. If check_square_for_pieces() ever returns True, then there exists some piece in the path of the move that
        is being attempted. Return True if any piece is detected, False otherwise"""

        for square in list_of_squares:
            if self._white_team.check_square_for_piece(square) == True:
                return True
            if self._black_team.check_square_for_piece(square) == True:
                return True

        return False


    def check_if_turn_team_piece_is_being_moved(self, source_square):
        """This method will be called by make_move to determine whether the attempted move is moving a piece of the
        team whose turn it is. Return True if a turn team's piece is on the source square, return False otherwise"""

        if self._turn == "WHITE":
            if self._white_team.check_square_for_piece(source_square) == True:
                return True

        if self._turn == "BLACK":
            if self._black_team.check_square_for_piece(source_square) == True:
                return True

        return False


    def check_piece_type_for_valid_move(self, piece_name, piece_type, source_row, source_column, destination_square,
                           destination_row, destination_column):
        """This method uses the passed piece_type information to call the correct method that will check whether the
        attempted move is valid based on that piece type. This method returns what is returned by that specifically
        called method. Will return True if the move is valid based on the piece type movement restrictions, return False
        if the move is not valid for that piece type"""

        if piece_type == "pawn":
            if self._turn == "WHITE":
                return self._white_team.check_pawn_move(piece_name, self._black_team, source_row, source_column,
                                                        destination_square, destination_row, destination_column)
            else:
                return self._black_team.check_pawn_move(piece_name, self._white_team, source_row, source_column,
                                                         destination_square, destination_row, destination_column)

        if piece_type == "rook":
            return self.check_rook_move(source_row, source_column, destination_row, destination_column)

        if piece_type == "knight":
            return self.check_knight_move(source_row, source_column, destination_row, destination_column)

        if piece_type == "bishop":
            return self.check_bishop_move(source_row, source_column, destination_row, destination_column)

        if piece_type == "queen":
            return self.check_queen_move(source_row, source_column, destination_row, destination_column)

        else:
            return self.check_king_move(source_row, source_column, destination_row, destination_column)


    def generate_piece_path(self, piece_type, source_row, source_column, destination_row, destination_column):
        """This method will call the appropriate piece type-specific path generator. Will only be used by is_valid_move
        to check generate the path of a pawn, rook, bishop, or queen that can be used to validate that there are no pieces
        along this path that would result in an invalid move"""

        if piece_type == "rook":
            piece_path = self.generate_rook_path(source_row, source_column, destination_row, destination_column)
        elif piece_type == "bishop":
            piece_path = self.generate_bishop_path(source_row, source_column, destination_row, destination_column)
        elif piece_type == "queen":
            piece_path = self.generate_queen_path(source_row, source_column, destination_row, destination_column)
        else:
            piece_path = self.generate_pawn_path(source_row, source_column, destination_column)

        return piece_path


    def check_path_for_pieces(self, piece_path):
        """This method will receive a list whose elements are the square coordinates (eg. 'a2') that a piece passes through
        on its way to the destination square. This method will iterate through each square in the list and check whether
        pieces from either the black or white team exist in these squares. If a piece is ever on one of these squares,
        then return True (a piece is in the path, not a valid move). Otherwise, return False (path is clear of pieces)"""

        for square in piece_path:
            if self._white_team.check_square_for_piece(square) == True:
                return True
            if self._black_team.check_square_for_piece(square) == True:
                return True

        return False


    def process_capture(self, destination_square):
        """If a valid capture has occurred, then this method will update the location of the captured piece to reflect that
        it has been captured, then will call the check_for_victory method to determine whether this capture has resulted
        in a victory"""

        if self._turn == "WHITE":
            self._black_team.update_piece_location(destination_square, "CAPTURED")

        else:
            self._white_team.update_piece_location(destination_square, "CAPTURED")

        self.check_for_victory()


    def check_for_valid_capture(self, destination_square):
        """This method will be called by is_valid_move to determine whether a capture is valid. If a piece attempts to
        capture one of its own pieces, then the capture is not valid and the entire move is not valid. If the piece is
        moving to an empty square, return True to indicate there are no issues with an invalid capture. If the piece is
        capturing a piece from the other team (valid capture), then call process_capture to update the location of the
        captured piece and check whether this capture resulted in a victory"""

        if self._turn == "WHITE":
            if self._white_team.check_square_for_piece(destination_square) == True:     # attempting to capture own piece
                return False
            if self._black_team.check_square_for_piece(destination_square) == False:    # piece is moving to an empty space
                return True
            else:
                self.process_capture(destination_square)
                return True

        else:
            if self._black_team.check_square_for_piece(destination_square) == True:     # attempting to capture own piece
                return False
            if self._white_team.check_square_for_piece(destination_square) == False:    # piece is moving to an empty space
                return True
            else:
                self.process_capture(destination_square)
                return True


    def is_valid_move(self, piece_name, piece_type, source_square, source_row, source_column, destination_square,
                           destination_row, destination_column):
        """This method will be called by make_move to determine whether the move is valid based on various restrictions.
        First, is_valid_move calls the specific method that will determine whether the movement matches how that specific
        piece type can move. Next, is_valid_move validates that a pawn, rook, bishop, or queen does not attempt to move
        through other pieces. Finally, is_valid_move calls the is_valid_capture method to verify that the piece does not
        attempt to capture itself. If any of these tests fail, then is_valid_move will immediately return False, indicating
        and invalid move. If all the tests pass, then update the location of the piece that has moved, change the turn,
        and return True"""

        if self.check_piece_type_for_valid_move(piece_name, piece_type, source_row, source_column, destination_square,
                           destination_row, destination_column) == False:
            return False

        # if the piece is a pawn, rook, bishop, or queen, it is necessary to check if these pieces attempt to move
        # through existing pieces on their way to the destination square
        if piece_type != "king" and piece_type != "knight":
            piece_path = self.generate_piece_path(piece_type, source_row, source_column, destination_row, destination_column)
            if piece_path != []:
                # If check_path_for_pieces returns True, this means there exists a piece along the path, not valid
                if self.check_path_for_pieces(piece_path) == True:
                    return False

        # Call is_valid_capture to verify that a piece does not attempt to capture itself. is_valid_capture will also
        # modify the locations of a captured piece and check for a victory in the case that a piece is captured
        if self.check_for_valid_capture(destination_square) == False:
            return False

        # all the tests have passed. This was a valid move. Now, call the update_piece_location method to update the
        # location of the moving piece. Then call set_turn to switch the turn to the other team.
        if self._turn == "WHITE":
            self._white_team.update_piece_location(source_square, destination_square)
        else:
            self._black_team.update_piece_location(source_square, destination_square)

        self.set_turn()
        return True


    def make_move(self, source_square, destination_square):
        """This method will receive coordinates (eg. 'a2') for the source square and the destination square, in that
        order. First, make_move will confirm that the move starts with square that contains a piece from the team whose
        turn it is. If this test passes, then the method will extract the integer values for the source row, source column
        destination row, and destination column. Then, the method will call is_valid_move, which does all the heavy lifting
        for determining whether a move is valid based on the type of piece being moved. is_valid_move also updates the
        moving (and captured) piece location, checks for victory, and changes the turn if a move is valid. make_move will
        return True is the move (and capture, if applicable) is indeed valid, False is not valid"""

        # return False if the game is over, and someone has already won
        if self._game_state != "UNFINISHED":
            return False

        # not a valid move if the turn does not start with moving a piece from the team whose turn it is
        if self.check_if_turn_team_piece_is_being_moved(source_square) == False:
            return False

        # extract the piece name and type of the piece that is moving
        if self._turn == "WHITE":
            piece_name = self._white_team.identify_piece_by_location(source_square)
            piece_type = self._white_team.get_piece_type(piece_name)
        else:
            piece_name = self._black_team.identify_piece_by_location(source_square)
            piece_type = self._black_team.get_piece_type(piece_name)

        # Assign specific integer values for the source row and column, and for the destination row and column
        source_row = self._letter_to_int[source_square[0]]
        source_column = int(source_square[1])
        destination_row = self._letter_to_int[destination_square[0]]
        destination_column = int(destination_square[1])

        return(self.is_valid_move(piece_name, piece_type, source_square, source_row, source_column, destination_square,
                           destination_row, destination_column))