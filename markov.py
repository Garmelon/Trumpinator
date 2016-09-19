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
			before = random.choice(list(self.matrix))
		
		selection = self.matrix[before]
		choice = random.randrange(sum(selection.values()))
		
		counter = 0
		for char, amount in selection.items():
			counter += amount
			if choice < counter:
				return char
	
	def regurgitate_line(self, line=""):
		while True:
			before = line[-self.before:]
			char = self.hiccup(before)
			
			if char == "":
				line += "\n"
				return line
			else:
				line += char
	
	# set start if you want to have the lines start with a particular word/string
	def regurgitate(self, lines=1, start=""):
		speech = ""
		
		for i in range(lines):
			speech += self.regurgitate_line(line=start)
		
		return speech
	
	def save(self, filename):
		with open(filename, "w") as f:
			json.dump(self.matrix, f)
	
	def load(self, filename):
		with open(filename) as f:
			self.matrix = json.load(f)

def main(filename, paragraphs=1, char_lookback=10, start=""):
	markov = Markov(char_lookback)
	markov.feed(filename)
	
	# print matrix stats for debugging purposes
	print("Entries:", len(markov.matrix))
	
	print("Regurgitating!")
	print(markov.regurgitate(paragraphs, start))

if __name__ == "__main__":
	try:
		paragraphs = int(sys.argv[1])
	except (IndexError, ValueError):
		paragraphs = 1
	
	try:
		char_lookback = int(sys.argv[2])
	except (IndexError, ValueError):
		char_lookback = 10
	
	try:
		start = sys.argv[3]
	except IndexError:
		start = ""
	
	main("trump_speech.txt", paragraphs, char_lookback, start)
