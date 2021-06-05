MANUSCRIPT_TEMPLATE_TEX = manuscript-numapde-preprint.tex
MANUSCRIPT_PREPRINT_PDF = $(MANUSCRIPT_TEMPLATE_TEX:.tex=.pdf)
MANUSCRIPT_MAIN_TEX = main.tex

CONTROLS_OPTIMIZED_ZERO = $(shell /bin/bash -c 'echo numericals/zeroguess/{1500,2000,2500}-0.0{10,15,20}.npy')
CONTROLS_OPTIMIZED_RAMPDOWN = $(shell /bin/bash -c 'echo numericals/rampdown/2000-1500-0.005-{0.005,0.010}-0.012.npy')

PLOTS_ALL = plots/optimized/zeroguess.pdf plots/optimized/rampdown.pdf


$(MANUSCRIPT_PREPRINT_PDF): $(MANUSCRIPT_MAIN_TEX) $(MANUSCRIPT_TEMPLATE_TEX) $(PLOTS_ALL)
	latexmk -pdf -silent $(MANUSCRIPT_TEMPLATE_TEX)

plots/optimized/zeroguess.pdf: $(CONTROLS_OPTIMIZED_ZERO) plots/_src/zeroguess.py
	python3 plots/_src/zeroguess.py --outfile=$@

plots/optimized/rampdown.pdf: $(CONTROLS_OPTIMIZED_RAMPDOWN) plots/_src/rampdown.py
	python3 plots/_src/rampdown.py --outfile=$@

numericals/%: $(wildcard 'optenv/*')

numericals/zeroguess/%.npy: numericals/_src/optimize-zeroguess.py
	mkdir -p numericals/zeroguess
	python3 numericals/_src/optimize-zeroguess.py --outfile=$@

numericals/rampdown/%.npy: numericals/_src/optimize-rampdown.py
	mkdir -p numericals/rampdown
	python3 numericals/_src/optimize-rampdown.py --outfile=$@


##############################################3

# # plots of advanced optimized controls
# plots/optimized/advanced/%.pdf: numericals/advanced/%.npy plots/_src/plot-control-advanced.py
# 	mkdir -p plots/optimized/advanced
# 	python3 plots/_src/plot-control-advanced.py --infile=$< --outfile=$@

# clean.figs:
# 	rm -rf plots/optimized

# clean.tmp:
# 	latexmk -c

clean.all: clean.plots clean.numericals
	latexmk -C

clean.numericals:
	rm -rf numericals/zeroguess/*.npy
	rm -rf numericals/rampdown/*.npy

clean.plots:
	rm plots/optimized/*
