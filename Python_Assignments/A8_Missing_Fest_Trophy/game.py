class Player:
    def __init__(self, name):
        self.name = name
        self.bag = []

    def collect(self, item):
        if item not in self.bag:
            self.bag.append(item)

    def has_item(self, item):
        return item in self.bag


class Place:
    def __init__(self, name, required_item=None):
        self.name = name
        self.required_item = required_item
        self.items = []

    def visit(self, player):
        if self.required_item and not player.has_item(self.required_item):
            print(f"FAILED: {self.name} is locked; need {self.required_item}.")
            return False
        print(f"Entered {self.name}.")
        return True


class CodeLock:
    def __init__(self, code):
        self.__code = str(code)

    def unlock(self, attempt):
        return str(attempt) == self.__code


class TrophyChest:
    def __init__(self, code):
        self.lock = CodeLock(code)
        self.opened = False

    def open(self, attempt):
        if self.lock.unlock(attempt):
            self.opened = True
            print("WIN: The trophy chest is open!")
            return True
        print("FAILED: Wrong code. The chest remains locked.")
        return False


def failed_route():
    print("\\n--- FAILED ROUTE ---")
    player = Player("Player")
    stage = Place("Main stage", "secret code")
    stage.visit(player)
    chest = TrophyChest("4821")
    chest.open("0000")


def winning_route():
    print("\\n--- WINNING ROUTE ---")
    player = Player("Player")
    canteen = Place("Canteen")
    lab = Place("Computer lab", "key")
    stage = Place("Main stage", "secret code")
    canteen.items.append("key")

    if canteen.visit(player):
        player.collect("key")
        print("Collected key.")

    if lab.visit(player):
        secret_code = "4821"
        player.collect("secret code")
        print("Found secret code.")
    else:
        return

    if stage.visit(player):
        chest = TrophyChest(secret_code)
        chest.open(secret_code)


if __name__ == "__main__":
    failed_route()
    winning_route()
