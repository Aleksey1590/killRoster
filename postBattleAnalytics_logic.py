"""
    A post-Battle validating script

    Script that can be used for killing/inflicting required amount of damage to the enemy and testing rating
"""


"""list: List of dictionaries of tanks.
    Structure of tank dict: 

        'name': '_str_',
        'tankHP': _int_,
        'team': _int_,
        'damageMin': _int_,
        'damageMax':_int_,
        'placeRequired':_int_

"""
tanks = [
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

# Initialize team's lists
team1 = []
team2 = []


def sortTeams(tanks):
    """ Sort tanks by their respective teams
        team1 - client's team
        team2 - enemy team
    """
    for tank in tanks:
        if tank['team']==1:
            team1.append(tank)
        elif tank['team']==2:
            team2.append(tank)
        else:
            raise TypeError


def countTeamHP (team, tankList):
    """Counts amount of Health Points a requested team has.
    Args:
        team (int): team ID
        tankList (list): a list of tanks
    Returns:
        Returns sum of Health Points a requested team has
    """
    teamHealth = 0
    for val in tankList:
        if val['team']==team:
            teamHealth += val['tankHP']
    return teamHealth

def countTeamDMG(team, tankList):
    """Counts sum of maximum damage a requested team has to inflict
    Args:
        team (int): team ID
        tankList (list): a list of tanks
    Returns:
        Returns sum of maximum damage a requested team has to inflict
    """

    totalDamage = 0
    for val in tankList:
        if val['team']==team:
            totalDamage += val['damageMax']
    return totalDamage


def startKilling (team1Temp, team2Temp):
    """
    Perform decision making process.
    Depending on the config files - script contains logic to make decision which tank from team 1 shoots a tank from team 2

    Args:
        team1Temp (list): team1 list that will be modified in this function
        team2Temp (list):
    Returns:
        team1 (list): Modified list of tanks from team 1 - after battle have happened
        team2 (list): Modified list of tanks from team 2 - after battle have happened
    """

    # Heads up that we want to inflict more damage than enemy has HP
    if countTeamDMG(1,tanks) > countTeamHP(2, tanks):
        print "We want to inflict more damage than enemy team has HP"
    elif countTeamDMG(1,tanks) < countTeamHP(2, tanks):
        print "Enemy team will win"
    else:pass
    print
    team1 = team1Temp
    team2 = team2Temp

    i=1

    # Show team stats before battle
    print "Enemy total HP Before Battle - ", countTeamHP(2, team2)
    print "Client's team total dmg to inflict Before Battle - ", countTeamDMG(1, team1)

    # Perform killing
    for tank1 in team1:
        print
        for tank2 in team2:
            print tank1['name'], " fights ", tank2['name']
            if tank2['tankHP']<=0:
                # This tank is already dead - do nothing and proceed
                print "This tank is already killed"
            elif tank2['damageMax'] == 0:
                # Tank has no more damage left to inflict - do nothing, break and proceed to another tank from team 1
                print "Tank has finished his damage infliction. Moving on to next tank in queue"
                break
            elif tank1['damageMax'] >= tank2['tankHP'] and tank2['tankHP']!=0:
                # tank1 shoots and inflicts (tank1['damageMax'] - tank2['tankHP']) damage to tank2
                print tank1['name'], " shoots and kills ", tank2['name']
                tank1['damageMax'] = tank1['damageMax'] - tank2['tankHP']
                tank2['tankHP'] = 0
            elif tank1['damageMax'] < tank2['tankHP'] and tank1['damageMax']!=0:
                # tank1 shoots and inflicts ( tank2['tankHP'] - tank1['damageMax'] ) damage to tank2
                print tank1['name'], " shoots ", tank2['name']
                tank2['tankHP'] = tank2['tankHP'] - tank1['damageMax']
                tank1['damageMax'] = 0
                print "Tank has finished his damage infliction. Moving on to next tank in queue"
                break
            else:
                # You shouldn't get here
                print "Exception"
            i += 1


    print
    print "Enemy total HP After Battle - ", countTeamHP(2, team2)
    print "Client's team total dmg to inflict After Battle - ", countTeamDMG(1, team1)
    print

    if countTeamHP(2, team2) > countTeamDMG(1, team1):
        print "Team 1 lost - enemy is still alive"
    elif countTeamHP(2, team2) <=countTeamDMG(1, team1):
        print "Team 1 won - enemy is killed"

    return team1, team2

sortTeams(tanks)

startKilling (team1, team2)