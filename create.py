def read_text (level):
	screen = open('level' + level + '.txt')
	vals = []
	count = 0
	for line in screen:
		lns = []
		for ch in line:
			if count < 34:
				lns.append(ch)
				count += 1
			elif ch == '\n':
				pass
			else:
				vals.append(lns)
				lns = []
		print lns
	print vals

def main ():
	level = raw_input('Welcome to Chelsea Run!\nWhat level? ')
	a = read_text(level)

if __name__ == '__main__':
	main()