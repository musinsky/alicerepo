%define alice_package_version 0.9.8x

# ALICE specific
%define package_name openssl
%define alice_name alice-%{package_name}

%define alice_dir /opt/cern/alice
%define alice_prefix %{alice_dir}/%{package_name}/%{alice_package_version}
%define alice_env_module_dir %{alice_dir}/env_modules

%define debug_package %{nil}

Name:           %{alice_name}-%{alice_package_version}
Version:        0
Release:        0%{?dist}
Summary:        A general purpose cryptography library with TLS implementation
License:        OpenSSL
URL:            http://www.openssl.org/
Source:         http://www.openssl.org/source/%{package_name}-%{alice_package_version}.tar.gz
Patch:          openssl-0.9.8-no-rpath.patch
BuildRequires:  coreutils, perl, sed, zlib-devel
Requires:       alice-environment-modules coreutils

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

ALICE notes: needed only libcrypto.so, libssl.so and include dir

%prep
%setup -q -n %{package_name}-%{alice_package_version}
%patch -p1 -b .no-rpath

%build
./config --prefix=%{alice_prefix} shared
make # don't use _smp_mflags (parallel make)

%install
make INSTALL_PREFIX=%{buildroot} install_sw

# remove unnecessary files
rm -rf %{buildroot}/%{alice_prefix}/{bin,ssl}
rm -rf %{buildroot}/%{alice_prefix}/lib/*.a

mkdir -p %{buildroot}/%{alice_prefix}/etc/modulefiles
cat > %{buildroot}/%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} <<EOF
#%Module 1.0
# 
# alice-openssl module for use with 'environment-modules' package:
# 
prepend-path            LD_LIBRARY_PATH %{alice_prefix}/lib
setenv                  OPENSSL_DIR     %{alice_prefix}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{alice_prefix}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Thu Jun 07 2012 Martin Vala <Martin.Vala@cern.ch> 0.9.8x-4
- removed ld.so.conf.d
- package directory structure changed

* Thu Jun 07 2012 Jan Musinsky <musinsky@gmail.com> 0.9.8x-3
- resolve problem with Rpath and improvements

* Wed Jun 06 2012 Jan Musinsky <musinsky@gmail.com> 0.9.8x-2
- small changes

* Tue Jun 05 2012 Martin Vala <Martin.Vala@cern.ch> 0.9.8x-1
- packaged
