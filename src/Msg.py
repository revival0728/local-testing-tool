# submit result
class WrongAnswer(Exception):
    def __init__(self, at_line: int, correct_output: str, user_output: str):
        self.correct_output = correct_output
        self.user_output = user_output
        self.at_line = at_line
        super().__init__()

class CompileError(Exception):
    def __init__(self, compile_msg: str):
        self.compile_msg = compile_msg
        super().__init__()

class TimeLimitExceed(Exception):
    def __init__(self, execution_time: int):
        self.execution_time = execution_time
        super().__init__()

class RuntimeError(Exception):
    def __init__(self, return_msg: str):
        self.return_msg = return_msg
        super().__init__()

class OutputLimitExceed(Exception):
    def __init__(self, ans_line: int, user_line: int):
        self.ans_line = ans_line
        self.user_line = user_line
        super().__init__()

class Accept(Exception):
    def __init__(self, file_name):
        self.file_name = file_name
        super().__init__()

# system signal
class ContestOver(Exception):
    pass

class ContestStarted(Exception):
    pass

class PracticeMode(Exception):
    pass

class ProblemExist(Exception):
    def __init__(self, pid: str):
        self.pid = pid
        super().__init__()


# user error
class PracticeModeError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__()

class ContestModeError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__()

class ProblemNotFound(Exception):
    pass
