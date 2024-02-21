
from wallchanger.wallchanger import Wallchanger


def test_can_load_config_file():
    wallchanger = Wallchanger()
    wallchanger.load("/data/code/bithive/wallchanger/tests/assets/config.conf")
    assert wallchanger.config['time']
    assert wallchanger.config['wallpapers']