# no debug info is generated
%global debug_package %{nil}

Name:		alice-geant3
Version:	1.14.2
Release:	1%{?dist}
Summary:	Geant3 for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+ 
URL:		http://root.cern.ch/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-root
Requires:	alice-root

# define alice dir sctucture
%define alice_dir /usr/cern/alice
%define rootsys_dir %{alice_dir}/alice-root/5.33.02b
%define _prefix %{alice_dir}/%{name}/%{version}

%description
AliEn for ALICE

%prep
%setup -q -n %{name}-%{version}

%build
export ROOTSYS="%{rootsys_dir}"
export LD_LIBRARY_PATH="%{rootsys_dir}/lib:$LD_LIBRARY_PATH"
export PATH="%{rootsys_dir}/bin:$PATH"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
G3TARGET=`root-config --arch`
mkdir -p %{buildroot}%{_prefix}/lib/tgt_$G3TARGET %{buildroot}%{_prefix}/TGeant3

cp lib/tgt_$G3TARGET/*.so %{buildroot}%{_prefix}/lib/tgt_$G3TARGET/
cp TGeant3/*.h %{buildroot}%{_prefix}/TGeant3/
cp -rf geant321 %{buildroot}%{_prefix}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/lib
%{_prefix}/TGeant3
%{_prefix}/geant321

%changelog
