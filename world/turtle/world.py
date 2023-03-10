import turtle as t
import maze.the_worlds_most_crazy_maze as obs
import mazerunner_path as mazepath


t.screensize(150, 250)
t.title("Toy Robot Five")
t.shape('triangle')
t.shapesize(0.5, 0.5, 1)
t.bgcolor('black')


def draw_obstacles(obs_list):
    '''
    Draws obstacles in turtle screen.
    Corrects robot to face up.
    '''
    t.tracer(0)
    for ob in obs_list:   
        x, y = ob[0], ob[1]
        t.color('black', 'white')
        t.begin_fill()
        t.goto(x,y)
        t.pendown()
        t.goto(x + 5 ,y)
        t.goto(x + 5,y + 5)
        t.goto(x,y + 5)
        t.goto(x,y)
        t.end_fill()
        t.penup()
    t.tracer(1)
    t.lt(90)
    t.goto(0,0)
    t.color('red')
    t.pencolor('red')
    t.pendown()


def show_obstacles(obs_list):
    '''
    Prints all possible obstacles in robot world.
    '''
    if len(obs_list) != 0:
        print('There are some obstacles:')
        for obs in obs_list:
            obs_x, obs_y = obs[0], obs[1]
            print(f'- At position {obs_x},{obs_y} (to {obs_x + 4},{obs_y + 4})')
    else:
        return


def show_position(robot_name, x, y):
    if y== 200:print('I am the top adge')
    elif y == -200: print('I am the bottom adge')
    elif x == -100 : print("I am at the left edge")
    elif x == 100 : print("I am at th right edge")
    print(' > '+robot_name+' now at position ('+str(x)+','+str(y)+').')


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """
    min_y, max_y = -200, 200
    min_x, max_x = -100, 100

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(steps, x, y, dir_index):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """
    directions = ['north', 'east', 'south', 'west']

    new_x = x
    new_y = y

    if directions[dir_index] == 'north':
        new_y = new_y + steps
    elif directions[dir_index] == 'east':
        new_x = new_x + steps
    elif directions[dir_index] == 'south':
        new_y = new_y - steps
    elif directions[dir_index] == 'west':
        new_x = new_x - steps

    if is_position_allowed(new_x, new_y):
        return True, new_x, new_y
    return False, x, y


def do_forward(robot_name, steps, x, y, dir_index, obs_list):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    update, new_x, new_y = update_position(steps, x, y, dir_index)
    if obs.is_position_blocked(new_x, new_y, obs_list) or obs.is_path_blocked(x, y, new_x, new_y, obs_list):
        return True, ''+robot_name+': Sorry, there is an obstacle in the way.', x, y
    elif update:
        t.fd(steps)
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.', new_x, new_y
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.', x, y


def do_back(robot_name, steps, x, y, dir_index, obs_list):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    update, new_x, new_y = update_position(-steps, x, y, dir_index)
    if obs.is_position_blocked(new_x, new_y, obs_list) or obs.is_path_blocked(x, y, new_x, new_y, obs_list):
        return True, ''+robot_name+': Sorry, there is an obstacle in the way.', x, y
    elif update:
        t.bk(steps)
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.', new_x, new_y  
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.', x, y


def do_right_turn(robot_name, dir_index):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """

    dir_index += 1
    if dir_index > 3:
        dir_index = 0
    
    t.rt(90)

    return True, ' > '+robot_name+' turned right.', dir_index


def do_left_turn(robot_name, dir_index):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """

    dir_index -= 1
    if dir_index < 0:
        dir_index = 3
    
    t.lt(90)

    return True, ' > '+robot_name+' turned left.', dir_index


def do_sprint(robot_name, steps, x, y, dir_index):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1, x, y, dir_index)
    else:
        (do_next, command_output, x, y) = do_forward(robot_name, steps, x, y, dir_index)
        print(command_output)
        return do_sprint(robot_name, steps - 1, x, y, dir_index)


def draw_boundary():
    '''
    Draws boundary of robot world.
    '''
    t.pencolor('green')
    t.color('black','white')
    t.penup()
    t.goto(100, 200)
    t.pendown()
    t.goto(100,-200)
    t.goto(-100, -200)
    t.goto(-100,200)
    t.goto(100,200)
    t.penup()


def run_maze(obs_list, side):
    """Go to the end of the end of the list path[]
    
    parameters:
    path  : (list) path to the end point
    
    side : the side of the end point of the robot. """

    print('starting maze run..')
    path = mazepath.draw_path(obs_list, side)

    end = path[-1]
    curr_pos = (0,0)
    for i in path:
    
        import turtle as b 
        b.shape("triangle")
        b.speed(0)
        if i[0] ==end[0] and end[1] == i[1]:
            break 
        b.goto(i)
        curr_pos = i
    return True, f'I am at the {side} of the edge', curr_pos[0], curr_pos[1]
    

draw_boundary()


def setup_world():
    pass

