"""
    A pre-Battle validating script

    Ensures that tanks that are sent into the game with damage inflicting objectives,
    are not violating game mechanics, rules and balance + no other misc errors that could break scenario script
"""

class RESULT_STATUS_CODE(object):
    """This class stores errors a developer can encounter."""
    OK = 0
    ERROR_TOO_MUCH_DAMAGE = 1
    ERROR_DEAD_ENEMY = 2      # enemyHP = 0
    ERROR_MIN_MAX_DMG = 3     # Minimum Damage is bigger than Maximum Damage
    ERROR_PLACE_REQUIRED = 4  # placeRequired is bigger than enemy team size (or None/Null)
    ERROR_MISC = 5            # An error that couldnt be classified - probably failed to read one of the params




def returnErrorName(x):
    """Returns ERROR name by its ID.
    Args:
        x (int): error id
    Returns:
        Error Name
    """

    return {
        RESULT_STATUS_CODE.OK : 'OK',
        RESULT_STATUS_CODE.ERROR_TOO_MUCH_DAMAGE : 'ERROR_TOO_MUCH_DAMAGE',
        RESULT_STATUS_CODE.ERROR_DEAD_ENEMY : 'ERROR_DEAD_ENEMY',
        RESULT_STATUS_CODE.ERROR_MIN_MAX_DMG : 'ERROR_MIN_MAX_DMG',
        RESULT_STATUS_CODE.ERROR_PLACE_REQUIRED : 'ERROR_PLACE_REQUIRED',
        RESULT_STATUS_CODE.ERROR_MISC : 'ERROR_MISC'
    }[x]


"""list: List of dictionaries of tanks.
    Structure of tank dict: 

        'name': '_str_',
        'tankHP': _int_,
        'team': _int_,
        'damageMin': _int_,
        'damageMax':_int_,
        'placeRequired':_int_

"""
TANK_INPUT = [
    {
        'name': 'botTest_1',
        'tankHP': 100,
        'team': 1,
        'damageMin': 100,
        'damageMax':150,
        'placeRequired':2
    },
    {
        'name': 'botTest_2',
        'tankHP': 200,
        'team': 1,
        'damageMin': 50,
        'damageMax': 100,
        'placeRequired': 1
    },
    {
        'name': 'botTest_3',
        'tankHP': 300,
        'team': 1,
        'damageMin': 100,
        'damageMax': 150,
        'placeRequired': 4
    },
    {
        'name': 'botTest_4',
        'tankHP': 400,
        'team': 1,
        'damageMin': 10,
        'damageMax': 30,
        'placeRequired': 3
    },
    {
        'name': 'botTest_5',
        'tankHP': 100,
        'team': 2,
        'damageMin': 100,
        'damageMax': 150,
        'placeRequired': 4

    },
    {
        'name': 'botTest_6',
        'tankHP': 200,
        'team': 2,
        'damageMin': 40,
        'damageMax': 60,
        'placeRequired': 1

    },
    {
        'name': 'botTest_7',
        'tankHP': 300,
        'team': 2,
        'damageMin': 25,
        'damageMax': 75,
        'placeRequired': 3
    },
    {
        'name': 'botTest_8',
        'tankHP': 400,
        'team': 2,
        'damageMin': 50,
        'damageMax': 100,
        'placeRequired': 2

    }
]

def countTeamSize(team, tankList):
    """Counts amount of tanks in a requested team.
    Args:
        team (int): team ID
        tankList (list): a list of tanks
    Returns:
        Returns integer of amount of tanks in a requested team
    """
    teamSize = 0
    for val in tankList:
        if val['team'] == team:
            teamSize += 1
    return teamSize

print "Player team size: ", countTeamSize(1, TANK_INPUT)
print "Enemy team size: ", countTeamSize(2, TANK_INPUT)
print

def countTeamHP(team, tankList):
    """Counts amount of Health Points a requested team has.
    Args:
        team (int): team ID
        tankList (list): a list of tanks
    Returns:
        Returns sum of Health Points a requested team has
    """

    teamHealth = 0
    for val in tankList:
        if val['team'] == team:
            teamHealth += val['tankHP']
    return teamHealth

print "Player team HP: ", countTeamHP(1, TANK_INPUT)
print "Enemy team HP: ", countTeamHP(2, TANK_INPUT)
print

