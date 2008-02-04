CONFIGS :=
CONFIG_NODEP :=
MAKE_OPTS :=

include multiarch.make

# multiarch kernel makefile
all modules_install mrproper:
	$(Q)$(MAKE) -C $(srctree) $(MAKE_OPTS) $<

pykconfig: $(objtree)/.config.conf
	@echo 'pykconfig is up to date'

$(objtree)/.config.conf: $(srctree)/arch/$(SRCARCH)/defconfig
	@echo '  kernel-config-update.py $(ARCH) arch/$(SRCARCH)/defconfig.conf $< > $@'
	$(Q)$(objtree)/scripts/kernel-config-update.py $(ARCH) $(srctree)/arch/$(SRCARCH)/defconfig.conf $< > .config.conf.tmp
	$(Q)mv .config.conf.tmp $@

$(srctree)/arch/$(SRCARCH)/defconfig: $(srctree)/arch/$(SRCARCH)/defconfig.conf
	@echo '  kernel-config.py $(ARCH) $< $@'
	$(Q)> .defconfig.tmp
	$(Q)$(objtree)/scripts/kernel-config.py $(ARCH) $< .defconfig.tmp
	$(Q)mv .defconfig.tmp $@
	$(Q)ln -sf $@ $(objtree)/.config

$(srctree)/arch/$(SRCARCH)/defconfig.conf: $(CONFIGS) $(objtree)/defconfig-nodep.conf
	$(Q)cat $^ > $@

$(objtree)/defconfig-nodep.conf: $(CONFIG_NODEP)
	$(Q)if [ ! -f $@ ] || ! cmp -s $< $@; then \
		echo '  cat $< > $@'; \
		cat $< > $@; \
	fi
