with open("gambling_data.txt", "r") as f:
    data = f.readlines()
    total_value = 0
    for line in data:
        values = line.split(",")
        for value in values:
            total_value += int(value)
    
    print(total_value / len(data))