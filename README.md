# Leaderboard

The microservice requests the data from score.txt.
The microservice checks every second for changes in score.txt

The format in which your data should be input to score.txt is:

[

{"User": "Name", "Score": int, "datetime": "month-day-year"},
{"User": "Bob", "Score": 100, "datetime": "02-24-2024"}

]

The microservice then reads this data using read_scores() and in update_leaderboard() it sorts the scores, removes 100% identical
submissions, ensures the datetime is not in the future, and then writes the top ten scores to file by calling
write_leaderboard(scores).
