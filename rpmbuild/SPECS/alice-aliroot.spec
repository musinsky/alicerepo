# no debug info is generated
%global debug_package %{nil}

# version
%define package_name aliroot-an

%define alice_package_version 5.04.34
%define	alice_fedora_rev 0
#deps versions
%define openssl_ver 0.9.8x
%define xrootd_ver 3.0.5
%define alien_ver 1.0.14n
%define root_ver 5.34.05
%define geant3_ver 1.14.8

%define alice_name alice-%{package_name}

%define alice_dir /opt/cern/alice
%define alice_prefix %{alice_dir}/%{package_name}/%{alice_package_version}
%define alice_env_module_dir %{alice_dir}/env_modules

# version and deps
%define openssl_dir %{alice_dir}/openssl/%{openssl_ver}
%define xrootd_dir %{alice_dir}/xrootd/%{xrootd_ver}
%define alien_dir %{alice_dir}/alien-client/%{alien_ver}
%define rootsys_dir %{alice_dir}/root/%{root_ver}
%define geant3_dir %{alice_dir}/geant3/%{geant3_ver}

Name:		%{alice_name}-%{alice_package_version}
Version:	0
Release:	%{alice_fedora_rev}%{?dist}
Summary:	AliRoot for ALICE
Group:		System Environment/Daemons
License:	LGPLv2+ 
URL:		http://aliceinfo.cern.ch/
Source0:	%{name}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	alice-environment-modules cmake subversion gcc-gfortran
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  glew-devel
BuildRequires:	alice-openssl-%{openssl_ver}
BuildRequires:	alice-xrootd-%{xrootd_ver}
BuildRequires:	alice-alien-client-%{alien_ver}
BuildRequires:	alice-root-%{root_ver}
BuildRequires:	alice-root-%{root_ver}-graf3d-eve
BuildRequires:	alice-root-%{root_ver}-genvector
BuildRequires:  alice-root-%{root_ver}-pythia6-single
BuildRequires:	alice-root-%{root_ver}-net-alien
#BuildRequires:	alice-root-%{root_ver}-xproof
#BuildRequires:	alice-root-%{root_ver}-proof-bench
#BuildRequires:	alice-root-%{root_ver}-proof-sessionviewer
#BuildRequires:	alice-root-%{root_ver}-proofd
BuildRequires:	alice-root-%{root_ver}-mathmore
BuildRequires:	alice-root-%{root_ver}-minuit2
BuildRequires:	alice-root-%{root_ver}-genvector
BuildRequires:  alice-root-%{root_ver}-io-xml
BuildRequires:  alice-root-%{root_ver}-mlp
BuildRequires:  alice-root-%{root_ver}-spectrum
BuildRequires:  alice-root-%{root_ver}-montecarlo-vmc
BuildRequires:	alice-geant3-%{geant3_ver}
Requires:	alice-environment-modules
Requires:	alice-root-%{root_ver}
Requires:	alice-root-%{root_ver}-net-alien
Requires:	alice-root-%{root_ver}-xproof
Requires:	alice-root-%{root_ver}-proof-bench
Requires:	alice-root-%{root_ver}-pythia6-single
Requires:	alice-root-%{root_ver}-proof-sessionviewer
Requires:	alice-root-%{root_ver}-proofd
Requires:	alice-root-%{root_ver}-mathmore
Requires:	alice-root-%{root_ver}-minuit2
Requires:	alice-root-%{root_ver}-genvector
Requires:       alice-root-%{root_ver}-montecarlo-vmc
Requires:       alice-root-%{root_ver}-tree-viewer
Requires:	alice-geant3-%{geant3_ver}

# define alice dir sctucture

%description
AliRoot for ALICE

%prep
%setup -q -n %{name}

