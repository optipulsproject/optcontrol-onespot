CONTROLS_OPTIMIZED=$(shell /bin/bash -c 'echo numericals/{1500,2000,2500}-0.0{10,15,20}.npy')
PLOTS_OPTIMIZED=$(subst numericals/,plots/optimized/,$(CONTROLS_OPTIMIZED:.npy=.pdf))

MANUSCRIPT_PREPRINT_TEX=manuscript-numapde-preprint.tex
MANUSCRIPT_PREPRINT_PDF=$(MANUSCRIPT_PREPRINT_TEX:.tex=.pdf)
MAIN_TEX=main.tex


preprint: $(MANUSCRIPT_PREPRINT_PDF)

$(MANUSCRIPT_PREPRINT_PDF): $(MAIN_TEX) $(MANUSCRIPT_PREPRINT_TEX) $(PLOTS_OPTIMIZED)
	latexmk -pdf -silent $(MANUSCRIPT_PREPRINT_TEX)

numericals/%.npy: bin/compute-optimal-control.py
	mkdir -p numericals
	python3 bin/compute-optimal-control.py --scratch=./numericals --outfile=$@

plots/optimized/%.pdf: numericals/%.npy plots/_src/plot-control.py
	mkdir -p plots/optimized
	python3 plots/_src/plot-control.py --infile=$< --outfile=$@
