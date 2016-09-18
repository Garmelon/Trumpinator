import sys
import random

class Markov:
	def __init__(self, before=1):
		self.before = before
		self.matrix = {}
	
	def feed(self, filename):
		with open(filename) as f:
			for line in f:
				self.devour(line[:-1])
	
	def devour(self, line):
		before = ""
		
		for char in line:
			if before not in self.matrix: self.matrix[before] = {}
			if char not in self.matrix[before]: self.matrix[before][char] = 0
			self.matrix[before][char] += 1
			before = (before + char)[-self.before:]
		
		if before not in self.matrix: self.matrix[before] = {}
		if "" not in self.matrix[before]: self.matrix[before][""] = 0
		self.matrix[before][""] += 1
	
	def hiccup(self, before):
		if before not in self.matrix:
			before = random.choice(self.matrix.keys())
		
		selection = self.matrix[before]
		choice = random.randrange(sum(selection.values()))
		
		counter = 0
		for char, amount in selection.items():
			counter += amount
			if choice < counter:
				return char
	
	def regurgitate_line(self):
		line = ""
		
		while True:
			before = line[-self.before:]
			char = self.hiccup(before)
			
			if char == "":
				line += "\n"
				return line
			else:
				line += char
	
	def regurgitate(self, lines=1):
		speech = ""
		
		for i in range(lines):
			speech += self.regurgitate_line()
		
		return speech

def main(filename, paragraphs, char_lookback):
	markov = Markov(char_lookback)
	markov.feed(filename)
	
	# print matrix stats for debugging purposes
	print("Entries:", len(markov.matrix))
	
	print("Regurgitating!")
	print(markov.regurgitate(paragraphs))

if __name__ == "__main__":
	try:
		paragraphs = int(sys.argv[1])
	except (IndexError, ValueError):
		paragraphs = 1
	
	try:
		char_lookback = int(sys.argv[2])
	except (IndexError, ValueError):
		char_lookback = 10
	
	main("trump_speech.txt", paragraphs, char_lookback)
