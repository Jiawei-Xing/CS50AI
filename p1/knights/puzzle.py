from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
A = And(AKnight, AKnave)
knowledge0 = And(
    # A is either a knight or a knave but not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # A is a knight and tells a truth.
    Implication(AKnight, A),
    # A is a knave and tells a lie.
    Implication(AKnave, Not(A))
)

# Puzzle 1
# A says "We are both knaves."
A = And(AKnave, BKnave)
# B says nothing.
knowledge1 = And(
    # A is either a knight or a knave but not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is either a knight or a knave but not both.
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # A is a knight and tells a truth.
    Implication(AKnight, A),
    # A is a knave and tells a lie.
    Implication(AKnave, Not(A))
)

# Puzzle 2
# A says "We are the same kind."
A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
B = And(Not(And(AKnight, BKnight)), Not(And(AKnave, BKnave)))
knowledge2 = And(
    # A is either a knight or a knave but not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is either a knight or a knave but not both.
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # A is a knight and tells a truth.
    Implication(AKnight, A),
    # A is a knave and tells a lie.
    Implication(AKnave, Not(A)),
    # B is a knight and tells a truth.
    Implication(BKnight, B),
    # B is a knave and tells a lie.
    Implication(BKnave, Not(B))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
A = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
# B says "A said 'I am a knave'."
B1 = Biconditional(A, AKnave)
# B says "C is a knave."
B2 = CKnave
# C says "A is a knight."
C = AKnight
knowledge3 = And(
    # A is either a knight or a knave but not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is either a knight or a knave but not both.
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # C is either a knight or a knave but not both.
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    # A is a knight and tells a truth.
    Implication(AKnight, A),
    # A is a knave and tells a lie.
    Implication(AKnave, Not(A)),
    # B is a knight and tells a truth.
    Implication(BKnight, And(B1, B2)),
    # B is a knave and tells a lie.
    Implication(BKnave, And(Not(B1), Not(B2))),
    # C is a knight and tells a truth.
    Implication(CKnight, C),
    # C is a knave and tells a lie.
    Implication(AKnave, Not(C))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
