class Head():
    def __str__(self):
        return "Head"

class Hand():
    def __str__(self):
        return "Hand"

class Feet():
    def __str__(self):
        return "Feet"

class Arm():
    def __init__(self, hand: Hand):
        self.hand = hand

    def __str__(self):
        return f"Arm(with {self.hand})"

class Leg():
    def __init__(self, foot: Feet):
        self.foot = foot

    def __str__(self):
        return f"Leg(with {self.foot})"
    
class Torso():
    def __init__(self, head: Head, right_arm: Arm, left_arm: Arm, right_leg: Leg, left_leg: Leg):
        self.head = head
        self.right_arm = right_arm
        self.left_arm = left_arm
        self.right_leg = right_leg
        self.left_leg = left_leg
    
    def __str__(self):
        return f"Torso(with {self.head}, {self.right_arm}, {self.left_arm}, {self.right_leg}, {self.left_leg})"
        
class Human():
    def __init__(self):
        self.head = Head()

        self.right_hand = Hand()
        self.left_hand = Hand()

        self.right_arm = Arm(self.right_hand)
        self.left_arm = Arm(self.left_hand)

        self.right_foot = Feet()
        self.left_foot = Feet()

        self.right_leg = Leg(self.right_foot)
        self.left_leg = Leg(self.left_foot)

        self.torso = Torso(self.head, self.right_arm, self.left_arm, self.right_leg, self.left_leg)

        self.body_parts = [
            self.head, self.torso,
            self.right_arm, self.right_hand,
            self.left_arm, self.left_hand,
            self.right_leg, self.right_foot,
            self.left_leg, self.left_foot
        ]

    
    def anatomy(self):
        
        return self.body_parts


