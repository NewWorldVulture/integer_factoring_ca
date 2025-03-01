from PIL import Image, ImageDraw

from CellularAutomata import CellularAutomata



class CursedImage():
	def __init__(self, ca_width=200, tm_width=35, scale=1, generations=100):
		# Side length for each cell (10 -> each cell will be 10 pixels wide)
		self.scale = scale
		self.generations = generations

		self.tm_width = scale * tm_width
		self.ca_width = scale * ca_width
		# Setting parameters for image
		# Pixel buffer on left side, inbetween, and on right side of image
		self.buffer = 3 * scale
		self.image_width = scale * (ca_width + tm_width) + (2 * self.buffer)
		if ca_width and tm_width:
			self.image_width += self.buffer
		self.height = (self.scale * self.generations) + (3 * self.buffer)
		# x-value 
		self.ca_start = self.buffer + self.buffer * (tm_width == True)

		# Create Actual Image as CursedImage.im
		self.im = Image.new("RGB", (self.image_width, self.height), "#000000")

	# Pass the entire Turing Machine
	def create_image(self, tm=None, ca=None):
		image = ImageDraw.Draw(self.im)
		flag = 0

		for gen in range(self.generations):
			if tm:
				# Draw Turing Machine State
				for index, cell in enumerate(tm.tape):
					x = self.buffer + self.scale * index
					y = self.buffer + self.scale * gen
					image.rectangle([x, y, x+self.scale, y+self.scale],
						fill = tm.colors[cell])
				#print(ca.curr_row)
			if ca:
				# Draw Cellular Automata
				for index, cell in enumerate(ca.curr_row):
					x = self.ca_start + self.scale * index
					y = self.buffer + self.scale * gen
					image.rectangle([x, y, x+self.scale, y+self.scale],
						fill = ca.colors[cell])

			# Advance Generations
			#tm.advance_generation()
			# Use the new tape values as the values for the Cellular Automata
			#print(ca.curr_row)
			p_row = ca.curr_row

			ca.advance_generation(regex_list=regexes)
			if (p_row == ca.curr_row) and (flag == 0):
				print(gen)
				flag = 1
				#break
			#ca.advance_generation()
		#print(''.join(ca.curr_row))


def main():
	# Create Cellular Automata
	ca = CellularAutomata(rule_number=None, neighborhood=3,
		colors=color_list, random_first_row=False, width=len(input_string),
		first_row=input_string
	)

	image = CursedImage(tm_width=0, scale=10, generations=475, ca_width=ca.width)
	image.create_image(ca=ca)
	#print(ca.curr_row)
	#print(len(color_list))
	image.im.show()

#input_string = "BF0110BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"

input_string = "F011BBBBBBBBBBBBBBBBBB" # F3 (169)
input_string = "F0110BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" # F6 (475)
#input_string = "F1011BBBBBBBBBBBBBBBBBBBBBBBBB" # F11 (929)
#input_string = "F1100BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" # F12 (1078)

