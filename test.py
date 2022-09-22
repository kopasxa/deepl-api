from datetime import datetime 
date = "2022-09-21T08:00:00.991Z"
print(datetime.strptime(date.replace("Z", "").replace("T", " "), '%Y-%m-%d %H:%M:%S.%f'))