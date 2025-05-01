"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os
import re

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["mongodb-org"])
def test_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    p = host.package(pkg)
    assert p.is_installed
    assert p.version.startswith("3.6.23")


@pytest.mark.parametrize("pkg", ["pymongo"])
def test_pip2_packages(host, pkg):
    """Test that the pip2 packages were installed."""
    assert pkg in host.pip.get_packages(pip_path="/usr/bin/pip2")


@pytest.mark.parametrize("pkg", ["pymongo"])
def test_pip3_packages(host, pkg):
    """Test that the pip3 packages were installed."""
    assert pkg in host.pip.get_packages(pip_path="/usr/bin/pip3")


@pytest.mark.parametrize(
    "prop,regex",
    [
        ("After", r"^After=.*network\.target"),
        ("After", r"^After=.*multi-user\.target"),
        ("After", r"^After=.*cloud-final\.service"),
        ("AssertPathIsMountPoint", r"^AssertPathIsMountPoint=/var/lib/mongodb$"),
        (
            "AssertPathIsMountPoint",
            r"^AssertPathIsMountPoint=/var/lib/mongodb/journal$",
        ),
        ("AssertPathIsMountPoint", r"^AssertPathIsMountPoint=/var/log/mongodb$"),
        (
            "ExecStart",
            r"^ExecStart=.*argv\[\]=/usr/bin/numactl --interleave=all /usr/bin/mongod --config /etc/mongod\.conf",
        ),
        ("RequiresMountsFor", r"^RequiresMountsFor=.*/var/lib/mongodb"),
        ("RequiresMountsFor", r"^RequiresMountsFor=.*/var/lib/mongodb/journal"),
        ("RequiresMountsFor", r"^RequiresMountsFor=.*/var/log/mongodb"),
        ("RuntimeDirectory", r"^RuntimeDirectory=mongodb$"),
        ("RuntimeDirectoryMode", r"^RuntimeDirectoryMode=0744$"),
    ],
)
def test_unit_content(host, prop, regex):
    """Test that unit parameters were modified via drop-ins as expected."""
    cmd = f"systemctl show --no-pager --property={prop} mongod.service"
    cmd_result = host.run(cmd)
    assert cmd_result.rc == 0, "{cmd} command failed"
    assert (
        re.search(regex, cmd_result.stdout) is not None
    ), f"Regex {regex} does not match any line in {cmd} output."


@pytest.mark.parametrize("svc", ["mongod"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled
