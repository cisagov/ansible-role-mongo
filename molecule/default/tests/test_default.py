"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["mongodb-org"])
def test_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["pymongo"])
def test_pip2_packages(host, pkg):
    """Test that the pip2 packages were installed."""
    assert pkg in host.pip.get_packages(pip_path="/usr/bin/pip2")


@pytest.mark.parametrize("pkg", ["pymongo"])
def test_pip3_packages(host, pkg):
    """Test that the pip3 packages were installed."""
    assert pkg in host.pip.get_packages(pip_path="/usr/bin/pip3")


@pytest.mark.parametrize(
    "file,content",
    [
        (
            "/lib/systemd/system/mongod.service",
            r"^After=network.target multi-user.target cloud-final.service$",
        ),
        (
            "/lib/systemd/system/mongod.service",
            r"^ExecStart=/usr/bin/numactl --interleave=all /usr/bin/mongod --config /etc/mongod.conf$",
        ),
        (
            "/lib/systemd/system/mongod.service",
            r"^RequiresMountsFor=/var/lib/mongodb /var/lib/mongodb/journal /var/log/mongodb$",
        ),
        (
            "/lib/systemd/system/mongod.service",
            r"^AssertPathIsMountPoint=/var/lib/mongodb$",
        ),
        (
            "/lib/systemd/system/mongod.service",
            r"^AssertPathIsMountPoint=/var/log/mongodb$",
        ),
        ("/lib/systemd/system/mongod.service", r"^RuntimeDirectory=mongodb$"),
        ("/lib/systemd/system/mongod.service", r"^RuntimeDirectoryMode=0744$"),
    ],
)
def test_files_content(host, file, content):
    """Test that config files were modified as expected."""
    f = host.file(file)

    assert f.exists
    assert f.contains(content)


@pytest.mark.parametrize("svc", ["mongod"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled
