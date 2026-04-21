def task_done(tasks):
    count = 0
    for task in tasks:
        if task[2] == "done":
            count += 1
    return count