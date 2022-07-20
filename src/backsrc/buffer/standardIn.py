from src.backsrc.buffer.compBuffer import CompilerBufferedIO
import sys

def _input():
    val = sys.stdin.buffer.readline().decode().replace('\n','')
    sys.stdin.buffer.flush()
    return val