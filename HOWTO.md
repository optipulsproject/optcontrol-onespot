# A Template for Publications

The numapde/Publications/numapde-template repository serves as a template for new publications.

## Setup a new Publication Repository from the Template
* Visit numapde/Publications/numapde-template> (preferably in a new browser tab or window), and fork it into a new (temporary) repository in your own personal namespace.
You will be taken to this new repository in your browser.
* Visit _Settings / General_ and change the **Project name** to something reflecting the intended topic of the publication.
Hit _Save changes_.
* On the same page, expand _Advanced_, scroll down to **Change path** and set it to something concise and related to the **Project name**.
Hit _Change path_.
* On the same page, scroll down to **Transfer project** and select _numapde / Publications_.
Hit _Transfer project_ and confirm the transfer as required.
You will be taken to the new repository location in your browser.
* Visit _Settings / General_ and update the **Project description** to reflect the intended topic of the publication.
Hit _Save changes_.
* Visit _Project_, open and edit [README.md](README.md) and replace its contents with the content enclosed by :scissors: below. 
Then edit the **@placeholders@** and save.
* After cloning the repository, you may want to rename `numapde-template.tex` and edit `numapde-local.sty` to get started with your publication.
* Visit _Settings / Members_ and invite co-authors as members to the repository.
Give them _Developer_ permissions.
(Notice that @numapde group members are automatically added by virtue of the namespace policy.)

:scissors:
``````markdown
# @Publication Title@
Authors:

## Cloning
Clone this repository using either
```bash
    git clone --recurse-submodules git@gitlab.hrz.tu-chemnitz.de:numapde/Publications/@project-name@.git 
```
if you have placed an SSH key in https://gitlab.hrz.tu-chemnitz.de/profile/keys, or 
```bash
    git clone --recurse-submodules https://gitlab.hrz.tu-chemnitz.de:numapde/Publications/@project-name@.git 
```
Then run 
```bash
    bin/numapde-submodules-updates.sh
```
to update the submodules numapde-public/numapde-latex> and numapde-public/numapde-bibliography>.

## Daily Workflow
Run 
```bash
    bin/numapde-submodules-updates.sh
```
regularly to update the submodules.
``````
:scissors: