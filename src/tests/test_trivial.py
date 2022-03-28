from arpwitch import arp_witch


def test_name_exist():
    aw = arp_witch
    assert aw.NAME is not None


def test_version_exist():
    aw = arp_witch
    assert aw.VERSION is not None


def test_version_call():
    version = arp_witch.ArpWitch().do_version()
    assert type(version) is dict
    assert "version" in version.keys()
