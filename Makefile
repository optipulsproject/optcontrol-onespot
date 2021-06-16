MANUSCRIPT_TEMPLATE_TEX = manuscript-numapde-preprint.tex
MANUSCRIPT_PREPRINT_PDF = $(MANUSCRIPT_TEMPLATE_TEX:.tex=.pdf)
MANUSCRIPT_MAIN_TEX = main.tex

OPTENV = optenv/__init__.py optenv/problem.py optenv/parameters.py optenv/material.json

ZEROGUESS_OPTCONTROLS = $(shell python3 optenv/filenames.py --experiment=zeroguess --type=optcontrols)
ZEROGUESS_REPORTS = $(shell python3 optenv/filenames.py --experiment=zeroguess --type=reports)

RAMPDOWN_OPTCONTROLS = $(shell optenv/filenames.py --experiment=rampdown --type=optcontrols)
RAMPDOWN_REPORTS = $(shell optenv/filenames.py --experiment=rampdown --type=reports)

PLOTS_ALL = plots/optimized/zeroguess.pdf plots/optimized/rampdown.pdf plots/coefficients/vhc.pdf plots/coefficients/kappa.pdf
TABLES_ALL = tables/zeroguess.tex tables/rampdown.tex


preprint: $(MANUSCRIPT_PREPRINT_PDF)

$(MANUSCRIPT_PREPRINT_PDF): \
			$(MANUSCRIPT_MAIN_TEX) \
			$(MANUSCRIPT_TEMPLATE_TEX) \
			$(PLOTS_ALL) \
			$(TABLES_ALL)
	latexmk -pdf -silent $(MANUSCRIPT_TEMPLATE_TEX)

plots/coefficients/vhc.pdf: plots/_src/vhc.py $(OPTENV)
	python3 plots/_src/vhc.py --outfile=$@

plots/coefficients/kappa.pdf: plots/_src/kappa.py $(OPTENV)
	python3 plots/_src/kappa.py --outfile=$@

plots/optimized/zeroguess.pdf: $(ZEROGUESS_OPTCONTROLS) plots/_src/zeroguess.py
	python3 plots/_src/zeroguess.py --outfile=$@

plots/optimized/rampdown.pdf: $(RAMPDOWN_OPTCONTROLS) plots/_src/rampdown.py
	python3 plots/_src/rampdown.py --outfile=$@

tables/zeroguess.tex: $(ZEROGUESS_REPORTS) tables/_src/zeroguess.py
	python3 tables/_src/zeroguess.py > tables/zeroguess.tex

tables/rampdown.tex: $(RAMPDOWN_REPORTS) tables/_src/rampdown.py
	python3 tables/_src/rampdown.py > tables/rampdown.tex

numericals/zeroguess/%.npy numericals/zeroguess/%.json &: \
			numericals/_src/optimize-zeroguess.py \
			$(OPTENV)
	mkdir -p numericals/zeroguess
	python3 numericals/_src/optimize-zeroguess.py --outfile=$@

numericals/rampdown/%.npy numericals/rampdown/%.json &: \
			numericals/_src/optimize-rampdown.py \
			$(OPTENV)
	mkdir -p numericals/rampdown
	python3 numericals/_src/optimize-rampdown.py --outfile=$@


plots.all: plots.coefficients plots.zeroguess plots.rampdown
plots.coefficients: plots/coefficients/vhc.pdf plots/coefficients/kappa.pdf
plots.zeroguess: plots/optimized/zeroguess.pdf
plots.rampdown: plots/optimized/rampdown.pdf

tables.all: tables/zeroguess.tex tables/rampdown.tex

numericals.all: numericals.zeroguess numericals.rampdown
numericals.zeroguess: $(ZEROGUESS_OPTCONTROLS) $(ZEROGUESS_REPORTS)
numericals.rampdown: $(RAMPDOWN_OPTCONTROLS) $(RAMPDOWN_REPORTS)

clean.all: clean.plots clean.numericals
	latexmk -C

clean.numericals:
	rm -rf numericals/zeroguess/*
	rm -rf numericals/rampdown/*

clean.plots:
	rm plots/coefficients/*
	rm plots/optimized/*