def countTeamMinDMG(team, tankList):
    """Counts sum of minimal damage a requested team has to inflict
    Args:
        team (int): team ID
        tankList (list): a list of tanks
    Returns:
        Returns sum of minimal damage a requested team has to inflict
    """

    damageMin = 0
    for val in tankList:
        if val['team']==team:
            damageMin += val['damageMin']
    return damageMin

print "Player team Min DMG: ", countTeamMinDMG(1, TANK_INPUT)
print "Enemy team Min DMG: ", countTeamMinDMG(2, TANK_INPUT)
print

def countTeamMaxDMG(team, tankList):
    """Counts sum of maximum damage a requested team has to inflict
    Args:
        team (int): team ID
        tankList (list): a list of tanks
    Returns:
        Returns sum of maximum damage a requested team has to inflict
    """
    damageMax = 0
    for val in tankList:
        if val['team'] == team:
            damageMax += val['damageMax']
    return damageMax

print "Player team Max DMG: ", countTeamMaxDMG(1, TANK_INPUT)
print "Enemy team Max DMG: ", countTeamMaxDMG(2, TANK_INPUT)
print

def validateInputData(tank, tankInput):
    """Runs multiple tests to validate if a given tank doesnt violate game rules, balance and mechanics
    Args:
        tank (dict): tank in form of dict in following format:
        tankInput (list): List of tank dictionaries
    Returns:
        Returns an OK argument if no tests were failed
        Returns and raises error code if a rule was broken and terminates scenario
    """

    # Checks if enemy team has any HP at the beginning of match
    enemyHP = countTeamHP(2, tankInput)
    if (enemyHP <= 0):
        return RESULT_STATUS_CODE.ERROR_DEAD_ENEMY

    # Checks if a team is asked to inflict more damage than enemy has Health Points
    if (countTeamHP(2, tankInput) <= countTeamMaxDMG(1, tankInput)):
        return RESULT_STATUS_CODE.ERROR_TOO_MUCH_DAMAGE

    # Ensures that Minimum is smaller than Maximum damage
    damageMin = tank['damageMin']
    damageMax = tank['damageMax']
    if ((damageMin > damageMax)):
        return RESULT_STATUS_CODE.ERROR_MIN_MAX_DMG

    # Ensures that placeRequired is not out of bounds of team size
    placeRequired = tank['placeRequired']
    teamSize = countTeamSize(2, tankInput)
    if (placeRequired > teamSize):
        return RESULT_STATUS_CODE.ERROR_PLACE_REQUIRED

    # Run tests if tank can inflict requested damage and get requested place in battle Rating
    if (placeRequired == 1):
        if (damageMax < enemyHP):
            return RESULT_STATUS_CODE.OK
        elif ((damageMax == enemyHP or damageMin == enemyHP)):
            return RESULT_STATUS_CODE.OK
        elif (damageMax > enemyHP or damageMin > enemyHP):
            return RESULT_STATUS_CODE.ERROR_TOO_MUCH_DAMAGE
        else:
            return RESULT_STATUS_CODE.ERROR_MISC
    elif (1 < placeRequired <= teamSize):
        damageSim = (damageMax * placeRequired) + ((placeRequired - 1) * (placeRequired) / 2)
        if (damageSim <= enemyHP):
            return RESULT_STATUS_CODE.OK
        else:
            return RESULT_STATUS_CODE.ERROR_TOO_MUCH_DAMAGE
    else:
        return RESULT_STATUS_CODE.ERROR_MISC



def validateAllPlayers(tankInput):
    """Run validation test for every single tank

    Args:
        tankInput (list): List of tank dictionaries
    Returns:
        statusCode (int): result id     # If 0 - Test passed successfully
                                        # Other int - an error was occurred

        errorTank (str): tank name      # No error - will return None;
                                        # In case of error - will return tank name that failed test
    """
    statusCode = RESULT_STATUS_CODE.ERROR_MISC
    errorTank = None
    for tank in tankInput:
        statusCode = validateInputData(tank, tankInput)
        if statusCode != RESULT_STATUS_CODE.OK:
            errorTank = tank
            break
    return statusCode, errorTank


def performTest(tankInput):
    """
    Args:
        tankInput (list): List of tank dictionaries
    """
    result = validateAllPlayers(tankInput)
    if (result[0]) != 0:
        statusCode = result[0]
        errorTank = result[1]['name']
        print returnErrorName(statusCode)
        print "Error tank: ", errorTank
        print "Test was not passed"
    else:
        print "Test passed successfully"

performTest(TANK_INPUT)