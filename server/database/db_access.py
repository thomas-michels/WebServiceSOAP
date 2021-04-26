
def get(table) -> list:
    with open(rf"database/data/{table}.csv", 'r') as file:
        return file.readlines()


def get_by_id(table, id):
    with open(rf"database/data/{table}.csv", 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:
        line_formatted = line.split(',$')
        if line_formatted[0] == id:
            return line

    return None


def insert(table, line):
    with open(rf"database/data/{table}.csv", 'a') as file:
        # file.writelines('\n' + line)
        return line


def update(table: str, id: str, data: dict):
    with open(rf"database/data/{table}.csv", 'r') as file:
        lines = file.readlines()

    new_lines = [lines[0]]
    for line in lines[1:]:
        line_formatted = line.split(',$')
        if line_formatted[0] == id:
            new_lines.append(f'{data}\n')
        else:
            new_lines.append(line)

    # with open(rf"database/data/{table}.csv", 'w') as file:
    #     file.writelines(new_lines)


def delete(table, id):
    with open(rf"database/data/{table}.csv", 'r') as file:
        lines = file.readlines()

    new_lines = [lines[0]]
    for line in lines[1:]:
        line_formatted = line.split(',$')
        if line_formatted[0] != id:
            new_lines.append(line)

    # with open(rf"database/data/{table}.csv", 'w') as file:
        # file.writelines(new_lines)
