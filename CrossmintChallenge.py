import requests
import time

API_URL = 'https://challenge.crossmint.io/api/'
CANDIDATE_ID = '231cc6e9-1eff-41b3-bf61-b6df43470a9c'

SOLOON_COLORS = ['blue', 'red', 'purple', 'white']
COMETH_DIRECTIONS = ['up', 'down', 'left', 'right']

RATE_LIMIT_API_CODE = 429
RATE_LIMIT_WAIT_TIME = 5
PHASE_2_COMMANDS = []

def get_goal_map():
    '''
    Gets the goal map from the API
    '''

    return requests.get(API_URL + 'map/' + CANDIDATE_ID + '/goal').json()

def post_polyanet(row: int, column: int):
    '''
    Posts a polyanet to the API
    '''

    return requests.post(API_URL + 'polyanets', json={'candidateId': CANDIDATE_ID, 'row': row, 'column': column})

def delete_polyanet(row: int, column: int):
    '''
    Deletes a polyanet from the API
    '''

    return requests.delete(API_URL + 'polyanets', json={'candidateId': CANDIDATE_ID, 'row': row, 'column': column})

def post_soloon(row: int, column: int, color_index: int):
    '''
    Posts a soloon to the API
    '''

    return requests.post(API_URL + 'soloons', json={'candidateId': CANDIDATE_ID, 'row': row, 'column': column, 'color': SOLOON_COLORS[color_index]})

def post_cometh(row: int, column: int, direction_index: int):
    '''
    Posts a cometh to the API
    '''

    return requests.post(API_URL + 'comeths', json={'candidateId': CANDIDATE_ID, 'row': row, 'column': column, 'direction': COMETH_DIRECTIONS[direction_index]})

def generate_phase_2_commands():
    '''
    Generates the commands for phase 2.
    Uses the goal map to determine what to POST.
    Commands are saved to PHASE_2_COMMANDS.
    '''

    goal_map = get_goal_map()['goal']

    for row in range(len(goal_map)):
        for column in range(len(goal_map[row])):
            if goal_map[row][column] == 'POLYANET':
                PHASE_2_COMMANDS.append('post_polyanet(' + str(row) + ', ' + str(column) + ')')
            elif "SOLOON" in goal_map[row][column]:
                color = goal_map[row][column].split('_')[0].lower()
                color_index = SOLOON_COLORS.index(color)

                PHASE_2_COMMANDS.append('post_soloon(' + str(row) + ', ' + str(column) + ', ' + str(color_index) + ')')
            elif "COMETH" in goal_map[row][column]:
                direction = goal_map[row][column].split('_')[0].lower()
                direction_index = COMETH_DIRECTIONS.index(direction)

                PHASE_2_COMMANDS.append('post_cometh(' + str(row) + ', ' + str(column) + ', ' + str(direction_index) + ')')

def process_api_commands(commands: list):
    '''
    Processes a list of API commands.
    If a rate limit is reached, the function will wait and try again.
    '''

    response_code = 0
    for command in commands:
        loc = {}
        exec('response = ' + command, globals(), loc)
        response = loc['response']

        response_code = response.status_code

        while response_code == RATE_LIMIT_API_CODE:
            print(f'Code {RATE_LIMIT_API_CODE}: Rate limit reached. Waiting {RATE_LIMIT_WAIT_TIME} seconds...')
            time.sleep(RATE_LIMIT_WAIT_TIME)
            loc = {}
            exec('response = ' + command, globals(), loc)
            response = loc['response']

            response_code = response.status_code

        if (response.ok): print('Success: ' + command)

def phase_1():
    '''
    Phase 1 of the challenge.
    Posts a polyanet to every POLYANET location on the goal map.
    '''

    goal_map = get_goal_map()['goal']

    for row in range(len(goal_map)):
        for column in range(len(goal_map[row])):
            if goal_map[row][column] == 'POLYANET':
                post_polyanet(row, column)

def phase_2():
    '''
    Phase 2 of the challenge.
    Generates commands based on the goal map and processes them.
    '''

    if len(PHASE_2_COMMANDS) == 0:
        generate_phase_2_commands()
        process_api_commands(PHASE_2_COMMANDS)
    else:
        process_api_commands(PHASE_2_COMMANDS)
    

def main():
    '''
    Main function.
    '''
    
    # phase_1()
    phase_2()

if __name__ == "__main__":
    main()