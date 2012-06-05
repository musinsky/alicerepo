# no debug info is generated
%global debug_package %{nil}

Name:		alice-xrootd
Version:	3.0.5
Release:	1%{?dist}
Summary:	Xroots for ALICE
Group:		System Environment/Daemons
License:	BSD
URL:		http://www.xrootd.org/
Source0:	xrootd-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-openssl libxml2-devel
Requires:	alice-openssl libxml2

# define alice dir sctucture
%define alice_dir /usr/cern/alice
%define openssl_dir %{alice_dir}/alice-openssl/0.9.8x
%define _prefix %{alice_dir}/%{name}/%{version}

%description
Xrootd for ALICE

%prep
%setup -q -n xrootd-%{version}

%build
export LD_LIBRARY_PATH="%{openssl_dir}/lib:$LD_LIBRARY_PATH"
./configure.classic --prefix=%{buildroot}%{_prefix} --with-ssl-incdir=%{openssl_dir}/include --with-ssl-libdir=%{openssl_dir}/lib \
  --enable-gsi --enable-secssl --no-arch-subdirs --disable-posix --disable-bonjour
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}%{_prefix}
rm -Rf %{buildroot}%{_prefix}/etc
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/include/xrootd


%changelog
