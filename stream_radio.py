#coding: utf-8
import subprocess
import os
import signal


def start_stream(name, url, q="best", vol=100) -> subprocess:
    # すでに起動してないかチェック
    r, _ = check_pid_file(name=name)
    if  r !=0:
        # 起動してるっぽい場合はreturn
        return
        
    # check options
    vol = 0 if vol < 0 else 100 if vol > 100 else int(vol)
    q = "best" if q not in ["best","worst", "audio_only"] else q
    # build up cli
    cmd = f"exec streamlink -p 'ffplay -nodisp -volume {vol}' {url} {q}"
    # subprocess
    c = subprocess.Popen(cmd, shell=True)
    create_pid_file(name=name, pid=c.pid)
    return c

def kill(proc_pid) -> None:
    # Send the signal to the process
    os.kill(proc_pid, signal.SIGTERM)

def create_pid_file(name, pid=0) -> None:
    pid_fn = name + ".pid"
    # ファイルがなければkillを実施してファイルを作成
    if not os.path.exists(pid_fn):
        kill_pid(name=name)
    with open(pid_fn, mode="w") as f:
        f.write(str(pid)+"\n")
    return

def check_pid_file(name):
    pid_fn = name + ".pid"
    if not os.path.exists(pid_fn):
        pid = 0
    else:
        with open(pid_fn, mode="r") as f:
            pid = int(f.read())
    return pid, pid_fn

def kill_pid(name):

    pid, pid_fn = check_pid_file(name)
    if pid == 0:
        return False
    
    # kill. プロセスがなかったら空振り.
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        print("No pid :)")

    # pidファイルを削除
    os.remove(pid_fn)
    return True

if __name__ == '__main__':

    import time

    TEST_URL = "https://radiko.jp/#!/live/JOAK-FM"
    TEST_NAME = "NHK_FM"

    c = start_stream(name=TEST_NAME, url=TEST_URL, q="best")
    time.sleep(30)
    kill_pid(name=TEST_NAME)
    print("Done.")