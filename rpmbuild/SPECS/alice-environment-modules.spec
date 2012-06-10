%define package_name environment-modules
%define alice_name alice-%{package_name}
%define alice_package_version 1.0.0

Name:		%{alice_name}
Version:	%{alice_package_version}
Release:	1%{?dist}
Summary:	Virtual env package for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+
URL:		http://alicepc104.jinr.ru
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	environment-modules
Requires:	environment-modules

%description
Virtual env package for ALICE

%prep
#%setup -q -n xrootd-%{version}

%build

%install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%changelog