states=[
 # BASICS
	# B => Blank Cell
	# 0 => Zero Cell
	# 1 => One Cell
	# F => Trigger Factor out / Copy integer right ('F' -> 'B') (See Command Carriers)

 # Command Carriers
	# @ => '0' Carrying 'F' command to left edge
	# ! => '1' Carrying 'F' command to left edge

 # Integer carry symbols (Far Left)
	# G => '0' Trigger carry left ('G' -> 'm' -> '0')
	# H => '1' Trigger carry left ('1' -> 'n' -> '1')
	# m => '0' decaying to base ('m' -> '0')
	# n => '1' decaying to base ('n' -> '1')

	# 6 => '0' carrying '0' right, loading from left
	# 7 => '0' carrying '1' right, loading from left
	# 8 => '1' carrying '0' right, loading from left
	# 9 => '1' carrying '1' right, loading from left

 # Integer carry symbols (Left)
	# No need for [1] in [e0] because there will be no /1/s after a check
	# i => '0' copying, overriding [e0] (i -> ⚢/⚤ -> 0)
	# j => '1' copying, overriding [e0] (j -> ⚧/⚣ -> 1)
	# ⚢ => '0' copying, carrying '0', overriding [e0]
	# ⚤ => '0' copying, carrying '1', overriding [e0]
	# ⚣ => '1' copying, carrying '0', overriding [e0]
	# ⚧ => '1' copying, carrying '1', overriding [e0]

 # Subtraction 0/1 set (Left)
	# a => '0' after subtraction ('0'-'0', '1'-'1')
	# b => '1' after subtraction ('1'-'0')
	# w => '0' carry '0' left, non-final ('w' -> 'a')
	# x => '0' carry '1' left, non-final ('x' -> 'C' ->...)
	# y => '1' carry '0' left, non-final ('y' -> 'b')
	# z => '1' carry '1' left, non-final ('z' -> 'a')

	# Borrow Handling
		# C => -1 after subtraction, Borrow Request ('C' -> 'b' -> '1')
		# ɔ => "continue carry". (Leeches off of Initial Carry 'C'. 'ɔ' -> 'd' -> 'b' -> '1')
		# d => decays 'C' ('C' -> 'd' -> ...)
		# c => Acknowledge C on the right ('b' -> 'c' -> 'a' -> '0')
		# e => Attempted borrow on '_' (First Separator set)

 # Subtraction 0/1 set (Right)
	# 2 => '0', carry '0', left
	# 3 => '0', carry '1', left
	# 4 => '1', carry '1', left
	# 5 => '1', carry '1', left

	# e => triggered when trying to borrow from _ (See first Separator set)
	# g => '0', trigger carry left, loading from left (2, 3, 4, 5)
	# h => '1', trigger carry left, loading from left (2, 3, 4, 5)

 # Difference Checking Set (Left)
	# o => '0' checked, only '0' checked so far ('o' => '0')
	# l => '1' checked. Trigger future 'l' and 'ø' ('l' => '1')
	# ø => '0' checked, '1' has been checked previously ('ø' -> '0')

 # First Separator Set
	# _ => Default
	# # => Subtracting to lower than 0. Error out, Trigger new Copy of Integer (See Basics)
	# ~ => Subtraction in progress. When [01] detected on right, '~' -> '=' -> '_'
	# = => Triggers check for if total is equal to zero. See Difference Check Set
	# ☉ => Separator Carrying '0' to the right for copying
	# ☽ => Separator Carrying '1' to the right for copying
	# ☆ => Separator switching from [☉☽] to '_'

 # Subtraction Symbol Set
	# S => Trigger subtraction operations
	# s => Subtraction marker, no triggers
	# p => Sub sign, carry '0' left (from 2, 3, 4, 5)
	# q => Sub sign, carry '1' left (""")
	# E => Error, triggered by 'e' in Subtraction Left Side set
	# ∃ => Error, waiting for copy to finish
	# K => Copy (Kopy) subtractor over to storage

 # Boundary Symbol Set
	# : => Default Set. Listens for
	# < => Increment, then trigger Subtraction ('<' -> ':')
	# ≤ => Post-Increment Subtraction symbol carrier
	# 🜄 => Boundary Carry '0' to the right for storage. Waits for end, then ('🜄' -> '<' to inc.)
	# 🜂 => Boundary Carry '1' to the right for storage. Waits for end, then ('🜂' -> '<' to inc.)

 # Incrementing binary number Set
	# ♀ => '0', carry increment command right ('♀' -> '0')
	# ♂ => '1', carry increment command right ('♂' -> '1')
	# 🜁 => '1', Incrementing. Triggers '1' -> '0' on the left ('🜁' -> '🜃' -> '0')
	# 🜃 => '1', Incrementing, decaying. Triggered by '🜃' or '0' on the left ('🜃' -> '0')

 # /END
]

