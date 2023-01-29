from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .marsLink import MarsLink

class InstructionChecked:

    _value: bool

    def __init__(self, instructionsCheckedBooleanValue:bool = False) -> None:
        self._value = instructionsCheckedBooleanValue

    def __eq__(self, otherInstructionChecked: object) -> bool:
        return self._value == otherInstructionChecked._value

class Instructions:

    _value:str

    _expectedInsctructions = ["UP", "DOWN", "LEFT", "RIGHT"]

    def _checkInstruction(self, instruction: str, instructionsChecked:InstructionChecked) -> InstructionChecked:
        if instructionsChecked == InstructionChecked(instructionsCheckedBooleanValue=False): return instructionsChecked
        if instruction not in self._expectedInsctructions:
            return InstructionChecked(instructionsCheckedBooleanValue=False)
        return InstructionChecked(instructionsCheckedBooleanValue=True)


    def check(self) -> InstructionChecked:

        instructionChecked = InstructionChecked(instructionsCheckedBooleanValue=True)
        instructionList = self._value.split('-')
        for instruction in instructionList:
            instructionChecked = self._checkInstruction(instruction=instruction, instructionsChecked=instructionChecked)
        
        if instructionChecked == InstructionChecked(instructionsCheckedBooleanValue=False):
            print("The Instructions Value Must Be One of ('UP', 'DOWN', 'LEFT', 'RIGHT')")

        return instructionChecked

    def __init__(self, value:str) -> None:

        self._value = value

    def linkFormat(self) -> str:
        return "-".join([instruction[0] for instruction in self._value.split("-")])

class DirectionMessage:

    _value:str

    def __init__(self, value) -> None:
        self._value = value

    def __str__(self) -> str:
        
        if self._value == 'N': return 'North'
        if self._value == 'S': return 'South'
        if self._value == 'E': return 'East'
        if self._value == 'W': return 'West'

class CoordonneeMessage:

    _value:str

    def __init__(self, value) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"[{self._value}] (y, x)"

class PositionMessage:

    _value:str

    def __init__(self, value) -> None:
        self._value = value

    # format network link message to human message
    def __str__(self) -> str:

        messageSplited      = self._value.split("_")
        coordonneeMessage   = CoordonneeMessage(value=messageSplited[0])
        directionMessage    = DirectionMessage(value=messageSplited[1])

        return f"Le rover est en position '{coordonneeMessage}' en direction '{directionMessage}'"


class ObstacleMessage:

    _value:str

    def __init__(self, value) -> None:
        self._value = value

    # format network link message to human message
    def __str__(self) -> str:
        coordonneeMessage = CoordonneeMessage(value=self._value)

        return f"Il est bloqué par un obstacle en position '{coordonneeMessage}'"

class RoverMessage:

    _value : str

    def __init__(self, value) -> None:
        self._value = value

    # format network link message to human message
    def __str__(self) -> str:

        messageSplited  = self._value.split("_O_")
        positionMessage = PositionMessage(value=messageSplited[0])
        
        if len(messageSplited) > 1  : obstacleMessage = ObstacleMessage(value=messageSplited[1])
        else                        : obstacleMessage = None

        stringToReturn = str(positionMessage)
        if obstacleMessage is not None:
            stringToReturn += f", {obstacleMessage}"

        return stringToReturn


class Console:

    _marsLink:'MarsLink'

    def __init__(self, marsLink:'MarsLink') -> None:
        self._marsLink = marsLink

    def _getInstruction(self) -> Instructions:

        instructionChecked = InstructionChecked(instructionsCheckedBooleanValue=False)

        while instructionChecked == InstructionChecked(instructionsCheckedBooleanValue=False):
            instructions        = Instructions(value=input("instructions (example: UP-RIGHT-UP): "))
            instructionChecked  = instructions.check()

        return instructions
    
    def run(self) -> None:

        while True:

            instructions = self._getInstruction()
            roverMessage = self._marsLink.sendInstructions(instructions=instructions)
            print(roverMessage)