# ALICE specific
%define package_name openssl
%define alice_name alice-%{package_name}
%define alice_prefix /opt/cern/alice/%{alice_name}-%{version}
%define debug_package %{nil}

Name:           %{alice_name}
Version:        0.9.8x
Release:        4%{?dist}
Summary:        A general purpose cryptography library with TLS implementation
License:        OpenSSL
URL:            http://www.openssl.org/
Source:         http://www.openssl.org/source/%{package_name}-%{version}.tar.gz
Patch:          openssl-0.9.8-no-rpath.patch
BuildRequires:  coreutils, perl, sed, zlib-devel
Requires:       coreutils

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

ALICE notes: needed only libcrypto.so, libssl.so and include dir

%prep
%setup -q -n %{package_name}-%{version}
%patch -p1 -b .no-rpath

%build
./config --prefix=%{alice_prefix} shared
make # don't use _smp_mflags (parallel make)

%install
make INSTALL_PREFIX=%{buildroot} install_sw

# remove unnecessary files
rm -rf %{buildroot}/%{alice_prefix}/{bin,ssl}

%files
%defattr(-,root,root,-)
%{alice_prefix}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Thu Jun 07 2012 Jan Musinsky <musinsky@gmail.com> 0.9.8x-4
- removed ld.so.conf.d

* Thu Jun 07 2012 Jan Musinsky <musinsky@gmail.com> 0.9.8x-3
- resolve problem with Rpath and improvements

* Wed Jun 06 2012 Jan Musinsky <musinsky@gmail.com> 0.9.8x-2
- small changes

* Tue Jun 05 2012 Martin Vala <Martin.Vala@cern.ch> 0.9.8x-1
- packaged
