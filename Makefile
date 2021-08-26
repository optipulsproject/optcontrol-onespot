MANUSCRIPT_TEMPLATE_TEX = manuscript-numapde-preprint.tex
MANUSCRIPT_PREPRINT_PDF = $(MANUSCRIPT_TEMPLATE_TEX:.tex=.pdf)
MANUSCRIPT_MAIN_TEX = main.tex

OPTENV = optenv/problem.py optenv/parameters.py optenv/material.json

ZEROGUESS_OPTCONTROLS = $(shell python3 optenv/filenames.py --experiment=zeroguess --type=optcontrols)
ZEROGUESS_REPORTS = $(shell python3 optenv/filenames.py --experiment=zeroguess --type=reports)

RAMPDOWN_OPTCONTROLS = $(shell optenv/filenames.py --experiment=rampdown --type=optcontrols)
RAMPDOWN_REPORTS = $(shell optenv/filenames.py --experiment=rampdown --type=reports)
RAMPDOWN_NOOPT_CONTROLS = $(subst rampdown,rampdown-noopt, $(RAMPDOWN_OPTCONTROLS))
RAMPDOWN_NOOPT_REPORTS = $(subst rampdown,rampdown-noopt, $(RAMPDOWN_REPORTS))

.PHONY: preprint \
		plots.all plots.coefficients plots.optimized plots.zeroguess plots.rampdown\
		tables.all \
		numericals.all numericals.zeroguess numericals.rampdown\
		touch \
		clean.all clean.temp clean.preprint clean.plots clean.numericals

# a workaround to make optenv package visible for the python scripts
# works only if make is called from the project root dir (which is normally the case)
export PYTHONPATH = :


preprint: $(MANUSCRIPT_PREPRINT_PDF)

$(MANUSCRIPT_PREPRINT_PDF): \
			$(MANUSCRIPT_MAIN_TEX) \
			$(MANUSCRIPT_TEMPLATE_TEX) \
			plots.all \
			tables.all
	latexmk -pdf -silent $(MANUSCRIPT_TEMPLATE_TEX)

plots/coefficients/vhc.pdf: plots/_src/vhc.py $(OPTENV)
	mkdir -p plots/coefficients
	python3 plots/_src/vhc.py --outfile=$@

plots/coefficients/kappa.pdf: plots/_src/kappa.py $(OPTENV)
	mkdir -p plots/coefficients
	python3 plots/_src/kappa.py --outfile=$@

plots/optimized/zeroguess.pdf: $(ZEROGUESS_OPTCONTROLS) plots/_src/zeroguess.py
	mkdir -p plots/optimized
	python3 plots/_src/zeroguess.py --outfile=$@

plots/optimized/rampdown.pdf: \
		$(RAMPDOWN_OPTCONTROLS) \
		$(RAMPDOWN_NOOPT_CONTROLS) \
		plots/_src/rampdown.py
	mkdir -p plots/optimized
	python3 plots/_src/rampdown.py --outfile=$@

tables/zeroguess.tex: $(ZEROGUESS_REPORTS) tables/_src/zeroguess.py
	python3 tables/_src/zeroguess.py > tables/zeroguess.tex

tables/rampdown.tex: \
		$(RAMPDOWN_REPORTS) \
		$(RAMPDOWN_NOOPT_REPORTS) \
		tables/_src/rampdown.py
	python3 tables/_src/rampdown.py > tables/rampdown.tex

# since the grouped targets feature was introduces in make since v4.3
# and we want to keep the project compatible with make >= 4.1
# here is some workaround for the grouped targets

numericals/zeroguess/%.json: numericals/zeroguess/%.npy ;
numericals/zeroguess/%.npy : \
			numericals/_src/optimize-zeroguess.py \
			$(OPTENV)
	mkdir -p numericals/zeroguess
	python3 numericals/_src/optimize-zeroguess.py --outfile=$@

numericals/rampdown/%.json: numericals/rampdown/%.npy ;
numericals/rampdown/%.npy: \
			numericals/_src/optimize-rampdown.py \
			$(OPTENV)
	mkdir -p numericals/rampdown
	python3 numericals/_src/optimize-rampdown.py --outfile=$@

numericals/rampdown-noopt/%.json: numericals/rampdown-noopt/%.npy ;
numericals/rampdown-noopt/%.npy: \
			numericals/_src/optimize-rampdown.py \
			$(OPTENV)
	mkdir -p numericals/rampdown-noopt
	python3 numericals/_src/optimize-rampdown.py --no-opt --outfile=$@

# PHONY

plots.all: plots.coefficients plots.zeroguess plots.rampdown
plots.coefficients: plots/coefficients/vhc.pdf plots/coefficients/kappa.pdf
plots.zeroguess: plots/optimized/zeroguess.pdf
plots.rampdown: plots/optimized/rampdown.pdf

tables.all: tables/zeroguess.tex tables/rampdown.tex

numericals.all: numericals.zeroguess numericals.rampdown
numericals.zeroguess: $(ZEROGUESS_OPTCONTROLS) $(ZEROGUESS_REPORTS)
numericals.rampdown: \
		$(RAMPDOWN_OPTCONTROLS) $(RAMPDOWN_REPORTS) \
		$(RAMPDOWN_NOOPT_CONTROLS) $(RAMPDOWN_NOOPT_REPORTS)

touch:
	touch numericals/rampdown/*
	touch numericals/rampdown-noopt/*
	touch numericals/zeroguess/*

clean.all: clean.preprint clean.plots clean.numericals

clean.temp:
	latexmk -c

clean.preprint:
	latexmk -C

clean.plots:
	rm -rf plots/coefficients/*
	rm -rf plots/optimized/*

clean.numericals:
	rm -rf numericals/zeroguess/*
	rm -rf numericals/rampdown/*
