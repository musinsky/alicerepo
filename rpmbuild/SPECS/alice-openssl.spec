# ALICE specific
%define package_name openssl
%define alice_name alice-%{package_name}
%define alice_prefix /opt/cern/alice/%{alice_name}-%{version}
%define debug_package %{nil}

Name:           %{alice_name}
Version:        0.9.8x
Release:        2%{?dist}
Summary:        A general purpose cryptography library with TLS implementation
License:        OpenSSL
URL:            http://www.openssl.org/
Source:         http://www.openssl.org/source/%{package_name}-%{version}.tar.gz
Patch:          openssl-0.9.8-no-rpath.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
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
./config --prefix=%{alice_prefix} \
    shared zlib no-asm no-krb5
make

%install
rm -rf %{buildroot}
make INSTALL_PREFIX=%{buildroot} install_sw

# remove unnecessary files
rm -rf %{buildroot}/%{alice_prefix}/bin/
rm -rf %{buildroot}/%{alice_prefix}/ssl/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{alice_prefix}/*

%changelog
* Wed Jun 06 2012 Jan Musinsky <musinsky@gmail.com> 0.9.8x-2
- small changes

* Tue Jun 05 2012 Martin Vala <Martin.Vala@cern.ch> 0.9.8x-1
- packaged
