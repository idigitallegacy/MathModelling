# Source data
n_participants = int(input("Amount of participants: "))
n_days = int(input("Event days amount:"))
n_tables = int(input("Event tables amount:"))
tables_capacity = list(map(int, input("Tables capacity:").split()))

# Getting started steps
tables_capacity = {i: tables_capacity[i] for i in range(len(tables_capacity))} # enumerating tables to sort them
interest = [[0 for i in range(n_participants)] for j in range(n_participants)]
visited = [[] for i in range(n_participants)]
tables_distribution = {}

# Sorting tables
sorted_tables_capacity = sorted(tables_capacity.items(), key=lambda item: item[1])
sorted_tables_capacity.reverse()
sorted_tables_capacity = dict(sorted_tables_capacity)


def calculate_new_table_interest(people, current_interest, human1, human2):
    suggested_interest = current_interest
    if human1 in people:
        for opponent in people:
            suggested_interest = suggested_interest + interest[opponent][human2]
    elif human2 in people:
        for opponent in people:
            suggested_interest = suggested_interest + interest[opponent][human1]
    else:
        for opponent in people:
            suggested_interest = suggested_interest + interest[opponent][human1] + interest[opponent][human2]
        suggested_interest = suggested_interest + interest[human1][human2]
    return suggested_interest


# Max s_table participants selection
def select_max_interest(added_participants, n_people):
    interest_pairs = {(i, j): interest[i][j] for i in range(n_participants) for j in range(i)}
    sorted_interest_pairs = sorted(interest_pairs.items(), key=lambda item: item[1])
    sorted_interest_pairs.reverse()
    sorted_interest_pairs = dict(sorted_interest_pairs)
    people = []

    current_table_interest = 0

    while len(people) < n_people:
        suggested_pair = None
        suggested_table_interest = current_table_interest
        for pair in list(sorted_interest_pairs.keys()):
            if (pair[0] in added_participants or pair[1] in added_participants) or (pair[0] in people and pair[1] in people):
                continue

            suggesting_table_interest = calculate_new_table_interest(people, current_table_interest, pair[0], pair[1])
            if suggesting_table_interest > suggested_table_interest or suggested_pair is None:
                suggested_pair = pair
                suggested_table_interest = suggesting_table_interest

        if suggested_pair[0] not in people and suggested_pair[1] not in people:
            people.append(suggested_pair[0])
            people.append(suggested_pair[1])
        if suggested_pair[0] in people and suggested_pair[1] not in people:
            people.append(suggested_pair[1])
        if suggested_pair[1] in people and suggested_pair[0] not in people:
            people.append(suggested_pair[0])
        current_table_interest = suggested_table_interest

        if len(people) + 1 == n_people:
            interest_pairs = {(i, j): interest[i][j] for i in people for j in range(n_participants)}
            sorted_interest_pairs = sorted(interest_pairs.items(), key=lambda item: item[1])
            sorted_interest_pairs.reverse()
            sorted_interest_pairs = dict(sorted_interest_pairs)

            suggested_pair = None
            suggested_table_interest = current_table_interest
            for pair in list(sorted_interest_pairs.keys()):
                if pair[1] in added_participants or pair[1] in people:
                    continue
                suggesting_table_interest = calculate_new_table_interest(people, current_table_interest, pair[0], pair[1])
                if suggesting_table_interest > suggested_table_interest or suggested_pair is None:
                    suggested_pair = pair
                    suggested_table_interest = suggesting_table_interest
            people.append(suggested_pair[1])
    return people


if __name__ == '__main__':
    # Action
    for day in range(n_days):
        tables_distribution[day] = {i: [] for i in range(n_tables)}
        day_participants = []
        for table in range(n_tables):
            capacity = tables_capacity[table]
            tables_distribution[day][table] = select_max_interest(day_participants, capacity)
            for i in tables_distribution[day][table]:
                day_participants.append(i)
                for j in tables_distribution[day][table]:
                    if i == j:
                        continue
                    interest[i][j] = interest[i][j] - day - 1 # - 1 because of days enumeration starts with 0
                    interest[j][i] = interest[j][i] - day - 1
                    if j not in visited[i]:
                        visited[i].append(j)
                    if i not in visited[j]:
                        visited[j].append(i)
            for i in tables_distribution[day][table]:
                for j in range(n_participants):
                    if j in tables_distribution[day][table]:
                        continue
                    if j not in visited[i] and i not in visited[j]:
                        interest[i][j] = interest[i][j] + day + 1
                        interest[j][i] = interest[j][i] + day + 1


    # Printing out
    for i in list(tables_distribution.keys()):
        print("Day " + str(i) + ".")
        for j in list(tables_distribution[i].keys()):
            print("\tTable " + str(j) + ". People: " + str(tables_distribution[i][j]))

    exit(0)