regexes = {
	##### { Subtraction Symbols #########
	# Right side carries LEFT
	r"[Sgh]0.": 'g',	# '0', trigger carry left, fill from left
	r"[Sgh]1.": 'h',	# '1', trigger carry left, fill from left

	r".0[g24]": '2',	# '0', carry '0', left
	r".0[h35]": '3',	# '0', carry '1', left
	r".1[g24]": '4',	# '1', carry '0', left
	r".1[h35]": '5',	# '1', carry '1', left

	r".[g23].": '0',	# Degrade back to '0'
	r".[h45].": '1',	# Degrade back to '1'

	# Right side Increment Command
	r"[E♀♂]0.": '♀',	 # '0', carry increment command right ('♀' -> '0')
	r"[E♀♂]1.": '♂',	 # '1', carry increment command right ('♂' -> '1')
	r".♀.": '0',	   # Decay back to '0'
	r".♂.": '1',	   # Decay back to '1'

	# Subtraction symbol
	r".[Ss][g24]": 'p', # sub sign, carry '0'
	r".[Ss][h35]": 'q', # sub sign, carry '1'
	r".[pqS].": 's',	# sub sign, no triggers
	r"e[sS].": 'E',		# sub sign, no copy, just increment
	r".E.": '∃',			# Wait for further instruction

	r"[01]∃.": 'R',	 # Errored out, trigger another subtraction
	r"os.": 'D',		# Trigger copy integer to the right/left ('D' -> 'Ɑ')
	r".D.": 'Ɑ',		# Wait for both sides to finish
	r".[Ɑ∃][@!]": 'R',	 # Subtraction signal from the right
	r"[mnij][Ɑ∃].": 'R',  # "Finished Copying" signal from the left

	r".[R][@!]": 'S',	 # Subtraction signal from the right
	r"[mnij][R].": 'S',  # "Finished Copying" signal from the left
	r"[mnij][Ɑ∃][@!]": 'S',# Both finished at same time
	r"[øl]s.": 'S',	 # Total greater than zero, Subtract again

	# Left side/Completion
	r".[0øi][pwy]": 'w',	# 0 carry 0, non-final
	r".[0øi][qxz]": 'x',	# 0 carry 1, non-final
	r".[1lj][pwy]": 'y',	# 1 carry 0, non-final
	r".[1lj][qxz]": 'z',	# 1 carry 1, non-final
	r".[wx].": '0',	 # Degrade back to 0
	r".[yz].": '1',	 # Degrade back to 1

	# Non-carrying finalizations
	r"[Cab_]w.": 'a',   # 0 sub 0, finalize a -> 0
	r"[Cab_]x.": 'C',   # 0 sub 1, request carry (See carry cases)
	r"Cx.": 'C',		# Continue Carry request
	r"[Cab_]y.": 'b',   # 1 sub 0, finalize b -> 1
	r"[Cab_]z.": 'a',   # 1 sub 1, finalize a -> 0

	# Subtraction borrow cases
	r".a[Cɔ]": 'ɔ',	# 0 gets Carry request, Carry request
	r".b[Cɔ]": 'a', # 1 gets Carry request, ACK, decay c -> a -> 0
	r"[bd]ɔ.": 'd',
	r"[bd]C.": 'b',
	r".d.": 'b',	# Degrade c back to a -> 0
	r"[_~][Cɔ].": 'e',		 # Error Out

	# Subtraction Product Check
	r"[=o]0.": 'o',	 # 0, All Digits so far are zero, decays to 0
	r"[=løo]1.": 'l',   # 1, during total check, decays to 1
	r"[lø]0.": 'ø',	 # 0, total not zero, decays to 0
	r".[øo].": '0',	 # Decay back to 0
	r".l.": '1',		# Decay back to 1

	# First separator (Boundary Set)
	r"[68]B.": '☉',	  # Setup for First calculations
	r"[79]B.": '☽',	  # """
	r".[_=~][Cɔ]": '#',	 # _ receive Carry request, error out, start copy left
	r".[_=~][!@]": 'K', # Receive Copy('Kopy') Request
	r"._[ab]": '~',	 # Intermediate phase about to trigger
	r".~[01]": '=',	 # Check final 
	r".=.": '_',		# Trigger checks, move along
	r".[☽☉].": '☆',	# Decay back to default 0/1 without any other input
	r".☆.": '_',	   # Trigger Normalization, Switch to default '_'
	r"[68G][K#~=_☽☉].": '☉',  # Boundary carrying copy '0' right
	r"[79H][K#~=_☽☉].": '☽',  # Boundary carrying copy '1' right

	# Integer Copy Copiers
	r"[☉🜄◣⚢⚧][Bбeøol0].": 'i', # '0' copying, overriding
	r"[☽🜂◢⚤⚣][Bбeøol0].": 'j', # '1' copying, overriding
	r"[☉🜄◣⚢⚧][i⚢⚤].": '⚢', # 0c0
	r"[☽🜂◢⚤⚣][i⚢⚤].": '⚤', # 0c1
	r"[☉🜄◣⚢⚧][j⚧⚣].": '⚧', # 1c0
	r"[☽🜂◢⚤⚣][j⚧⚣].": '⚣', # 1c1
	r"[<☆01,][i⚢⚤].": '0',	# Decay to '0'
	r"[<☆01,][j⚧⚣].": '1',	# Decay to '1'

	# Zero Fill States
	r"[ij][Be].": 'б',  # Future Subtraction symbol, when finalized
	r".0[б⚳⚴]": '⚳',	   # '0', Carry "fill" signal left
	r".1[б⚳⚴]": '⚴',	   # '1', Carry "fill" signal left
	r"_⚳.": '☊',	  # '0', Trigger 0-Fill carry right
	r"_⚴.": '☋',	  # '1', Trigger 0-Fill carry right
	r".☊.": '0',	   # Below is all the same as carrying an actual int, but just counting.
	r".☋.": '1',
	r"[01]⊗.": '☊',	  # '0', Trigger Fill
	r"[01]⚸.": '☋',	   # '1', Trigger Fill
	r"[☊☋⚸⊗][⚳].": '⊗',  # Carry Right
	r"[☊☋⚸⊗][⚴].": '⚸',  # Carry right

	r"[☋⚸☊⊗][б₿].": '₿',  # Carry Fill-0 over subtraction symbol
	r"[01]₿.": 'ƨ',		 # Decay to 'S' when no more carries are coming
	r".ƨ[!@]": 'S',		   # Decay to 'S'
	r"[₿♁]B.": '⊗',	 # Fill in another '0' (⊗ -> 0)
	r"[₿♁]⊗.": '♁',		# Carry fill '0' over
	r"[0ƨ]♁.": '0',		 # Decay to '0'
	r"☊B.": '<',	   # Trigger immediate incrementation

	### STORAGE #################
	r".[◒◓].": '0',
	r".[◐◑].": '1',
	r"[🜄∩◣◐◒][0⚳◒◓].": '◒', # 0c0
	r"[🜂∪◢◑◓][0⚳◒◓].": '◓', # 0c1
	r"[🜄∩◣◐◒][1⚴◐◑].": '◐', # 1c0
	r"[🜂∪◢◑◓][1⚴◐◑].": '◑', # 1c1

	r"[Z◖◗◘]0.": '◖',
	r"[Z◖◗◘]1.": '◗',
	r"[Z◖◗◘],.": '◘',
	r"[Z◖◗◘]б.": 'B',
	r".◖.": '0',
	r".◗.": '1',
	r".[◖◗]б": 'B',
	r".◘.": 'B',	# '◘'

	r".[◣◢].": ',',
	r"[◐◒][б◣◢,].": '◣',	# Comma, carrying '0'
	r"[◑◓][б◣◢,].": '◢',	# Comma, carrying '1'
	### STORAGE #################


	# Accepted Subtractor - Copy Carriers
	r"[68G][:<🜄🜂].": '🜄',  # Second Boundary carrying '0' over
	r"[79H][:<🜄🜂].": '🜂',  # Second Boundary carrying '1' over
	r"[mn][🜂🜄].": '<',   # Trigger incremenetation


	# Integer Copy Triggers
	r".[1][>≤#!@FDK]": '!',   # 1 Copy command move left (triggers phase 1 copy)
	r".[0][>≤#!@FDK]": '@',   # 0 Copy command move left (triggers phase 1 copy)
	r"🜃[:].": '≤',		# Trigger Subtraction from right
	r".≤.": ':',		# Decay to '⊂'. Listen for subtraction triggers
	r".B[!@]": 'F',	 # Trigger copy phase over
	r"[^B]!.": '1',		# Decay carry command to '1'
	r"[^B]@.": '0',		# Decay carry command to '0'

	# Error Cases
	r"e[Cɔab01wxyz].": 'e',  # """

	# Subtraction Finalization
	r"[^e]a[01s]": '0',	# Finalize a -> 0
	r"[^e]b[01s]": '1',	# Finalize b -> 1
	##### } #############################

	##### COPY STATES ###################
	r"B0[@!]": 'G',	 #
	r"B1[@!]": 'H',	 # 
	r".F.": 'B',		# Decay (F -> B)
	r"[DFmn][067@].": 'G',	# '0', trigger right carry, from left
	r"[DFmn][189!].": 'H',	# '1', trigger right carry, from left
	r".G.": 'm',		# Decay from [67] -> m -> 0
	r".H.": 'n',		# Decay from [89] -> n -> 1

	r"[G68][670@].": '6',	# '0', carry '0', right
	r"[79H][670@].": '7',	# '0', carry '1', right
	r"[G68][891!].": '8',	# '1', carry '0', right
	r"[H79][891!].": '9',	# '1', carry '1', right

	r"[B01][67].": 'm',  # Decay from 0c -> m -> 0
	r"[B01][89].": 'n',  # Decay from 1c -> m -> 1
	r".m.": '0',
	r".n.": '1',
	##### ###############################

	# FINISHERS #
	r"[G68][⊆∩∪].": '∩',	# '0' FINISHER carry
	r"[H79][⊆∩∪].": '∪',	# '1' FINISHER carry
	r"[01][∪∩]": 'Y',   # Final Finisher
	r".Y.": 'Z',
	r".[^B]Z": 'Z',	 # Clear the Board (LEFT)
	r".Z.": 'B',		# Clear the Board (LEFT)
	# FINISHERS FINISH #

	##### INCREMENTATION ################
	# Adds 1 to the subtractor
	r"[♀♂]:.": '<',	 # Received trigger, increment subtractor by 1
	r".<.": '>',		# Wait for finished incrementation
	r"[01][>].": '⊂',	# Decay from [<>] -> :
	r"[gh]⊂.": '⊆',	 # Trigger subtraction occurs once (See Finishers)
	r"[gh]⊆.": ':',	 # Trigger Twice
	r".0[<🜁]": '1',	 # Increment a 0 to a 1
	r".1[<🜁]": '🜁',	# Increment a 1 -> 🜁 -> 🜃 -> 0
	r"[0🜃]🜁.": '🜃',	# Decay from 🜁 -> 🜃 (🜃 -> 0)
	r".🜃.": '0',		# Decay from 🜃 -> 0
}

