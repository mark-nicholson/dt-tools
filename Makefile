#
#  Utilities to speed up develpment
#

INTF_UI = devicetree/gui/dt_main_window.ui \
          devicetree/gui/compiler_dialog.ui \
          devicetree/gui/console_dialog.ui
INTF_PY = $(INTF_UI:.ui=.py)

help:
	@echo "Utility Targets"
	@echo ""
	@echo "    run       - build depends and launch the app"
	@echo "    designer  - run the QT4 GUI Designer"
	@echo "    test      - run the testing "
	@echo "    clean     - tidy up general files"
	@echo "    distclean - scrub the directory structure"
	@echo ""

designer:
	designer-qt4 &

run: $(INTF_PY)
	PYTHONPATH=. python3 devicetree/dtviewer.py


build-ui: $(INTF_PY)


.SUFFIXES: .ui .py
.ui.py:
	@rm -f $@
	pyside-uic $< > $@

info:
	@echo "INTF_UI = $(INTF_UI)"
	@echo "INTF_PY = $(INTF_PY)"

clean:
	rm -rf build
	rm -f $(INTF_PY)
	find . -name '*~' | xargs /bin/rm -f
	find . -name '__pycache__' | xargs /bin/rm -rf

distclean: clean
	rm -rf venv

#
#  Utility for bootstrapping the virtual-env
#
get-pip.py:
	wget https://bootstrap.pypa.io/get-pip.py

venv: get-pip.py
	@echo "Setting up VirtualEnv ..."
	/usr/bin/python3 /usr/bin/pyvenv-3.4 $@ \
		 --system-site-packages --without-pip
	. $@/bin/activate && python3 get-pip.py

