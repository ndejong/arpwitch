
import ArpWitch

def test_name_exist():
    aw = ArpWitch
    assert aw.NAME is not None


def test_version_exist():
    aw = ArpWitch
    assert aw.VERSION is not None

def test_version_call():
    version = ArpWitch.ArpWitch().do_version()
    assert type(version) is dict
    assert 'version' in version.keys()
