from datetime import datetime, timedelta

durees = ["00:19:10", "01:45:30", "03:15:45"]

durees_timedelta = [datetime.strptime(d, "%H:%M:%S") - datetime.strptime("0:0:0", "%H:%M:%S") for d in durees]
somme_durees = sum(durees_timedelta, timedelta())
time = somme_durees / len(durees_timedelta)
if "." in str(time):
    time = str(time).split(".")[0]

print("Moyenne des durées :", time)