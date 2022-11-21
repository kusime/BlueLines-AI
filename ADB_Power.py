# https://openbase.com/python/pure-python-adb/documentation
from ppadb.client import Client as AdbClient


class ADB:
    def __init__(self, deviceName: str):
        # Default is "127.0.0.1" and 5037
        client = AdbClient(host="127.0.0.1", port=5037)
        self.device = client.device(deviceName)

    def tap(self, point):
        self.device.shell(f'input tap {int(point[0])} {int(point[1])}')

    def screenshot(self, filename='screenshot'):
        result = self.device.screencap()
        with open(f'{filename}.png', "wb") as fp:
            fp.write(result)


if __name__ == "__main__":
    test = ADB("S8M6R20710001175")
    # test.tap((1000, 1000))
    test.screenshot("Net Error")
