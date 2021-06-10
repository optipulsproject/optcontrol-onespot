MANUSCRIPT_TEMPLATE_TEX = manuscript-numapde-preprint.tex
MANUSCRIPT_PREPRINT_PDF = $(MANUSCRIPT_TEMPLATE_TEX:.tex=.pdf)
MANUSCRIPT_MAIN_TEX = main.tex

ZEROGUESS_OPTCONTROLS = $(shell optenv/filenames.py --experiment=zeroguess --type=optcontrols)
ZEROGUESS_REPORTS = $(shell optenv/filenames.py --experiment=zeroguess --type=reports)

RAMPDOWN_OPTCONTROLS = $(shell optenv/filenames.py --experiment=rampdown --type=optcontrols)
RAMPDOWN_REPORTS = $(shell optenv/filenames.py --experiment=rampdown --type=reports)

PLOTS_ALL = plots/optimized/zeroguess.pdf plots/optimized/rampdown.pdf
TABLES_ALL = tables/zeroguess.tex tables/rampdown.tex


$(MANUSCRIPT_PREPRINT_PDF): \
			$(MANUSCRIPT_MAIN_TEX) \
			$(MANUSCRIPT_TEMPLATE_TEX) \
			$(PLOTS_ALL) \
			$(TABLES_ALL)
	latexmk -pdf -silent $(MANUSCRIPT_TEMPLATE_TEX)

plots/optimized/zeroguess.pdf: $(ZEROGUESS_OPTCONTROLS) plots/_src/zeroguess.py
	python3 plots/_src/zeroguess.py --outfile=$@

plots/optimized/rampdown.pdf: $(RAMPDOWN_OPTCONTROLS) plots/_src/rampdown.py
	python3 plots/_src/rampdown.py --outfile=$@

numericals/zeroguess/%.npy numericals/zeroguess/%.json &: numericals/_src/optimize-zeroguess.py
	mkdir -p numericals/zeroguess
	python3 numericals/_src/optimize-zeroguess.py --outfile=$@


numericals/rampdown/%.npy numericals/rampdown/%.json &: numericals/_src/optimize-rampdown.py
	mkdir -p numericals/rampdown
	python3 numericals/_src/optimize-rampdown.py --outfile=$@

tables/zeroguess.tex: $(ZEROGUESS_REPORTS) tables/_src/zeroguess.py
	python3 tables/_src/zeroguess.py > tables/zeroguess.tex

tables/rampdown.tex: $(RAMPDOWN_REPORTS) tables/_src/rampdown.py
	python3 tables/_src/rampdown.py > tables/rampdown.tex


clean.all: clean.plots clean.numericals
	latexmk -C

clean.numericals:
	rm -rf numericals/zeroguess/*.npy
	rm -rf numericals/rampdown/*.npy

clean.plots:
	rm plots/optimized/*
