# A Template for Publications

## Initial step
We provide the python script bin/numapde-create-new-publication.py which forkes this repository and provides a basic README.md. The simplest call provides a long and a short title, i.e.
````
    python3 bin/numapde-create-new-publication.py "I am the long title" "i am the short title"
````

The script requires  the following environment variables:
*  NUMAPDE_GITLAB_SERVER : the url of this gitlab server (gitlab.hrz.tu-dresden.de)
*  NUMAPDE_GITLAB_TOKEN  : Your personal gitlab-access token. See the [numapde-wiki](https://www.tu-chemnitz.de/mathematik/numawiki/index.php/Incoming#Account_for_numapde_Gitlab_Repositories) for the generation of the personal access token.

The script has the following option:
*  --namespace : provide a new gitlab namespace. The default namespace is numapde/Publications

