# Copyright 2024 Open Source Robotics Foundation, Inc.
# Licensed under the Apache License, Version 2.0

from unittest.mock import Mock

from colcon_core.package_descriptor import PackageDescriptor
from colcon_ros_distro.package_discovery.ros_distro \
    import RosDistroPackageDiscovery
import pytest
from rosdistro.distribution_file import DistributionFile

requires_rep159 = pytest.mark.skipif(
    not hasattr(DistributionFile, 'merge_extends'),
    reason='needs the REP 159 rosdistro (format 3 extends)')


@pytest.mark.usefixtures('use_sim_distro')
def test_discover():
    extension = RosDistroPackageDiscovery()
    extension.add_arguments(parser=Mock(), with_default=True)

    args = Mock()
    args.ros_distro = 'sim'
    descs = extension.discover(args=args, identification_extensions={})

    sim_pkg_a = PackageDescriptor('sim/sim_pkg_a')
    sim_pkg_a.name = 'sim_pkg_a'
    sim_pkg_a.type = 'ros_distro'

    assert descs and sim_pkg_a in descs


def test_defaults():
    extension = RosDistroPackageDiscovery()
    extension.add_arguments(parser=Mock(), with_default=True)

    assert extension.has_default()

    args = Mock()
    args.ros_distro = 'sim'
    assert extension.has_parameters(args=args)


def test_no_identification_extensions():
    extension = RosDistroPackageDiscovery()
    extension.add_arguments(parser=Mock(), with_default=True)

    args = Mock()
    args.ros_distro = 'sim'
    with pytest.raises(AssertionError):
        extension.discover(args=args, identification_extensions={Mock()})


def _names(ros_distro):
    extension = RosDistroPackageDiscovery()
    args = Mock()
    args.ros_distro = ros_distro
    return {d.name for d in extension.discover(
        args=args, identification_extensions={})}


@requires_rep159
@pytest.mark.usefixtures('use_rep159_distro')
def test_discover_binary_import_skips_parent_packages():
    assert _names('bin_child') == {'bin_child_pkg', 'ros_workspace'}


@requires_rep159
@pytest.mark.usefixtures('use_rep159_distro')
def test_discover_source_rebuild_keeps_parent_packages():
    assert _names('src_child') == {
        'src_child_pkg', 'parent_pkg', 'ros_workspace'}


@requires_rep159
@pytest.mark.usefixtures('use_rep159_distro')
def test_discover_parent_unchanged():
    assert _names('parent') == {'parent_pkg', 'ros_workspace'}
