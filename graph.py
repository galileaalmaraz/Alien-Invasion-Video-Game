import json
import pygal
import datetime
import dateutil.parser as dateparser
import itertools

# 1. Line Graph
# - Measuring the motivational results
# - X-axis => time spent of user
# - Y-axis => scores made by usercle

# 2. Bar Graph
# - Comparing User’s scores
# - X-axis => Username
# - Y-axis => Score

# 3. Pie Chart
# - Measuring the time spent on each level
# The pie chart will contain an average of times that take stage user to complete a level


def load_data(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    return data


def get_user_data(filename, username):
    data = load_data(filename)
    for userdata in data:
        if userdata["username"] == username:
            return userdata
    return None


def get_diff_in_secs(start, end):
    start = dateparser.isoparse(start)
    end = dateparser.isoparse(end)
    difference = end - start
    seconds_in_day = 24 * 60 * 60
    m, s = divmod(difference.days * seconds_in_day + difference.seconds, 60)
    return m * 60 + s


def get_user_levels_data(userdata):
    levels = userdata["levels"]

    levels = [
        (
            level["level"],
            get_diff_in_secs(level["starttime"], level["endtime"]),
        )
        for level in levels
    ]
    return levels
    total_time = sum([l[1] for l in levels])
    levels_data = [(l[0], l[1] / total_time * 100) for l in levels]
    return levels_data


def avg(l):
    return sum(l) / len(l)


def get_levels_percentages(data):
    all_levels = [get_user_levels_data(row) for row in data]
    levels_nums_list = [[level_num for level_num, value in r] for r in all_levels]
    levels_nums_list = itertools.chain(*levels_nums_list)
    max_level = max(levels_nums_list)
    levels = {i: 0 for i in range(1, max_level + 1)}
    levels_count_map = {i: 0 for i in range(1, max_level + 1)}

    for row in all_levels:
        for level_num, time in row:
            levels[level_num] += time
            levels_count_map[level_num] += 1

    for key in levels.keys():
        levels[key] = levels[key] / levels_count_map[key]
    levels_averages = levels
    levels_time_sum = sum([t for t in levels_averages.values()])
    levels_percents = [
        (f"Level {k}", v / levels_time_sum * 100) for k, v in levels_averages.items()
    ]
    return levels_percents


def get_total_levels_score(levels):
    return sum([l["score"] for l in levels])


def get_total_time_of_game(levels):
    return sum([get_diff_in_secs(l["starttime"], l["endtime"]) for l in levels])


def get_user_score_pairs(data):
    return [(row["username"], get_total_levels_score(row["levels"])) for row in data]


def get_score_time_pairs(data):
    return [
        (get_total_time_of_game(row["levels"]), get_total_levels_score(row["levels"]))
        for row in data
    ]


def draw_pie_chart():
    pie_chart = pygal.Pie()
    pie_chart.title = "Average Time Spent on Each Level"
    data = load_data("./scores.json")
    levels_data = get_levels_percentages(data)
    for piece in levels_data:
        title, percent = piece
        pie_chart.add(title, percent)
    pie_chart.render_to_file("./graphs/piechart.svg")


def draw_bar_graph():
    bar_graph = pygal.Bar()
    bar_graph.title = "Users' Scores Comparison"
    data = load_data("./scores.json")
    score_pairs = get_user_score_pairs(data)
    for username, score in score_pairs:
        bar_graph.add(username, score)

    bar_graph.render_to_file("./graphs/bargraph.svg")


def draw_line_graph():
    line_graph = pygal.Line()
    line_graph.title = "Measuring Motivational Results"
    data = load_data("./scores.json")
    score_pairs = get_score_time_pairs(data)
    score_pairs = sorted(score_pairs, key=lambda x: x[0])
    scores = [s[1] for s in score_pairs]
    times = [s[0] for s in score_pairs]
    line_graph.x_labels = times
    line_graph.add("Correlation between time and score", scores)

    line_graph.render_to_file("./graphs/linegraph.svg")


def create_graphs():
    draw_pie_chart()
    draw_bar_graph()
    draw_line_graph()
