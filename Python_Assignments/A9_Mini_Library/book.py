class Book:
    def __init__(self, title, author, copies=1):
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if copies < 0:
            raise ValueError("Copies cannot be negative")
        self.title = title
        self.author = author
        self.__copies = copies

    def get_copies(self):
        return self.__copies

    def add_copies(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__copies += amount

    def borrow(self):
        if self.__copies <= 0:
            return False
        self.__copies -= 1
        return True

    def return_copy(self):
        self.__copies += 1

    def to_dict(self):
        return {"title": self.title, "author": self.author, "copies": self.__copies}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], int(data["copies"]))

    def __str__(self):
        return f"{self.title} by {self.author} ({self.__copies} copies)"
