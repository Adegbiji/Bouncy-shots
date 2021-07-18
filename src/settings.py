import json

def update_difficulty(difficulty):
	data = {
		"difficulty":difficulty
	}
	with open(r'other\game_data.json', 'w') as file:
		json.dump(data, file)

def success_message():
	print("Changes saved.")

def main():
	print("Enter your prefered game difficulty.")

	option = input("(E)asy, (M)edium or (H)ard mode: ")

	if option.upper() == "E":
		update_difficulty("easy")
		success_message()
	elif option.upper() == "M":
		update_difficulty("medium")
		success_message()
	elif option.upper() == "H":
		update_difficulty("hard")
		success_message()
	else:
		print("Invalid input.")

if __name__ == '__main__':
	main()