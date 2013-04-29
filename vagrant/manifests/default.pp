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

package { 'python-pip':
    ensure => present,
}

if $operatingsystem == 'Fedora' {
    file { "/usr/bin/pip":
        ensure => link,
        target => "/usr/bin/pip-python",
        require => Package["python-pip"],
        before => Package["evernote"],
    }
}

package { "evernote":
    ensure => latest,
    provider => pip,
    require => Package["python-pip"],
}

vcsrepo { "/opt/EN-LinuxClipper":
    ensure   => latest,
    owner    => vagrant,
    group    => vagrant,
    provider => git,
    require  => [ Package["git"] ],
    source   => "https://github.com/YakindanEgitim/EN-LinuxClipper.git",
    revision => 'devel',
    before   => [ File["/usr/bin/en-clipper"], File["/opt/EN-LinuxClipper/en-linuxclipper/core.py"] ],
}

file { "/usr/bin/en-clipper":
    ensure => link,
    target => "/opt/EN-LinuxClipper/en-linuxclipper/core.py",
}

file { "/opt/EN-LinuxClipper/en-linuxclipper/core.py":
    ensure => file,
    mode => 0755,
}

file { "/usr/share/icons/hicolor/64x64/apps/everpad-mono.png":
    ensure => file,
    source => "/vagrant/everpad-mono.png",
}
