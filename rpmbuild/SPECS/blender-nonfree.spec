%global blender_api 2.63

# [Fedora] Turn off the brp-python-bytecompile script 
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%global blenderlib  %{_datadir}/blender/%{blender_api}
%global blenderarch %{_libdir}/blender/%{blender_api}
%global __python %{__python3}

%global fontname blender

Name:           blender-nonfree
Epoch:		1
Version:        %{blender_api}a
Release: 	4%{?dist}

Summary:        3D modeling, animation, rendering and post-production

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://www.blender.org

Source0:	http://download.blender.org/source/blender-%{version}.tar.gz
Source1:	blenderplayer.1
Source5:        blender.xml

Source10:	macros.blender

Patch1:		blender-2.44-bid.patch
Patch2:		blender-2.63-syspath.patch

Patch4:		blender-2.48-undefine-operation.patch
Patch5:		blender-2.50-uninit-var.patch

Patch10:	blender-2.58-python_include.patch
Patch11: 	blender-2.61-openjpeg_stdbool.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  python3-devel >= 3.2
BuildRequires:  cmake
BuildRequires:  SDL-devel
BuildRequires:	expat-devel
BuildRequires:  pcre-devel
BuildRequires:  libxml2-devel
BuildRequires:  boost-devel

# Compression stuff
BuildRequires:	xz-devel
BuildRequires:  zlib-devel

BuildRequires:  libXi-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  freetype-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  glew-devel
BuildRequires:  freeglut-devel

BuildRequires:	fftw-devel
BuildRequires:	ftgl-devel
BuildRequires:	ode-devel
BuildRequires:	openjpeg-devel
BuildRequires:  qhull-devel

# Picture/Vidoe stuff
BuildRequires:  libjpeg-devel
BuildRequires:  openjpeg-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:  libogg-devel
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:	OpenImageIO-devel

# Audio stuff
BuildRequires:	libsamplerate-devel
BuildRequires:  libao-devel
BuildRequires:  libsndfile-devel
BuildRequires:  esound-devel
BuildRequires:	freealut-devel
BuildRequires:	jack-audio-connection-kit-devel

BuildRequires:	openCOLLADA-devel >= svn825

BuildRequires:  libspnav-devel

BuildRequires:  ffmpeg-devel
BuildRequires:  faac-devel
BuildRequires:  x264-devel
BuildRequires:  xvidcore-devel
BuildRequires:  faad2-devel
BuildRequires:  lame-devel

# mvala
Requires:       ffmpeg-libs
Requires:       faac
Requires:       blender%{?_isa} = %{epoch}:%{version}-%{release}
#Requires:       blender-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
# end mvala

Provides:	  blender(ABI) = %{blender_api}

#Provides:	  blender-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
#Obsoletes:	  blender-fonts <= 2.48a-9

%description
Blender is the essential software solution you need for 3D, from modeling,
animation, rendering and post-production to interactive creation and playback.

Professionals and novices can easily and inexpensively publish stand-alone,
secure, multi-platform content to the web, CD-ROMs, and other media.

%prep
%setup -q -n blender-%{version}
%patch1 -p1 -b .bid
%patch2 -p1 -b .syspath

%patch4 -p0
%patch5 -p0

%patch10 -p1
%patch11 -p1 -b .openjpeg_stdbool

find -name '.svn' -print | xargs rm -rf

%build
mkdir cmake-make
cd cmake-make
export CFLAGS="$RPM_OPT_FLAGS -fPIC -funsigned-char -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%ifnarch %{ix86} x86_64
  -DWITH_RAYOPTIMIZATION=OFF \
%endif
 -DCMAKE_SKIP_RPATH=ON \
 -DBUILD_SHARED_LIBS=OFF \
 -DWITH_FFTW3:BOOL=ON \
 -DWITH_JACK:BOOL=ON \
 -DWITH_CODEC_SNDFILE:BOOL=ON \
 -DWITH_IMAGE_OPENJPEG:BOOL=ON \
 -DWITH_OPENCOLLADA:BOOL=ON \
 -DWITH_PYTHON:BOOL=ON \
 -DWITH_PYTHON_INSTALL:BOOL=OFF \
 -DWITH_CODEC_FFMPEG:BOOL=ON \
 -DWITH_GAMEENGINE:BOOL=ON \
 -DWITH_CXX_GUARDEDALLOC:BOOL=OFF \
 -DWITH_BUILTIN_GLEW=ON \
 -DWITH_INSTALL_PORTABLE=OFF \
 -DWITH_PYTHON_SAFETY=ON \
 -DWITH_PYTHON_MODULE=OFF \
 -DWITH_PLAYER=ON \
 -DWITH_MOD_OCEANSIM=ON

make -j5
cd ..

install -d release/plugins/include
install -m 644 source/blender/blenpluginapi/*.h release/plugins/include

chmod +x release/plugins/bmake

make -C release/plugins/

%install
cd cmake-make
#make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp bin/blender ${RPM_BUILD_ROOT}%{_bindir}/blender-nonfree
cd ..
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/applications/
#cp release/freedesktop/blender.desktop ${RPM_BUILD_ROOT}%{_datadir}/applications/blender-nonfree.desktop

cat << 'EOF' > ${RPM_BUILD_ROOT}%{_datadir}/applications/blender-nonfree.desktop
[Desktop Entry]
Name=Blender (Non Free)
GenericName=3D modeller
GenericName[es]=modelador 3D
GenericName[de]=3D-Modellierer
GenericName[fr]=modeleur 3D
GenericName[ru]=Редактор 3D-моделей
Comment=3D modeling, animation, rendering and post-production
Comment[es]=modelado 3D, animación, renderizado y post-producción
Comment[de]=3D-Modellierung, Animation, Rendering und Nachbearbeitung
Exec=blender-nonfree
Icon=blender
Terminal=false
Type=Application
Categories=Graphics;3DGraphics;
MimeType=application/x-blender;
EOF
%post
%postun
%files
%defattr(-,root,root,-)
%{_bindir}/blender-nonfree
%{_datadir}/applications/blender-nonfree.desktop

%changelog
