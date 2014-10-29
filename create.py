def read_text (level):
	screen = open('level' + level + '.txt')
	characters = []
	lines = []
	count = 0
	for line in screen:
		for ch in line:
			if count < 35:
				characters.append(ch)
				count += 1
			elif ch == '\n':
				count = 0
				characters = []
				pass
		lines.append(characters)
	return lines

def main ():
	level = raw_input('Welcome to Chelsea Run!\nWhat level? ')
	a = read_text(level)
	print a

if __name__ == '__main__':
	main()