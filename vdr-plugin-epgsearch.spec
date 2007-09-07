
%define plugin	epgsearch
%define name	vdr-plugin-%plugin
%define version	0.9.23
%define rel	1

Summary:	VDR plugin: search the EPG for repeats and more
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPL+
URL:		http://winni.vdr-developer.org/epgsearch/index_eng.html
Source:		http://winni.vdr-developer.org/epgsearch/downloads/vdr-%plugin-%version.tgz
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.4.1-6
Requires:	vdr-abi = %vdr_abi

%description
EPG-Search can be used as a replacement for the default schedules
menu entry. It looks like the standard schedules menu, but adds some
additional functions:
- Commands for EPG entries with 5 built-in commands like 'show repeats',
  'create search'. One can add own commands for other needs, like adding a
  VDRAdmin auto-timer.
- Add up to 4 user-defined times to 'now' and 'next'
- Searching the EPG: Create reusable queries, which can also be used
  as 'search timers'.
- Search timers: Search for broadcasts in the background and add a
  timer if one matches (similar to VDRAdmin's auto-timers) or simply
  make an announcement about it via OSD
- Avoid double recordings of the same event
  * timer preview
  * recognition of broken recordings
  * fuzzy event comparison
- Progress bar in 'What's on now' and 'What's on next'
- Shift the time displayed by keypress, e.g. 'What's on now' + 30 minutes
- Start menu can be setup between 'Schedule' or 'What's on now'
- background check for timer conflicts with a timer conflict manager
- detailed epg menu (summary) allows jumping to the next/previous
  event
- support for extended EPG info for search timers
- extension of the timer edit menu with a directory item, user
  defined weekday selection and a subtitle completion.

%package -n %plugin-devel
Summary:	Development headers of epgsearch VDR plugin
Group:		Development/C++
Requires:	vdr-devel

%description -n %plugin-devel
Headers for developing plugins that will use services provided by
epgsearch.

%prep
%setup -q -n %plugin-%version

chmod -x scripts/*.conf

%vdr_plugin_params_begin %plugin
# the path to svdrpsend.pl for external
# SVDRP communitcation (default is internal
# communication)
var=SVDRPSENDCMD
param=--svdrpsendcmd=SVDRPSENDCMD
# config dir for epgsearch
var=CONFIGDIR
param=--config=CONFIGDIR
# logfile for epgsearch
var=LOGFILE
param=--logfile=LOGFILE
# logfile verbosity
var=LOGLEVEL
param=--verbose=LOGLEVEL
# reload epgsearchmenu.conf with plugin call
var=RELOADMENUCONF
param=--reloadmenuconf
# path to an alternative mail script for mail notification
var=MAILCMD
param=--mailcmd=MAILCMD
%vdr_plugin_params_end

%build
# -DUSE_GRAPHTFT needs alpha version of graphtft
%define vdr_add_optflags -DUSE_PINPLUGIN
%vdr_plugin_build

%install
rm -rf %{buildroot}
%vdr_plugin_install

make install-doc MANDIR=%{buildroot}%{_mandir}

install -d -m755 %{buildroot}%{_bindir}
install -m755 scripts/*.pl %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_includedir}/vdr/%{plugin}
install -m644 services.h %{buildroot}%{_includedir}/vdr/%{plugin}

cat %plugin.vdr conflictcheckonly.vdr epgsearchonly.vdr quickepgsearch.vdr > combined.vdr

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f combined.vdr
%defattr(-,root,root)
%doc README* HISTORY* MANUAL* doc conf scripts
%{_bindir}/autotimer2searchtimer.pl
%{_bindir}/convert_epgsearchdone_data.pl
%{_bindir}/convert_info_vdr.pl
%{_bindir}/sendEmail.pl
%{_mandir}/man1/createcats.1*
%{_mandir}/man1/epgsearch.1*
%{_mandir}/man4/epgsearch.4*
%{_mandir}/man5/epgsearch*.5*
%{_mandir}/man5/noannounce.conf.5*
%{_mandir}/man5/timersdone.conf.5*
%lang(de) %{_mandir}/de

%files -n %plugin-devel
%defattr(-,root,root)
%{_includedir}/vdr/%{plugin}

