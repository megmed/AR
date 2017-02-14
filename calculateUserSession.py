import csv
import logging
from datetime import datetime

logging.basicConfig(filename='extract.log', level=logging.INFO)


def seconds_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return abs((d2 - d1).seconds)


def calculateSessions():
    with open('data/actions_1_von_4.csv', 'r', newline='') as csvfile:
        dataReader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        headers = next(dataReader, None)  # skip the headers
        print("""\
        Header
        %s
        """ % (headers))
        # sort data by userid and timestamp
        sortedlist = sorted(dataReader, key=lambda row: (row[0], row[1]), reverse=False)
        allActionsCount = 0
        actionsPerMinute = 0
        sessionActionsCount = 0
        sessionActions = []
        sessionDuration = 0
        sessionDurationMaxDistance = 300  # in seconds
        previousRow = None
        previousUserId = None

        # find periods of actions per user and calculate the usage duration and amount of actions
        for row in sortedlist:

            sessionActionsCount += 1
            allActionsCount += 1

            if sessionActionsCount > 1:
                print(', '.join(previousRow))

            userId = row[0]
            actionLabel = row[3]
            if sessionActionsCount > 1:
                actionsSecondsBetween = seconds_between(previousRow[1], row[1])
                print(actionsSecondsBetween)
                if userId != previousUserId or actionsSecondsBetween > sessionDurationMaxDistance:
                    if sessionActionsCount == 2:
                        sessionActions.append(actionLabel)

                    if (sessionDuration > 0):
                        actionsPerMinute = ((sessionActionsCount - 1) / (sessionDuration / 60))
                    # user id changed or max distance reached
                    print("""\

********** New Session ********
UserId: %s
Duration: %s
ActionsCount: %s
Actions/Minute: %s
Actions: %s
*******************************

                    """ % (
                    previousUserId, sessionDuration, (sessionActionsCount - 1), actionsPerMinute, sessionActions))

                    # reset numbers and actions list
                    sessionDuration = 0
                    actionsPerMinute = 0
                    sessionActionsCount = 0
                    sessionActions = []

                else:
                    # add time difference between those two actions
                    sessionDuration += actionsSecondsBetween
                    # add current action to the list of actions
                    sessionActions.append(actionLabel)

            if allActionsCount > 300:
                print(', '.join(row))
                break
            previousUserId = row[0]
            previousRow = row


calculateSessions()
