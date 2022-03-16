import GetProblem
import IO
import Msg

import json
import subprocess
import colorama
import sys
import os

LANGUAGE_EXT = dict()
CMD_MACRO = {   # pass the full path in it
    '@Dir': lambda x: os.path.join(*(x.strip().split(os.path.join('@', '@')[1])[:-1])),
    '@File-Ext': lambda x: (x.strip().split(os.path.join('@', '@')[1])[-1]).split('.')[0],
    '@File': lambda x: x.strip().split(os.path.join('@', '@')[1])[-1],
    '@Path': lambda x: x
}

class Main:
    def __init__(self):
        self.options = None
        self.status = None
        self.GetProblem = GetProblem.GetProblem()
        self.test_data = dict()

    def Gpath(self, *args):
        return os.path.join('.', *args)

    def _Msbfn(self, fn, lan):
        return f'{fn}.{LANGUAGE_EXT[lan]}'

    def cMacro(self, cmd, full_path):
        for macro in CMD_MACRO:
            cmd = cmd.replace(macro, CMD_MACRO[macro](full_path))
        return cmd

    def init(self):
        with open(self.Gpath('settings', 'options.json'), 'r', encoding='utf-8') as jsfile:
            self.options = json.loads(jsfile.read())
        
        with open(self.Gpath('settings', 'status.json'), 'r', encoding='utf-8') as jsfile:
            self.status = json.loads(jsfile.read())

        for lan in self.options['language']:
            LANGUAGE_EXT[lan] = self.options['language'][lan]['file_ext']

    def edit(self, pid, language):
        filename = self.Gpath('solutions', pid, self._Msbfn(pid, language))
        vi = subprocess.Popen(f'nvim {filename}', shell=True)
        vi.wait()

    def test_problem(self, pid: str, language: str):
        process_output = lambda x: x.strip().replace('\r', '').split('\n')

        if not (pid in self.test_data):
            self.GetProblem.get_problem(pid)
            self.test_data[pid] = self.GetProblem.get_test_data()
        commands = self.options['language'][language]['submit_commands'].copy()
        fn = self.options['language'][language]['submit_file_name']
        path = self.Gpath('submit_files', fn)
        ufile_path = self.Gpath('solutions', pid, self._Msbfn(pid, language))
        sfile_path = self._Msbfn(path, language)
        if 'compile' in commands:
            commands['compile'] = self.cMacro(commands['compile'], sfile_path)
        commands['run'] = self.cMacro(commands['run'], sfile_path)
        with open(ufile_path, 'r', encoding='utf-8') as user_file:
            with open(sfile_path, 'w', encoding='utf-8') as submit_file:
                submit_code = user_file.read()
                submit_file.write(submit_code)
        comp_outs, comp_errs = None, None
        run_outs, run_errs = None, None
        if 'compile' in self.options['language'][language]['submit_commands']: # Language that needs to compile
            compiler = subprocess.Popen(commands['compile'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            try:
                comp_outs, comp_errs = compiler.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                compiler.kill()
                comp_outs, comp_errs = compiler.communicate()
            comp_outs, comp_errs = comp_outs.decode('utf-8'), comp_errs.decode('utf-8')
            if compiler.returncode != 0:
                self.status[pid] = 'CE'
                raise Msg.CompileError(comp_errs)
        run = subprocess.Popen(commands['run'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        try:
            run_outs, run_errs = run.communicate(input=self.test_data[pid]['input'].encode('utf-8'), timeout=10)
        except subprocess.TimeoutExpired:
            run.kill()
            run_outs, run_errs = run.communicate()
            self.status[pid] = 'TLE'
            raise Msg.TimeLimitExceed(10)
        run_outs, run_errs = run_outs.decode('utf-8'), run_errs.decode('utf-8')
        if run.returncode != 0:
            self.status[pid] = 'RE'
            raise Msg.RuntimeError(run_errs)
        user_list, ans_list = process_output(run_outs), process_output(self.test_data[pid]['output'])
        if len(ans_list) > len(user_list):
            self.status[pid] = 'WA'
            raise Msg.WrongAnswer(len(user_list)+1, ans_list[len(user_list)], '')
        if len(ans_list) < len(user_list):
            self.status[pid] = 'OLE'
            raise Msg.OutputLimitExceed(len(ans_list), len(user_list))
        for line, (user, ans) in enumerate(zip(user_list, ans_list)):
            if user.strip() != ans.strip():
                self.status[pid] = 'WA'
                raise Msg.WrongAnswer(line+1, ans, user)

        self.status[pid] = 'AC'
        raise Msg.Accept(ufile_path)

    def get_status(self, pid):
        if pid == 'all':
            return self.status
        if not (pid in self.status):
            raise Msg.ProblemNotFound
        return {pid: self.status[pid]}

    def save_status(self):
        with open(self.Gpath('settings', 'status.json'), 'w', encoding='utf-8') as jsfile:
            json.dump(self.status, jsfile)

    def remake_problem(self, pid, language):
        file_path = self.Gpath("solutions", pid, self._Msbfn(pid, language))
        if os.path.exists(file_path):
            os.system(f'rm {file_path}')
        self.status[pid] = '-'
        self.add_problem(pid, language)

    def add_problem(self, pid, language):
        if not (pid in self.status):
            self.status[pid] = '-'
            self.save_status()
            os.system(f'mkdir {self.Gpath("solutions", pid)}')
        file_path = self.Gpath("solutions", pid, self._Msbfn(pid, language))
        if not os.path.exists(file_path):
            os.system(f'touch {file_path}')

    def exit(self):
        self.save_status()
        sys.exit()

    def main(self):
        pass

if __name__ == '__main__':
    colorama.init()
    program = IO.IO(Main)
    program.start()
