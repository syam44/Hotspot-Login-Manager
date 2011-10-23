#
# hotspot-login-manager
# https://github.com/syam44/Hotspot-Login-Manager
#
# Distributed under the GNU General Public License version 3
# https://www.gnu.org/copyleft/gpl.html
#
# Authors: syam (aks92@free.fr)
#
# Description: makefile for easier command-line interaction
#


#
# Display available targets
#
.PHONY: usage
usage:
	@echo "Targets:"
	@echo "    install     Install hooks and configuration files."
	@echo "    uninstall   Uninstall hooks only, keep configuration files around."
	@echo "    purge       Uninstall hooks and DELETE configuration files."
	@echo
	@echo "    all         Make all project files: version, i18n-pot, i18n-mo, build"
	@echo "    clean       Clean intermediary files."
	@echo "    build       Rebuild intermediary files."
	@echo
	@echo "    i18n-mo     Generate .mo catalog files (program translations) from existing .po translated files."
	@echo "    i18n-pot    Generate .pot translation model."
	@echo "    version     Spread version information from root \"VERSION\" file to the whole codebase."


#
# Make all project files
#
all: version i18n-pot i18n-mo build


#
# Clean intermediary files
#
.PHONY: clean clean-mo clean-pyc
clean: clean-pyc clean-mo

clean-mo:
	find ./hotspot_login_manager/lang -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 rm -r 2>/dev/null || true

clean-pyc:
	find ./ -type f -name '*.pyc' -print0 | xargs -0 rm 2>/dev/null || true
	find ./ -type f -name '*.pyo' -print0 | xargs -0 rm 2>/dev/null || true


#
# Rebuild intermediary files
#
.PHONY: build
build: clean-pyc
	devtools/precompile.py
	chmod a-ws,a+rx,u+w ./hotspot-login-manager.py
	find ./hotspot_login_manager -type d -print0 | xargs -0 chmod a-ws,a+rx,u+w
	find ./hotspot_login_manager -type f -print0 | xargs -0 chmod a-wxs,a+r,u+w
	find ./distrib -type d -print0 | xargs -0 chmod a-ws,a+rx,u+w
	find ./distrib -type f -print0 | xargs -0 chmod a-wxs,a+r,u+w
	chmod -R g-rwxs,o-rwxs ./distrib/etc/hotspot-login-manager
	chmod a+rx ./distrib/etc/init.d/hotspot-login-manager
	chmod a+rx ./distrib/etc/network/if-up.d/hotspot-login-manager


#
# Install hooks and configuration files
#
.PHONY: install
install: build
	devtools/make-install install


#
#  Uninstall hooks only, keep configuration files around
#
.PHONY: uninstall
uninstall:
	devtools/make-install uninstall


#
# Uninstall hooks and DELETE configuration files
#
.PHONY: purge
purge:
	devtools/make-install purge


#
# I18N: Generate .mo catalog files from existing .po translated files
#
.PHONY: i18n-mo
i18n-mo: $(shell find ./hotspot_login_manager/lang/ -type f -name '*.po' | sed 's@\.po$$@/LC_MESSAGES/hotspot-login-manager.mo@g')

./hotspot_login_manager/lang/%/LC_MESSAGES/hotspot-login-manager.mo: ./hotspot_login_manager/lang/%.po
	mkdir -p $(shell dirname $@)
	msgfmt --strict --check -o - $^ > $@.tmp
	mv $@.tmp $@


#
# I18N: Generate messages.pot translation model
#
.PHONY: i18n-pot
i18n-pot: ./hotspot_login_manager/lang/hotspot-login-manager.pot

./hotspot_login_manager/lang/hotspot-login-manager.pot: $(shell find ./ -type f -name '*.py')
	mkdir -p ./hotspot_login_manager/lang
	devtools/make-i18n-pot $@ $^


#
# Spread version information from root "VERSION" file to the whole codebase
#
.PHONY: version
version: ./hotspot_login_manager/libs/core/hlm_version_autogen.py

./hotspot_login_manager/libs/core/hlm_version_autogen.py: VERSION
	devtools/make-version-py $@
