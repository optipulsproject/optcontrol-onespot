# A template for publications
This is a template repository to fork publication repositories from.

## How to use this repository
* Clone this repository into some working directory. We assume `~/Work/Publications/numapde-template`.
* Pull the latest changes to this repository:
  ````bash
  cd ~/Work/Publications/numapde-template
  git pull
  ````
* Call the [bin/numapde-create-new-publication.py](bin/numapde-create-new-publication.py) script which initiates the fork & rename and sets up a basic `README.me` file in the new repository.
  ````bash
  # The following will fork into https://gitlab.hrz.tu-chemnitz.de/numapde/Publications/Riemannian-ADMM
  bin/numapde-create-new-publication.py "Intrinsic ADMM on Riemannian Manifolds" "Riemannian ADMM"
  # The following will fork into https://gitlab.hrz.tu-chemnitz.de/numapde/Sandbox/Riemannian-ADMM
  bin/numapde-create-new-publication.py "Intrinsic ADMM on Riemannian Manifolds" "Riemannian ADMM" --namespace numapde/Sandbox 
  ````

The script relies on the following standard environment variables to be set:
*  NUMAPDE_GITLAB_SERVER : the URL of this gitlab server (gitlab.hrz.tu-chemnitz.de)
*  NUMAPDE_GITLAB_TOKEN  : Your personal gitlab-access token; see the [numapde-wiki](https://www.tu-chemnitz.de/mathematik/numawiki/index.php/Incoming#Account_for_numapde_Gitlab_Repositories) for the generation of the personal access token.

The script has the following option:
*  `--namespace`: provides a Gitlab namespace. The default namespace is `numapde/Publications`.

## After forking
* When finishing, the script will report the address to clone the newly created repository.
* You may use `bin/numapde-submodules-updates.sh` at any time to update the dependent submodules.
* If necessary, you may use `source bin/numapde-set-paths.sh` to setup the `TEXINPUTS` and `BIBINPUTS` environment variables.
  This script will only amend paths if necessary.
* The script `bin/numapde-pack-it-all.sh` can be used to pack the manuscript files into a `.zip` file, e.g., for submission to https://arxiv.org.
* Invite coauthors external to the group through https://gitlab.hrz.tu-chemnitz.de.

