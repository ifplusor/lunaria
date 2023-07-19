LUNARIZE=python3 ../lunarize.py
LIGHT_THEME=../lunaria-light.json
DARK_THEME=../lunaria-dark.json
ECLIPSE_THEME=../lunaria-eclipse.json
EINK_THEME=../lunaria-eink.json

all: themes/light.json themes/dark.json themes/eclipse.json themes/e-ink.json

clean: 
	$(RM) themes/template.json themes/light.json themes/dark.json themes/eclipse.json themes/template-eink.json themes/e-ink.json

themes/template.json: themes/template.yaml
	npx js-yaml themes/template.yaml > themes/template.json

themes/light.json: themes/template.json $(LIGHT_THEME)
	$(LUNARIZE) $(LIGHT_THEME) $< $@

themes/dark.json: themes/template.json $(DARK_THEME)
	$(LUNARIZE) $(DARK_THEME) $< $@

themes/eclipse.json: themes/template.json $(ECLIPSE_THEME)
	$(LUNARIZE) $(ECLIPSE_THEME) $< $@

themes/template-eink.json: themes/template-eink.yaml
	npx js-yaml themes/template-eink.yaml > themes/template-eink.json

themes/e-ink.json: themes/template-eink.json $(EINK_THEME)
	$(LUNARIZE) --format=identity $(EINK_THEME) $< $@

.PHONY: all clean
