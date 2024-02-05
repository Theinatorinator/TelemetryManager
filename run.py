import sys
from os.path import dirname
if __name__ == "__main__":
    sys.path.append(dirname(__file__)+'\\python')
    from telemetrymanager import TelemetryManager
    TelemetryManager()
