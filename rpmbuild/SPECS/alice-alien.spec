# no debug info is generated
%global debug_package %{nil}

Name:		alice-alien
Version:	1.0.14n
Release:	1%{?dist}
Summary:	AliEn for ALICE
Group:		System Environment/Daemons
License:	BSD
URL:		http://www.xrootd.org/
Source0:	xrootd-xalienfs-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-xrootd autoconf libtool chrpath
Requires:	alice-xrootd

# define alice dir sctucture
%define alice_dir /usr/cern/alice
%define xrootd_dir %{alice_dir}/alice-xrootd/3.0.5
%define _prefix %{alice_dir}/%{name}/%{version}

%description
AliEn for ALICE

%prep
%setup -q -n xrootd-xalienfs-%{version}

%build
#export LD_LIBRARY_PATH="%{openssl_dir}/lib:$LD_LIBRARY_PATH"
rm -Rf autom4te.cache
./bootstrap.sh
./configure --prefix=%{_prefix} \
    --with-certificate-directory=%{_prefix}/share \
    --with-xrootd-location=%{xrootd_dir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
chrpath --delete %{buildroot}%{_prefix}/bin/gcp
chrpath --delete %{buildroot}%{_prefix}/bin/gprepare
chrpath --delete %{buildroot}%{_prefix}/bin/gbbox
chrpath --delete %{buildroot}%{_prefix}/bin/gsubmit
chrpath --delete %{buildroot}%{_prefix}/bin/gps
chrpath --delete %{buildroot}%{_prefix}/bin/gisonline
chrpath --delete %{buildroot}%{_prefix}/bin/gshell
chrpath --delete %{buildroot}%{_prefix}/bin/gstage
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/include
%{_prefix}/share
%{_prefix}/etc

%changelog
