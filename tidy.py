events = [
    ('High Jump'),
    ('Shot Put'),
    ('Javelin'),
    ('Triple Jump'),
    ('Long Jump'),
    ('Discus'),
]

current_event = None
current_group = None
current_gender = None
current_event_qualifying_distance = None

events_data = set()

competitors = []

with open('startlist.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        l = line.strip().split(',')
        #print(l)
        if l[0][:5] == 'Event':
            if current_event:
                events_data.add((
                    current_event,
                    current_gender,
                    current_event_qualifying_distance
                ))
            current_gender = l[1].split()[0]
            current_event = ' '.join(l[1].split()[1:-3])
            if current_event not in events:
                current_event = None
                continue
            current_group = int(l[1].split()[-1])

            print(current_gender, current_event, current_group)

        if l[1][:19] == 'Qualifying Standard':
            current_event_qualifying_distance = float(l[1][21:-1])

        if current_event and (l[0][:10] == 'Qualifying' or l[0][:5] == 'Round' or l[0][:6] == 'Group ' or (l[0] == '' and l[1].isdigit())):
            name = l[2] + ' ' + l[3]
            school = l[4]
            number = int(l[1])

            competitors.append({
                'name': name,
                'school': school,
                'number': number,
                'event': current_event,
                'gender': current_gender,
                'group': current_group
            })

with open('events_data.csv', 'w') as f:
    for event in events_data:
        f.write(f"{event[0]},{event[1] },{event[2]}\n")

with open('competitors_data.csv', 'w') as f:
    for competitor in competitors:
        f.write(f"{competitor['gender']},{competitor['event']},{competitor['group']},{competitor['number']},{competitor['name']},{competitor['school']}\n")