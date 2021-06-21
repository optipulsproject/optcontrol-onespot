An Optimal Control Problem for Single Spot Laser Pulse Welding
==============================================================

[![pipeline status](https://gitlab.hrz.tu-chemnitz.de/numapde/Publications/optimal-control-spot-welding/badges/master/pipeline.svg)](https://gitlab.hrz.tu-chemnitz.de/numapde/Publications/optimal-control-spot-welding/-/commits/master)

This repository contains a manuscript which is a part of [OptiPuls][projectpage] project.

---

**Authors:** Dmytro Strelnikov <dmytro.strelnikov@math.tu-chemnitz.de>, Roland Herzog <roland.herzog@math.tu-chemnitz.de>  
**Funding:** Funding: Project IGF 20.826B (DVS I2.3005) in Forschungsvereinigung Schweißen und verwandte Verfahren e.V. of the [Deutschen Verbandes für Schweißen und verwandte Verfahren e.V.](https://www.die-verbindungs-spezialisten.de/)  
**Project page:** [Simulation Based Optimization of the Time-Dependent Pulse Power for Laser Beam Welding of Aluminum Alloys in Order to Avoid Hot Cracks][projectpage]


## About this paper

A mathematical model for the single spot laser pulse welding based on the quasi-linear heat equation is derived in the paper and a detailed discretization procedure is given. The corresponding [optipuls](https://github.com/dstrelnikov/optipuls) python module provides the outlined discrete model implemented in code utilizing the [FEniCS](https://fenicsproject.org/) computing platform.

The numerical results presented in the paper can be easily reproduced by following the instructions from this document.


## Numerical results

This section provides detailed instructions on reproducing of the numerical results presented in the paper.

### Why?

We believe that any numerical results presented in a scientific publication must be considered reliable only if the exaсt way they were obtained is clear and hence they can be verified by a reader. The most transparent way to go is to provide an explicit instruction on reproducing of the results, requiring only free software.

Despite it is often not the case in many scientific publications, we intend to encourage reproducibility culture in computational science by setting an example.

### Prerequisites

A working [FEniCS](https://fenicsproject.org/) computing platform installation is required as well as the following additional python packages (including their dependencies):

- [optipuls](https://github.com/dstrelnikov/optipuls)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [tabulate](https://pypi.org/project/tabulate/)

We suppose that [make](https://www.gnu.org/software/make/) is already installed on your machine provided a UNIX-like system is used.

If you already have FEniCS installed locally, you can use python virtual environments to install the remaining dependencies without cluttering your system:
```
python3 -m venv --system-site-packages ~/.local/optipuls
source ~/.local/optipuls/bin/activate
pip install git+https://github.com/dstrelnikov/optipuls@optcontrol
pip install matplotlib tabulate
```

Since it can get quite tricky to install FEniCS, we also provide a bundle of docker images.


### Reproducing (local build)

Once the depencdencies are satisfied, reproducing of the results is as simple as running `make` in the root of the project:
```
git clone https://gitlab.hrz.tu-chemnitz.de/numapde/Publications/optimal-control-spot-welding
cd optimal-control-spot-welding
make -j$(nproc)
```

Make will run the computations, produce the plots, the tables, and the final `manuscript-numapde-preprint.pdf` file.


### Reproducing (build in docker)

Don't forget to build/pull the `optipuls`, `tabulate`, and `numapde/publications` docker images in advance.

Compute & make plots:
```
docker run \
  -v $(pwd):/home/fenics/shared \
  optipuls:latest \
  make -C shared plots.all -j$(nproc)
```

Make tables:
```
$ docker run \
  -u $UID \
  -v $(pwd):/data \
  tabulate:latest \
  make tables.all
```

Make paper:
```
docker run \
  -u $UID \
  -v $(pwd):/data \
  numapde/publications:latest \
  make preprint
```

q
### GitLab CI/CD artifacts

- `manuscript-numapde-preprint.pdf` (latest successful) [view][gitlab-pdf-view], [download][gitlab-pdf-download]

### How?

For anyone how might get interested in implementing a similar reproduction mechanism, we outline the key points of the paper building process.

#### GitLab CI/CD and make

...

[projectpage]: https://www.tu-chemnitz.de/mathematik/part_dgl/projects/optipuls/index.en.php "OptiPuls"

[gitlab-pdf-view]: https://gitlab.hrz.tu-chemnitz.de/numapde/Publications/optimal-control-spot-welding/-/jobs/artifacts/master/file/manuscript-numapde-preprint.pdf?job=tex
[gitlab-pdf-download]: https://gitlab.hrz.tu-chemnitz.de/numapde/Publications/optimal-control-spot-welding/-/jobs/artifacts/master/raw/manuscript-numapde-preprint.pdf?job=tex