color_list = {
	'∩': (255, 28, 90),
	'∪': (110, 30, 255),
	'Y': (143, 229, 255),
	'Z': (100, 65, 50),

	'◒': (190, 128, 90),
	'◓': (200, 240, 85),
	'◐': (195, 90, 10),
	'◑': (140, 190, 10),

	',': (56, 56, 56),
	'◣': (100, 40, 40),
	'◢': (40, 40, 100),

		# 0's Reds
		# 1's Blues
	'B': (0,0,0), 
	'0': (255, 255, 255),
	'1': (150, 150, 150),
	'2': (255, 200, 100),
	'3': (100, 255, 255),
	'4': (255, 153, 50),
	'5': (0, 153, 255),
	'6': (235, 66, 71),
	'7': (90, 170, 255),
	'8': (138, 43, 46),
	'9': (43, 89, 138),

	'б': (110, 0, 110),
	'⚳': (120, 45, 80),
	'⚴': (45, 45, 77),

	'◖': (194, 90, 196),
	'◗': (90, 111, 196),
	'◘': (60, 80, 90),

	'☉': (100, 30, 30),
	'☽': (40, 30, 100),
	'☆': (180, 230, 220),
	'i': (100, 60, 60),
	'j': (70, 70, 100),
	'⚢': (255, 100, 0),
	'⚣': (40, 100, 170),
	'⚤': (255, 140, 0),
	'⚧': (50, 40, 175),

	'♀': (230, 180, 160),
	'♂': (140, 100, 200),
	'☊': (255, 90, 200),
	'☋': (117, 90, 255),
	'⊗': (205, 0, 103),
	'⚸': (105, 70, 253),
	'ƨ': (170, 30, 180),

	'g': (255, 32, 0), 
	'h': (0, 32, 255), 
	'G': (110, 150, 80), 
	'H': (80, 150, 125), 
	'm': (92, 0, 0),
	'n': (0, 45, 100),

	# Message carriers
	'!': (100, 75, 222),
	'@': (230, 125, 230),
	# 
	'🜃': (222, 100, 100),
	'🜁': (145, 70, 70),
	'☊': (250, 170, 170),
	'☋': (170, 170, 250),

	'⊂': (68, 117, 115),
	'⊆': (0, 202, 156),

	# Subtracting side
	'a': (255, 90, 20),
	'b': (0, 0, 153),
	'w': (255, 255, 150),
	'x': (100, 150, 255),
	'y': (255, 153, 50), 
	'z': (50, 100, 255), 

	# Carries
	'c': (100, 150, 255),
	'C': (255, 0, 255), 
	'ɔ': (255, 100, 255),
	'd': (150, 0, 200), 
	'e': (100, 0, 100), 

	# Subtraction symbol
	'S': (255, 255, 0), 
	's': (108, 75, 122),
	'p': (200, 60, 100),
	'q': (60, 85, 150), 
	'E': (44, 74, 0),   
	'∃': (90, 133, 70),
	'D': (210, 40, 210),
	'Ɑ': (230, 110, 230),
	'K': (30, 60, 50),
	'R': (80, 10, 55),
	'♁': (220, 230, 60),

	'₿': (100, 0, 0),

	# Separator/wall
	'F': (135, 255, 135),
	'_': (0, 255, 0),
	'~': (80, 130, 90),
	'=': (0, 170, 20), 
	'#': (0, 10, 20),
	'o': (230, 230, 0),
	'l': (40, 80, 0),
	'ø': (120, 140, 0),

	# Second separator set (Boundary Set)
	':': (0, 255, 255),
	'<': (0, 150, 255),
	'≤': (160, 210, 255),
	'>': (255, 255, 100),
	'🜄': (150, 110, 90),
	'🜂': (90, 120, 145),
}


main()