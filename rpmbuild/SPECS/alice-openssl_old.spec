# no debug info is generated
%global debug_package %{nil}

Name:		alice-openssl
Version:	0.9.8x
Release:	1%{?dist}
Summary:	Openssl for ALICE
Group:		System Environment/Libraries
License:	OpenSSL
URL:		http://www.openssl.org/
Source0:	openssl-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	coreutils, krb5-devel, perl, sed, zlib-devel, /usr/bin/cmp
BuildRequires:	/usr/bin/rename
Requires: coreutils, ca-certificates >= 2008-5

# define alice dir sctucture
%define alice_dir /usr/cern/alice
%define _prefix %{alice_dir}/%{name}/%{version}

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%prep
%setup -q -n openssl-%{version}

%build
./config --prefix=%{_prefix} --openssldir=%{_prefix} shared
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}/lib
cp libcrypto.so.* %{buildroot}%{_prefix}/lib/
cp libssl.so.* %{buildroot}%{_prefix}/lib/
MY_PWD=`pwd`
cd %{buildroot}%{_prefix}/lib/
ln -s libcrypto.so.0.9.8 libcrypto.so
ln -s libssl.so.0.9.8 libssl.so
cd $MY_PWD
mkdir -p %{buildroot}%{_prefix}/include/openssl
cp include/openssl/*.h %{buildroot}%{_prefix}/include/openssl/

#make install DESTDIR=%{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_prefix}/lib/*
%dir %{_prefix}/include/openssl
%attr(0644,root,root) %{_prefix}/include/openssl/*

%changelog
