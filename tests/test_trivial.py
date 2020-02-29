
import ArpWitch

def test_name_exist():
    aw = ArpWitch
    assert aw.NAME is not None


def test_version_exist():
    aw = ArpWitch
    assert aw.VERSION is not None
