import sys
import os
import Msg
from termcolor import colored as _c

class IO:
    def __init__(self, main_obj: object):
        self.help_text = f'''\
{_c("******************************************************************************************************", "cyan")}

You can enter the following command to "Submit" or "View a Problem"
    - {self._command_info("test", "[Problem_ID] [Language]", "test a problem")}
    - {self._command_info("help", "", "show this text")}
    - {self._command_info("status", "[Problem_ID]", "show the submit result of specific problem")}
    - {self._command_info("edit", "[Problem_ID] [Language]", "edit problem answer")}
    - {self._command_info("add", "[Problem_ID] [Language]", "add a problem to the system")}
    - {self._command_info("add", "[Problem_ID] [Language]", "remake a problem in the system")}
    - {self._command_info("exit", "", "exit the system")}

{_c("******************************************************************************************************", "cyan")}
'''
        self.react = main_obj()
        self.all_command = {
            'test': self._test, 
            'help': self._help,
            'status': self._status,
            'edit': self._edit,
            'add': self._add,
            'exit': self._exit,
            'remake': self._remake
        }

    def _command_info(self, command: str, args: str, info: str):
        return f'{_c(command, "yellow")} {_c(args, "blue")}: {info}'

    def _argument_err_msg(self, expected: int, got: int):
        self.output('system', f'argument expected {expected} got {got}')

    def _remake(self, args: tuple):
        if len(args) != 2:
            self._argument_err_msg(2, len(args))
            return
        self.react.remake_problem(args[0], args[1])

    def _add(self, args: tuple):
        if len(args) != 2:
            self._argument_err_msg(2, len(args))
            return
        self.react.add_problem(args[0], args[1])

    def _test(self, args: tuple):
        if len(args) != 2:
            self._argument_err_msg(2, len(args))
            return
        self.react.test_problem(args[0], args[1])

    def _help(self, args: tuple =tuple()):
        if(len(args) != 0):
            self._argument_err_msg(0, len(args))
            return
        print(self.help_text)

    def _exit(self, args: tuple=tuple()):
        if len(args) != 0:
            self._argument_err_msg(0, len(args))
            return
        self.react.exit()

    def _status(self, args: tuple):
        if len(args) != 1:
            self._argument_err_msg(1, len(args))
            return
        result = self.react.get_status(args[0])
        print()
        for p in result:
            if result[p] == 'AC':
                print(f'\t- {p}: {_c("[", "cyan")}{_c(result[p], "green")}{_c("]", "cyan")}')
            elif result[p] == '-':
                print(f'\t- {p}: {_c("[", "cyan")}{result[p]}{_c("]", "cyan")}')
            else:
                print(f'\t- {p}: {_c("[", "cyan")}{_c(result[p], "red")}{_c("]", "cyan")}')
        print()

    def _edit(self, args: tuple):
        if len(args) != 2:
            self._argument_err_msg(2, len(args))
            return
        self.react.edit(args[0], args[1])

    def start(self):
        self.output('system', 'Initializing the system')
        self.react.init()
        while True:
            try:
                print(f'{_c("[", "cyan")}In{_c("]", "cyan")}: ', end='')
                _input = input()
                commands = _input.strip().split()
                if len(commands) == 0:
                    continue
                if not (commands[0] in self.all_command):
                    continue
                self.all_command[commands[0]](tuple(commands[1:]))
                self.react.main()
            except Msg.WrongAnswer as sr:
                self.output(_c('WA', 'red'), f'At line {sr.at_line}\n{_c("Your answer: ", "blue")}\n{sr.user_output}\n{_c("Correct answer:", "blue")}\n{sr.correct_output}')
            except Msg.CompileError as sr:
                self.output(_c('CE', 'red'), f'{_c("Compiler message: ", "blue")}\n{sr.compile_msg}')
            except Msg.TimeLimitExceed as sr:
                self.output(_c('TLE', 'red'), f'Execution time: {sr.execution_time}s')
            except Msg.OutputLimitExceed as sr:
                line_msg = lambda x: ['lines', 'line'][int(x==1)]
                self.output(_c('OLE', 'red'), f'Expected {sr.ans_line} {line_msg(sr.ans_line)} got {sr.user_line} {line_msg(sr.user_line)}')
            except Msg.Accept as sr:
                self.output(_c('AC', 'green'), 'Accepted')
                os.system(f'cat {sr.file_name} | clip.exe')
                self.output('system', 'accepted answer had copied to your clipboard')
            except KeyboardInterrupt:
                print()
            except Msg.ProblemNotFound:
                self.output('system', 'problem id not found')
            except Msg.RuntimeError as sr:
                self.output(_c('RE', 'red'), f'{_c("In stderr: ", "blue")}\n{sr.return_msg}')
            # except FileNotFoundError:
            #     self.output('system', 'submit file not found')

    def output(self, pre_msg: str, msg: str):
        print(f'{_c("[", "cyan")}{pre_msg}{_c("]", "cyan")}: {msg}')
