import random

names = ['Jannes', 'Abdalla', 'Christian', 'Lea', 'Esther', 'Charlotte', 'Sébastien', 'Stephanie']

def shuffleNames(names):
    # Create a List to store each newly generated list
    shuffled_names_lists = []
    # Shuffle the list four times
    for i in range(4):
        # Create a copy of the original list
        shuffled_names = names.copy()
        # Shuffle the copy
        random.shuffle(shuffled_names)
        # Check that no name appears twice at the same index
        if i == 0:
            # Append the shuffled list to the list of shuffled lists
            shuffled_names_lists.append(shuffled_names)
        elif i == 1:
            while any(shuffled_names[j] == shuffled_names_lists[i-1][j] for j in range(len(shuffled_names_lists[i-1]))):
                random.shuffle(shuffled_names)
            # Append the shuffled list to the list of shuffled lists
            shuffled_names_lists.append(shuffled_names)
        elif i == 2:
            while any(shuffled_names[j] == shuffled_names_lists[i-1][j] for j in range(len(shuffled_names_lists[i-1]))) or any(shuffled_names[j] == shuffled_names_lists[i-2][j] for j in range(len(shuffled_names_lists[i-2]))):
                random.shuffle(shuffled_names)
            # Append the shuffled list to the list of shuffled lists
            shuffled_names_lists.append(shuffled_names)
        elif i == 3:
            while any(shuffled_names[j] == shuffled_names_lists[i-1][j] for j in range(len(shuffled_names_lists[i-1]))) or any(shuffled_names[j] == shuffled_names_lists[i-2][j] for j in range(len(shuffled_names_lists[i-2]))) or any(shuffled_names[j] == shuffled_names_lists[i-3][j] for j in range(len(shuffled_names_lists[i-3]))):
                random.shuffle(shuffled_names)
            # Append the shuffled list to the list of shuffled lists
            shuffled_names_lists.append(shuffled_names)
    # Print the shuffled lists
    for i in range(len(names)):
        print(shuffled_names_lists[0][i] + ': ' + shuffled_names_lists[1][i] + ', ' + shuffled_names_lists[2][i] + ', ' + shuffled_names_lists[3][i])

shuffleNames(names)
    