%build
export ROOTSYS="%{rootsys_dir}"
export GEANT3="%{geant3_dir}"
export LD_LIBRARY_PATH="%{geant3_dir}/lib/tgt_$ALICE_TARGET:%{rootsys_dir}/lib:%{alien_dir}/lib:%{xrootd_dir}/lib:%{openssl_dir}/lib:$LD_LIBRARY_PATH"
export PATH="%{rootsys_dir}/bin:$PATH"
export ALICE_TARGET="$(root-config --arch)"
export ALICE_INSTALL="%{alice_prefix}"
export ALICE_ROOT="${PWD}"
export ALICE="$(dirname ${ALICE_ROOT})"
mkdir build
cd build
cmake $ALICE_ROOT
make %{?_smp_mflags}
cd %{_builddir}

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}/
export PATH="%{rootsys_dir}/bin:$PATH"
export ALICE_TARGET="$(root-config --arch)"

# creating pars
make par-all
mkdir -p %{buildroot}%{alice_prefix}/pars
mv *.par %{buildroot}%{alice_prefix}/pars/

# copy * from source (TODO copy only headers)
cd ../
rm -Rf build
cp -rf * %{buildroot}%{alice_prefix}

# create module file
mkdir -p %{buildroot}%{alice_prefix}/etc/modulefiles
cat > %{buildroot}%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} <<EOF
#%Module 1.0
# 
# AliRoot module for use with 'environment-modules' package:
# 
prepend-path            PATH            %{xrootd_dir}/bin
prepend-path            PATH            %{alien_dir}/bin
prepend-path            PATH            %{rootsys_dir}/bin
prepend-path            PATH            %{alice_prefix}/bin/tgt_$ALICE_TARGET
prepend-path            LD_LIBRARY_PATH %{openssl_dir}/lib
prepend-path            LD_LIBRARY_PATH %{xrootd_dir}/lib
prepend-path            LD_LIBRARY_PATH %{alien_dir}/lib
prepend-path            LD_LIBRARY_PATH %{rootsys_dir}/lib
prepend-path            LD_LIBRARY_PATH %{geant3_dir}/lib/tgt_$ALICE_TARGET
prepend-path            LD_LIBRARY_PATH %{alice_prefix}/lib/tgt_$ALICE_TARGET
setenv                  OPENSSL_DIR     %{openssl_dir}
setenv                  XROOTD_DIR      %{xrootd_dir}
setenv                  ALIEN_DIR       %{alien_dir}
setenv                  ROOTSYS         %{rootsys_dir}
setenv                  GEANT3          %{geant3_dir}
setenv                  ALICE_ROOT      %{alice_prefix}
setenv                  ALICE           %{alice_dir}
setenv                  ALICE_TARGET    $ALICE_TARGET
setenv                  X509_CERT_DIR   %{alien_dir}/share/certificates
setenv                  GSHELL_NO_GCC   1
setenv                  GSHELL_ROOT     %{alien_dir}
EOF

mkdir -p %{buildroot}/etc/modulefiles
cp %{buildroot}%{alice_prefix}/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch} %{buildroot}/etc/modulefiles/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{alice_prefix}
#%{alice_prefix}/bin
#%{alice_prefix}/lib
#%{alice_prefix}/include
#%{alice_prefix}/etc
#%{alice_prefix}/data
#%{alice_prefix}/ANALYSIS
#%{alice_prefix}/EVE
#%{alice_prefix}/FMD
#%{alice_prefix}/LHAPDF
#%{alice_prefix}/MUON
#%{alice_prefix}/OADB
#%{alice_prefix}/OCDB
#%{alice_prefix}/PHOS
#%{alice_prefix}/PWGCF
#%{alice_prefix}/PWGGA
#%{alice_prefix}/PWGHF
#%{alice_prefix}/PWGLF
#%{alice_prefix}/PWGPP
#%{alice_prefix}/QAref
#%{alice_prefix}/TOF
#%{alice_prefix}/TPC
/etc/modulefiles/%{alice_name}-%{alice_package_version}-%{_arch}

%changelog
* Mon Jun 11 2012 Martin Vala <Martin.Vala@cern.ch> - 5.03.29-2
- Added proofd dep

* Mon Jun 11 2012 Martin Vala <Martin.Vala@cern.ch> - 5.03.29-1
- First alice version
