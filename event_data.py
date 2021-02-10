"""
Functions related to event analytics, such as finding best times to meet,
showing event members, etc
"""


from datetime import datetime, timedelta
from data import data
from error_checks import (check_event_id, check_is_member, 
                          check_logged_in, check_username)


CUTOFF = 3
SEARCH_DELAY = 2


def event_details(username, event_id):
    """
    Give details about the given event, specifically a list of event members,
    event creation date, event deadline, event length, event admin.

        Parameters:
            username (str): username of user requesting event details
            event_id (int): unique ID of event

        Exceptions:
            InputError when any of:
                username does not exist
                event_id does not exist
                username is not a member of event
            AuthError when:
                username is not logged in

        Returns:
            members ({str}): a set of event member usernames
            admin (str): username of event admin
            create_time (datetime.datetime): create time of event
            length (int): event length in hours
            deadline (datetime.date): event deadline
    """
    check_username(username)
    check_event_id(event_id)
    check_is_member(username, event_id)
    check_logged_in(username)
    event = data.events.get(event_id)
    details = {
        "members": event.member_usernames,
        "admin":  event.admin_username,
        "create_time": event.create_time,
        "length": event.event_length,
        "deadline": event.event_deadline,
    }

    return details


def find_best_times(username, event_id):
    """
    Find the best three closest time intervals for meeting,
    where 'best' is defined to be the date with the most
    members available. 
    If the event length is set, the start of the best time intervals 
    of that length will be found, otherwise a 3 hour interval will be
    assumed.
    If the event deadline is set, the best times before
    the deadline will be found, otherwise the maximum deadline
    of 60 days past the creation date.
    If not modified, the best times will be found within the default
    desired time range of the event.

        Parameters:
            username (str): username of user
            event_id (int): unique ID of event

        Exceptions:
            InputError when any of:
                username does not exist
                event_id does not exist
                username is not a member of event
            AuthError when any of:
                username is not logged in

        Returns:
            times ([datetime.datetime]): a list of the best times,
            from best to worst
    """
    check_username(username)
    check_event_id(event_id)
    check_is_member(username, event_id)
    check_logged_in(username)

    event = data.events.get(event_id)
    schedules = [s.times for s in list(event.availabilities.values())]
    intersection = find_intersection(schedules)
    print(event.admin_username)
    for u in event.availabilities:
        print(u, event.availabilities[u].times[:9])
    #print(intersection)
    best_intervals = find_best_intervals(intersection, CUTOFF, event)
    return best_intervals


def find_intersection(lists):
    """
    Given lists, a list of 2D lists, return another list 'result' of same
    dimensions as the 2D lists where each entry result[x][y] equals the sum
    of True l[x][y] entries for all l in lists. Assume lists is non-empty.
    """
    result = lists[0][:]
    x = len(result)
    y = len(result[0])
    for d in range(x):
        for t in range(y):
            result[d][t] = [l[d][t] for l in lists].count(True)

    return result


def time_to_index(time):
    return time.hour * 2 + time.minute // 30


def find_best_intervals(times, cutoff, event):
    search_start = datetime.now() + timedelta(hours=SEARCH_DELAY)
    min_day_index = (search_start.date() - event.create_time.date()).days
    min_first_day_time_index = search_start.hour * 2
    min_time_index = time_to_index(event.min_time)
    max_time_index = time_to_index(event.max_time)
    max_day_index = (event.event_deadline - event.create_time.date()).days

    best_scores = {}
    for d, day in enumerate(times):
        if d < min_day_index or d > max_day_index:
            continue

        for tim in range(min_time_index, max_time_index - event.event_length * 2 + 1):
            if d == min_day_index and tim < min_first_day_time_index:
                continue

            score = sum(day[tim:(tim + event.event_length)])
            if len(best_scores) < cutoff:
                best_scores[score] = (d, tim)
            else:
                min_best_score = min(list(best_scores.keys()))
                if score > min_best_score:
                    del best_scores[min_best_score]
                    best_scores[score] = (d, tim)

    highscores = sorted(list(best_scores.keys()), reverse=True)
    return [best_scores[hs] for hs in highscores]


def find_best_interval_starts(times, cutoff, event_id):
    """
    Given times (a 2D list where times[d][t] is the number of people available
    at the corresponding time), find the best 'cutoff' starting times of best
    intervals to meet, depending on event settings.
    """