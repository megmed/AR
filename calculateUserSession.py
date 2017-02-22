import csv
import logging
from datetime import datetime

logging.basicConfig(filename='extract.log', level=logging.INFO)


def seconds_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return abs((d2 - d1).seconds)


input_csv_file_path = 'data/actions_1_von_4.csv'
output_csv_file_path = 'data/output/sessions.csv'
actionsMaxDistance = 300  # max distance between two actions in seconds, if reached => new session


def calculateSessions():
    with open(input_csv_file_path, 'r', newline='') as csvfile:
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
        previousRow = None
        previousUserId = None

        # find periods of actions per user and calculate the usage duration and amount of actions
        with open(output_csv_file_path, 'w', newline='') as outfile:
            dataWriter = csv.writer(outfile, delimiter='\t', quoting=csv.QUOTE_NONE)
            # write header
            # dataWriter.writerow(['user_id', 'session_duration', 'session_actions_count', 'actions_per_minute', 'session_actions',
            #                  'brochure_view_fraction', 'product_view_fraction', 'store_view_fraction', 'favs_view_fraction',
            #                  'fav_store_fraction', 'start_screen_view_fraction'])
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
                    if sessionActionsCount == 2:
                        sessionActions.append(firstActionLabel)

                    if userId != previousUserId or actionsSecondsBetween > actionsMaxDistance:
                        sessionActionsCount = sessionActionsCount - 1
                        if (sessionDuration > 0):
                            actionsPerMinute = ((sessionActionsCount) / (sessionDuration / 60))
                        # user id changed or max distance reached
                        brochureViewFraction = sessionActions.count('brochure_view') / sessionActionsCount
                        productViewFraction = sessionActions.count('product_view') / sessionActionsCount
                        storeViewFraction = sessionActions.count('store_view') / sessionActionsCount
                        favsViewFraction = sessionActions.count('favs_view') / sessionActionsCount
                        favStoreFraction = sessionActions.count('fav_store') / sessionActionsCount
                        startScreenViewFraction = sessionActions.count('start_screen_view') / sessionActionsCount
                        print("""\

    ********** New Session ********
    UserId: %s
    Duration: %s
    ActionsCount: %s
    Actions/Minute: %s
    Actions: %s
    Brochure_View: %s
    Product_View: %s
    Store_View: %s
    Favs_View: %s
    Fav_Store: %s
    Start_Screen_View: %s
    *******************************

                        """ % (
                            previousUserId, sessionDuration, sessionActionsCount, actionsPerMinute, sessionActions,
                            brochureViewFraction, productViewFraction, storeViewFraction, favsViewFraction,
                            favStoreFraction, startScreenViewFraction))
                        # write to file
                        dataWriter.writerow(
                            [previousUserId, sessionDuration, sessionActionsCount, actionsPerMinute, sessionActions,
                             brochureViewFraction, productViewFraction, storeViewFraction, favsViewFraction,
                             favStoreFraction, startScreenViewFraction])

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
                elif sessionActionsCount == 1:
                    firstActionLabel = actionLabel

                # debug: limit to number of lines
                # if allActionsCount > 300:
                #   print(', '.join(row))
                #   break
                previousUserId = row[0]
                previousRow = row

    outfile.close()
    csvfile.close()


if __name__ == '__main__':
    print("run")

    calculateSessions()
