case $::osfamily {
    Debian: {
        $cairo_pkg_name   = [ 'python-cairo' ]
        $gi_pkg_name   = [ 'python-gi' ]
    }
    RedHat: {
        $cairo_pkg_name   = [ 'pycairo' ]
        $gi_pkg_name   = [ 'pygobject3' ]
    }
}

package { 'cairo':
    ensure => present,
    name   => $cairo_pkg_name,
}

package { 'gi':
    ensure => present,
    name   => $gi_pkg_name,
}

package { 'git':
    ensure => present,
}

package { 'python-oauth2':
    ensure => present,
}

package { 'python-distutils-extra':
    ensure => present,
}

vcsrepo { "/tmp/EN-LinuxClipper":
    ensure   => latest,
    owner    => vagrant,
    group    => vagrant,
    provider => git,
    require  => [ Package["git"] ],
    source   => "https://github.com/YakindanEgitim/EN-LinuxClipper.git",
    revision => 'devel',
}

exec { "enlinuxclipper":
    command => "/usr/bin/env python setup.py install",
    cwd => "/tmp/EN-LinuxClipper",
    refreshonly => true,
    require => [ Package["python-distutils-extra"] ],
    subscribe => [ Vcsrepo["/tmp/EN-LinuxClipper"] ],
}
