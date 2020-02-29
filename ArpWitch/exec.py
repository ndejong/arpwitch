
import time
import psutil
import subprocess
from threading import Thread

from . import EXEC_MAX_RUNTIME

from . import logger
from . import timestamp


class ArpWitchExecException(Exception):
    pass


class ArpWitchExec:

    subprocess_list = []

    def async_command_exec_thread(self, exec_command, packet_data, as_user=None):
        if exec_command is None:
            return

        logger.debug('ArpWitch.async_command_exec(<exec_command>, <packet_data>, <as_user>)')

        try:
            command_line = exec_command.format(
                IP=packet_data['ip']['addr'],
                HW=packet_data['hw']['addr'],
                TS=timestamp(),
                ts=timestamp().replace('+00:00','').replace(':','').replace('-','').replace('T','Z') ,
            )
        except KeyError:
            logger.critical('Unsupported {KEY} supplied in exec command, valid values are {IP}, {HW} and {TS}')
            exit(1)

        if as_user is not None:
            command_line = 'sudo -u {} {}'.format(as_user, command_line)

        thread = Thread(target=self.command_exec, args=(command_line,))
        thread.start()

    def async_command_exec_threads_wait(self, wait_max=EXEC_MAX_RUNTIME):
        wait_elapsed = 0
        wait_start = time.time()
        logger.debug('ArpWitch.async_command_exec_threads_wait(wait_max={})'.format(wait_max))

        while len(self.subprocess_list) > 0 and wait_elapsed < wait_max:
            for i, sp in enumerate(self.subprocess_list):
                if sp.poll() is not None:
                    if sp.returncode > 0:
                        logger.warning('exec thread returned with a non-zero returncode')
                    self.subprocess_list.pop(i)
            time.sleep(0.10)  # 100ms
            wait_elapsed = time.time() - wait_start
            #logger.debug('subprocess_list_len={} wait_elapsed={}'.format(len(self.subprocess_list), wait_elapsed))
        for i, sp in enumerate(self.subprocess_list):
            if sp.poll() is None:
                self.terminate_process(sp.pid)
        logger.debug('ArpWitch.async_command_exec_threads_wait() - done')

    def command_exec(self, command_line):
        logger.debug('ArpWitch.command_exec(command_line="{}")'.format(command_line))

        self.subprocess_list.append(
            subprocess.Popen(command_line, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        )

    def terminate_process(self, pid):
        logger.warning('ArpWitch.terminate_process(pid={})'.format(pid))

        # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        process = psutil.Process(pid)
        for process_child in process.children(recursive=True):
            process_child.terminate()
        process.terminate()
