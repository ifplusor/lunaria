LUNARIZE=python3 ../lunarize.py
LIGHT_THEME=../lunaria-light.json
DARK_THEME=../lunaria-dark.json
ECLIPSE_THEME=../lunaria-eclipse.json

ifeq ($(shell uname -s),Darwin)
	SED=sed -i ''
else
	SED=sed -i
endif

all: lunaria_light.yaml lunaria_dark.yaml lunaria_eclipse.yaml
clean: 
	$(RM) lunaria_light.yaml lunaria_dark.yaml lunaria_eclipse.yaml

lunaria_light.yaml: template.yaml $(LIGHT_THEME)
	$(LUNARIZE) --format=css_hex $(LIGHT_THEME) $< $@
	$(SED) 's/DETAILS/lighter/g' $@

lunaria_dark.yaml: template.yaml $(DARK_THEME)
	$(LUNARIZE) --format=css_hex $(DARK_THEME) $< $@
	$(SED) 's/DETAILS/darker/g' $@

lunaria_eclipse.yaml: template.yaml $(ECLIPSE_THEME)
	$(LUNARIZE) --format=css_hex $(ECLIPSE_THEME) $< $@
	$(SED) 's/DETAILS/darker/g' $@

.PHONY: all clean
