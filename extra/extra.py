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

# Max h_ij = h_ji pairs selection
def select_max_interest(added_participants, n_people):
    interest_pairs = {(i, j): interest[i][j] for i in range(n_participants) for j in range(i)}
    sorted_interest_pairs = sorted(interest_pairs.items(), key=lambda item: item[1])
    sorted_interest_pairs.reverse()
    sorted_interest_pairs = dict(sorted_interest_pairs)
    people = []
    for pair in list(sorted_interest_pairs.keys()):
        if pair[1] in people and pair[0] not in people and pair[0] not in day_participants:
            people.append(pair[0])
        if pair[0] in people and pair[1] not in people and pair[1] not in day_participants:
            people.append(pair[1])
        if pair[0] not in people and pair[1] not in people and pair[0] not in day_participants and pair[1] not in day_participants:
            people.append(pair[0])
            people.append(pair[1])
        if len(people) + 1 == n_people:
            interest_pairs = {(i, j): interest[i][j] for i in people for j in range(i)}
            sorted_interest_pairs = sorted(interest_pairs.items(), key=lambda item: item[1])
            sorted_interest_pairs.reverse()
            sorted_interest_pairs = dict(sorted_interest_pairs)
            for opponent in list(sorted_interest_pairs.keys()):
                if opponent[1] not in people and opponent[1] not in day_participants:
                    people.append(opponent[1])
                    break
        if len(people) == n_people:
            return people


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

overall = 0
for i in range(len(interest)):
    for j in range(i):
        overall = overall + interest[i][j]

print("Overall interest: " + str(overall))
exit(0)
