from abc import abstractmethod


class Observer:
    @abstractmethod
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class SmsNotifier(Observer):
    def update(self, subject):
        print(f"SMS -> {subject.students[-1].username} has joined the course {subject.name}")


class EmailNotifier(Observer):
    def update(self, subject):
        print(f"E-mail -> {subject.students[-1].username} has joined the course {subject.name}")
