# A Template for Publications
This is a template repository to fork publication repositories from.

## How to Use This Repository
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
