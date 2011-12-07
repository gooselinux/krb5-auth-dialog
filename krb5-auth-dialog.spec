%define libgnomeui_version 2.9.1
%define krb5_version 1.4
%define libnm_version 0.5
%define dbus_version 0.90

Summary: Kerberos 5 authentication dialog
Name: krb5-auth-dialog
Version: 0.13
Release: 3%{?dist}
License: GPLv2+
Group: User Interface/X
URL: https://honk.sigxcpu.org/piki/projects/krb5-auth-dialog/
Source0: http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: krb5-devel >= %{krb5_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: perl-XML-Parser, gettext
BuildRequires: intltool
BuildRequires: libnotify-devel
BuildRequires: gnome-doc-utils
%ifnarch s390 s390x
BuildRequires: NetworkManager-glib-devel >= %{libnm_version}
%endif
Requires: libgnomeui >= %{libgnomeui_version}
Requires: krb5-libs >= %{krb5_version}
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

# https://bugzilla.gnome.org/show_bug.cgi?id=599725
Patch0: seriesid-clash.patch

%description
This package contains a dialog that warns the user when their Kerberos
tickets are about to expire and lets them renew them.

%prep
%setup -q
%patch0 -p1 -b .seriesid

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %name.lang
%defattr(-,root,root,-)
%doc
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/krb5-auth-dialog*
%{_datadir}/krb5-auth-dialog/
%{_datadir}/applications/krb5-auth-dialog-preferences.desktop
%{_datadir}/dbus-1/services/org.gnome.KrbAuthDialog.service
%{_datadir}/icons/hicolor/*/*/*
%{_mandir}/man1/*
%{_sysconfdir}/xdg/autostart/krb5-auth-dialog.desktop


%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
        %{_sysconfdir}/gconf/schemas/krb5-auth-dialog.schemas >/dev/null || :
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :


%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/krb5-auth-dialog.schemas &> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/krb5-auth-dialog.schemas &> /dev/null || :
fi

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%changelog
* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.13-3
- Update icon caches
Resolves: #609270

* Tue Oct 27 2009 Matthias Clasen <mclasen@redhat.com> - 0.13-2
- Fix a clash with the help file seriesid

* Wed Oct 21 2009 Matěj Cepl <mcepl@redhat.com> - 0.13-1
- New upstream release (fixes #530001)

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 0.12-2
- Fix the preferences dialog

* Sat Aug 29 2009 Matthias Clasen <mclasen@redhat.com> - 0.12-1
- Update to 0.12
- Rebuild against new libnm_glib

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Matěj Cepl <mcepl@redhat.com> - 0.10-1
- Catch up with upstream release again.

* Thu Apr 23 2009 Matthias Clasen <mclasen@redhatcom> - 0.8-4
- Don't show bubbles before the icon is there
- Use the same invisible char as the rest of the world

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Colin Walters <walters@verbum.org> - 0.8-2
- BR notify, pointed out by Bojan Smojver <bojan@rexursive.com>

* Tue Jan 13 2009 Colin Walters <walters@verbum.org> - 0.8-1
- New upstream release
- Remove both patches; they are upstreamed
- Add gconf spec goo
- Add new stuff to files list

* Mon Feb 18 2008 Christopher Aillon <caillon@redhat.com> - 0.7-7
- Rebuild to celebrate my birthday (and GCC 4.3)

* Thu Nov  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.7-6
- Fix the Comment field in the desktop file (#344351)

* Mon Oct 22 2007 Christopher Aillon <caillon@redhat.com> - 0.7-5
- Don't start multiple times in KDE (#344991)

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 0.7-4
- Rebuild for build ID

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> 0.7-3
- Update the license tag

* Thu Mar 15 2007 Karsten Hopp <karsten@redhat.com> 0.7-2
- rebuild with current gtk2 to add png support (#232013)

* Mon Jul 24 2006 Christopher Aillon <caillon@redhat.com> - 0.7-1
- Update to 0.7
- Don't peg the network and CPU when the KDC is unavailable

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.6.cvs20060212-4
- rebuild for dbus 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.cvs20060212-3.1
- rebuild

* Sat Jun 24 2006 Jesse Keating <jkeating@redhat.com> - 0.6.cvs20060212-3
- Add missing BRs perl-XML-Parser, gettext
- Work around no network manager stuff on z900s

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> - 0.6.cvs20060212-1
- Update to latest CVS to get some of Nalin's fixes

* Tue Feb  7 2006 Jesse Keating <jkeating@redhat.com> - 0.6-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> 0.6-1
- Update to 0.6, adding an autostart file

* Fri Dec  9 2005 Jesse Keating <jkeating@redhat.com> - 0.5-2.1
- rebuilt

* Thu Dec  1 2005 John (J5) Palmieri <johnp@redhat.com> - 0.5-2
- rebuild for new dbus

* Tue Nov  8 2005 Christopher Aillon <caillon@redhat.com> 0.5-1
- Update to 0.5

* Tue Nov  1 2005 Christopher Aillon <caillon@redhat.com> 0.4-1
- Update to 0.4

* Mon Oct 31 2005 Christopher Aillon <caillon@redhat.com> 0.3-1
- Update to 0.3, working with newer versions of krb5 and NetworkManager

* Tue Aug 16 2005 David Zeuthen <davidz@redhat.com>
- Rebuilt

* Tue Mar 22 2005 Nalin Dahyabhai <nalin@redhat.com> 0.2-5
- Change Requires: krb5 to krb5-libs, repeat $ -> % fix for build requirements.

* Tue Mar 22 2005 Dan Williams <dcbw@redhat.com> 0.2-4
- Fix $ -> % for Requires: krb5 >= ...

* Mon Mar 21 2005 David Zeuthen <davidz@redhat.com> 0.2-3
- Fix up BuildRequires and Requires (#134704)

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> 0.2-2
- Rebuild

* Mon Aug 16 2004 GNOME <jrb@redhat.com> - auth-dialog
- Initial build.

