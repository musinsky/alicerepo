# no debug info is generated
%global debug_package %{nil}

# version
%define alice_package_version 1.14.2

#deps versions
%define openssl_ver 0.9.8x
%define xrootd_ver 3.0.5
%define alien_ver 1.0.14n
%define root_ver 5.33.02b


%define package_name geant3
%define alice_name alice-%{package_name}

%define alice_dir /opt/cern/alice
%define alice_prefix %{alice_dir}/%{package_name}/%{version}
%define alice_env_module_dir %{alice_dir}/env_modules

# deps
%define openssl_dir %{alice_dir}/openssl/%{openssl_ver}
%define xrootd_dir %{alice_dir}/xrootd/%{xrootd_ver}
%define alien_dir %{alice_dir}/alien/%{alien_ver}
%define rootsys_dir %{alice_dir}/root/%{root_ver}



Name:		%{alice_name}
Version:	%{alice_package_version}
Release:	1%{?dist}
Summary:	Geant3 for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+ 
URL:		http://root.cern.ch/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alice-root%{?_isa} = %{root_ver}
Requires:	alice-environment-modules
#Requires:	alice-root%{?_isa} = %{root_ver}

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
mkdir -p %{buildroot}%{alice_prefix}
PATH="%{rootsys_dir}/bin:$PATH"
G3TARGET=`root-config --arch`
mkdir -p %{buildroot}%{alice_prefix}/lib/tgt_$G3TARGET %{buildroot}%{alice_prefix}/TGeant3

cp lib/tgt_$G3TARGET/*.so %{buildroot}%{alice_prefix}/lib/tgt_$G3TARGET/
cp TGeant3/*.h %{buildroot}%{alice_prefix}/TGeant3/
cp -rf geant321 %{buildroot}%{alice_prefix}/

mkdir -p %{buildroot}%{alice_prefix}/etc/modulefiles
cat > %{buildroot}%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} <<EOF
#%Module 1.0
#
# AliRoot module for use with 'environment-modules' package:
#
prepend-path            PATH            %{xrootd_dir}/bin
prepend-path            PATH            %{alien_dir}/bin
prepend-path            PATH            %{rootsys_dir}/binalice_arch
prepend-path            LD_LIBRARY_PATH %{openssl_dir}/lib
prepend-path            LD_LIBRARY_PATH %{xrootd_dir}/lib
prepend-path            LD_LIBRARY_PATH %{alien_dir}/lib
prepend-path            LD_LIBRARY_PATH %{rootsys_dir}/lib
prepend-path            LD_LIBRARY_PATH %{geant3_dir}/lib/tgt_$ALICE_TARGET
setenv                  X509_CERT_DIR   %{alien_dir}/share/certificates
setenv                  GSHELL_NO_GCC   1
setenv                  GSHELL_ROOT     %{alien_dir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{alice_prefix}/lib
%{alice_prefix}/TGeant3
%{alice_prefix}/geant321
%{alice_prefix}/etc

%changelog
