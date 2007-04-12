
%define plugin	epgsearch
%define name	vdr-plugin-%plugin
%define version	0.9.20
%define rel	1

Summary:	VDR plugin: search the EPG for repeats and more
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPL
URL:		http://people.freenet.de/cwieninger/html/vdr-epg-search__english_.html
Source:		http://people.freenet.de/cwieninger/vdr-%plugin-%version.tar.bz2
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
%vdr_plugin_build

%install
rm -rf %{buildroot}
%vdr_plugin_install

make install-doc MANDIR=%{buildroot}%{_mandir}

install -d -m755 %{buildroot}%{_bindir}
install -m755 scripts/sendEmail.pl %{buildroot}%{_bindir}

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
%{_bindir}/sendEmail.pl
%{_mandir}/man1/createcats.1*
%{_mandir}/man1/epgsearch.1*
%{_mandir}/man4/epgsearch.4*
%{_mandir}/man5/epgsearch*.5*
%{_mandir}/man5/noannounce.conf.5*
%{_mandir}/man5/timersdone.conf.5*
%lang(de) %{_mandir}/de


