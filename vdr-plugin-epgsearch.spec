
%define plugin	epgsearch
%define name	vdr-plugin-%plugin
%define version	0.9.24
%define prever	0
%define rel	4

Summary:	VDR plugin: search the EPG for repeats and more
Name:		%name
Version:	%version
%if %prever
Release:	%mkrel 0.%prever.%rel
%else
Release:	%mkrel %rel
%endif
Group:		Video
License:	GPL+
URL:		http://winni.vdr-developer.org/epgsearch/index_eng.html
%if %prever
Source:		vdr-%plugin-%version.%prever.tgz
%else
Source:		http://winni.vdr-developer.org/epgsearch/downloads/vdr-%plugin-%version.tgz
%endif
Patch0:		epgsearch-includes.patch
Patch1:		epgsearch-const-char-gcc4.4.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0-7
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
%if %prever
%setup -q -n %plugin-%version.%prever
%else
%setup -q -n %plugin-%version
%endif
%patch0 -p1
%patch1 -p1
%vdr_plugin_prep

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
# -DUSE_PINPLUGIN does not work with current pin patch
VDR_PLUGIN_EXTRA_FLAGS="-DUSE_GRAPHTFT"
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



%changelog
* Tue Jul 28 2009 Anssi Hannula <anssi@mandriva.org> 0.9.24-4mdv2010.0
+ Revision: 402763
- enable graphtft support

* Tue Jul 28 2009 Anssi Hannula <anssi@mandriva.org> 0.9.24-3mdv2010.0
+ Revision: 401088
- rebuild for new VDR
- adapt for vdr compilation flags handling changes, bump buildrequires
- fix build with gcc4.4 (const-char-gcc4.4.patch partially from upstream)

* Sat Mar 21 2009 Anssi Hannula <anssi@mandriva.org> 0.9.24-2mdv2009.1
+ Revision: 359704
- fix includes (includes.patch)
- rebuild for new vdr

* Sun May 11 2008 Anssi Hannula <anssi@mandriva.org> 0.9.24-1mdv2009.0
+ Revision: 205449
- new version

* Mon Apr 28 2008 Anssi Hannula <anssi@mandriva.org> 0.9.24-0.rc1.2mdv2009.0
+ Revision: 197924
- rebuild for new vdr

* Sat Apr 26 2008 Anssi Hannula <anssi@mandriva.org> 0.9.24-0.rc1.1mdv2009.0
+ Revision: 197659
- 0.9.24-rc1
- add vdr_plugin_prep
- bump buildrequires on vdr-devel

* Fri Jan 04 2008 Anssi Hannula <anssi@mandriva.org> 0.9.23-3mdv2008.1
+ Revision: 145083
- rebuild for new vdr
- adapt for changed vdr optflags scheme

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 29 2007 Anssi Hannula <anssi@mandriva.org> 0.9.23-2mdv2008.1
+ Revision: 103089
- rebuild for new vdr

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 0.9.23-1mdv2008.0
+ Revision: 81919
- 0.9.23
- update URL
- build with pin plugin support
- adapt license tag to the new policy

* Sun Jul 08 2007 Anssi Hannula <anssi@mandriva.org> 0.9.21-5mdv2008.0
+ Revision: 49995
- rebuild for new vdr

* Sun Jul 08 2007 Anssi Hannula <anssi@mandriva.org> 0.9.21-4mdv2008.0
+ Revision: 49908
- provide services.h in epgsearch-devel subpackage

* Thu Jun 21 2007 Anssi Hannula <anssi@mandriva.org> 0.9.21-3mdv2008.0
+ Revision: 42081
- rebuild for new vdr

* Sat May 05 2007 Anssi Hannula <anssi@mandriva.org> 0.9.21-2mdv2008.0
+ Revision: 22748
- rebuild for new vdr

* Tue May 01 2007 Anssi Hannula <anssi@mandriva.org> 0.9.21-1mdv2008.0
+ Revision: 19868
- 0.9.21
- provide more scripts in bindir


* Fri Mar 02 2007 Anssi Hannula <anssi@mandriva.org> 0.9.20-1mdv2007.0
+ Revision: 130878
- 0.9.20

* Tue Dec 05 2006 Anssi Hannula <anssi@mandriva.org> 0.9.19-2mdv2007.1
+ Revision: 90916
- rebuild for new vdr

* Fri Nov 03 2006 Anssi Hannula <anssi@mandriva.org> 0.9.19-1mdv2007.1
+ Revision: 76359
- 0.9.19
- update filelist and configuration file

* Tue Oct 31 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17d-5mdv2007.1
+ Revision: 73996
- rebuild for new vdr
- Import vdr-plugin-epgsearch

* Thu Sep 07 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17d-4mdv2007.0
- rebuild for new vdr

* Fri Aug 25 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17d-3mdv2007.0
- fix mangled description

* Thu Aug 24 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17d-2mdv2007.0
- stricter abi requires

* Wed Aug 09 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17d-1mdv2007.0
- 0.9.17d

* Mon Aug 07 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17c-3mdv2007.0
- rebuild for new vdr

* Wed Jul 26 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17c-2mdv2007.0
- rebuild for new vdr

* Tue Jul 11 2006 Anssi Hannula <anssi@mandriva.org> 0.9.17c-1mdv2007.0
- initial Mandriva release

