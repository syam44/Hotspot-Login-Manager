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
	@echo "    all         Make all project files: version, i18n-pot, i18n-mo"
	@echo "    clean       Clean intermediary files."
	@echo
	@echo "    i18n-mo     Generate .mo catalog files (program translations) from existing .po translated files."
	@echo "    i18n-pot    Generate .pot translation model."
	@echo "    version     Spread version information from root \"VERSION\" file to the whole codebase."


#
# Make all project files
#
all: version i18n-pot i18n-mo


#
# Clean intermediary files
#
.PHONY: clean clean-mo clean-pyc
clean: clean-pyc clean-mo

clean-mo:
	find ./hotspot_login_manager/lang -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 rm -r 2>/dev/null || true

clean-pyc:
	find ./ -type f -name '*.pyc' -print0 | xargs -0 rm 2>/dev/null || true


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
