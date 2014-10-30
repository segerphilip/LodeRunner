def read_text (level):
	screen = open('level' + level + '.txt')
	characters = []
	lines = []
	count = 0
	for line in screen:
		for ch in line:
			if ch == '\n':
				lines.append(characters)
				characters = []
			else:
				characters.append(ch)
	return lines

def main ():
	level = raw_input('Welcome to Chelsea Run!\nWhat level? ')
	a = read_text(level)
	print a

if __name__ == '__main__':
	main()