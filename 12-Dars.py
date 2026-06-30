class Task:
    def __init__(self, text):
        self.text = text
        self.done = False

# creating objects (instances) from the class
task1 = Task("Buy milk")
task2 = Task("Walk the dog")

print(task1.text)   # Buy milk
print(task2.text)   # Walk the dog
print(task1.done)   # False


class PriorityTask(Task):
    def __init__(self, text, priority):
        super().__init__(text)       # runs Task's __init__ first
        self.priority = priority      # then adds the new attribute

    def __str__(self):
        status = "✓" if self.done else " "
        return f"[{status}] ({self.priority}) {self.text}"

t = PriorityTask("Submit project", "high")
t.mark_done()        # inherited from Task — no need to rewrite it!
print(t)              # [✓] (high) Submit project
        