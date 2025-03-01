
# Checklists for tasks in the corpus publishing pipeline

The following lists contain tasks required for publishing a corpus. The
lists are in a rough order in which tasks should be (or typically are)
done.

The appropriate task list can be copied verbatim to the description of
a Jira ticket for publishing (a version of) a corpus, where it will be
rendered as an enumerated list. (The list should be copied when the
description input field is in “Text” mode, not “Visual”.) In the
description field, the list should be adjusted as appropriate for the
corpus in question: for example, LBR records are needed only for RES
corpora.

Each task description is preceded by “[ ]” representing a checkbox and
a task type marker. When you take a task under work, write your name
between the square brackets (“[Name]”). When a task is completed,
replace it with an “[X]”.

The task type marker is an italicized (slanted) two-character string.
The first character is _+_ for obligatory tasks and _?_ for optional
ones, and the second character indicates the rough type of the task by
one of the following letters:

- _A_: administrative
- _D_: data processing
- _K_: Korp configuration
- _T_: testing

## Negotiate publishing a corpus in the Language Bank of Finland

```
# [ ] _+A_ Negotiate with the corpus owner
# [ ] _+A_ Prepare a deposition agreement and have it signed
```

## Acquire source data

```
# [ ] _+D_ Receive, download or harvest the data
# [ ] _+D_ Check the data: format and validity
## [ ] _?D_ Clean up the data
# [ ] _+D_ Package the data for IDA
# [ ] _+D_ Upload the data package to IDA
```

## Publish source data in Download 

```
# [ ] _?D_ Get the data from IDA
# [ ] _+A_ Create a META-SHARE record
# [ ] _+A_ Request URNs (for META-SHARE, download, license pages)
# [ ] _+A_ Add corpus to the list of upcoming resources
# [ ] _+A_ Create license pages
# [ ] _+A_ Add citing information to the META-SHARE record
# [ ] _+D_ Create a download package
## [ ] _+D_ Create and add readme and license files
## [ ] _+D_ Zip the data and the readme and license files
## [ ] _+D_ Compute an MD5 checksum for the zip package
# [ ] _+D_ Add the download package, MD5 checksum file and readme and license files to the directory {{/scratch/clarin/download_preview}} on Puhti
# [ ] _+T_ Have the package tested
# [ ] _?A_ Create an LBR record (for a RES corpus)
# [ ] _+D_ Upload the package to the download service (or ask someone with the rights to do that)
# [ ] _+T_ Have it tested again (access rights!)
# [ ] _+A_ Move the resource from the list of upcoming resources to the list of published resources
# [ ] _+A_ Update the META-SHARE record; add location PID
# [ ] _+A_ Create or update the resource group page
# [ ] _+A_ Publish news about the new corpus on the Portal
# [ ] _+D_ Upload the source package to IDA
## [ ] _+A_ Freeze the IDA package
# [ ] _?D_ Ask Martin (or Tero) to add the data to Kielipankki directory {{/appl/data/kielipankki}} on Puhti if the source data is to be published there
```

## Publish a corpus in Korp

```
# [ ] _?D_ Get the data from IDA
# [ ] _+A_ Create a META-SHARE record
# [ ] _+A_ Request URNs (for META-SHARE, Korp, license pages)
# [ ] _+A_ Add corpus to the list of upcoming resources
# [ ] _+A_ Create license pages
# [ ] _+A_ Add citing information to the META-SHARE record
# [ ] _?D_ Convert the data to HRT
# [ ] _?D_ Convert HRT to VRT (tokenizing)
# [ ] _?D_ Convert the data directly to VRT (alternative to HRT->VRT)
# [ ] _?D_ Parse the data (for corpora in languages with a parser)
# [ ] _?D_ Re-order or group the data (e.g. chapters, articles)
# [ ] _?D_ Add additional annotations
## [ ] _?D_ Add name annotations
## [ ] _?D_ Add sentiment annotations
## [ ] _?D_ Add identified languages
# [ ] _+D_ Validate the VRT data
# [ ] _+D_ Check the positional attributes
## [ ] _?D_ Re-order to the commonly used order if necessary
# [ ] _+D_ Create a Korp corpus package ({{korp-make}})
## [ ] _+D_ Install the corpus package on the Korp server (or ask someone with the rights to do that)
# [ ] _+K_ Add corpus configuration to Korp (currently, a new branch in [Kielipankki-korp-frontend|https://https://github.com/CSCfi/Kielipankki-korp-frontend])
## [ ] _+K_ Add the configuration proper to a Korp mode file
## [ ] _+K_ Add translations of new attribute names (and values)
## [ ] _+K_ Push the branch to GitHub
## [ ] _+K_ Create a Korp test instance and install the new configuration branch to it (or ask someone with the rights to do that)
# [ ] _?D_ For a non-PUB corpus, add temporary access rights for the people who should test it (with the {{authing/auth}} script on the Korp server)
# [ ] _+T_ Test the corpus in Korp (Korp test version) and ask someone else to test it, too
## [ ] _?A_ Ask feedback from the corpus owner (depending on how involved they wish to be)
# [ ] _?D_ Fix corpus data and re-publish (if needed)
# [ ] _?K_ Fix Korp configuration and re-publish (if needed)
# [ ] _+D_ Upload the Korp corpus package to IDA
# [ ] _+K_ Publish the corpus in Korp as a beta test version
## [ ] _+K_ Merge the corpus configuration branch to branch {{master}}
## [ ] _+K_ Add news about this new corpus to the Korp newsdesk (https://github.com/CSCfi/Kielipankki-korp-frontend/tree/news/master)
## [ ] _+K_ Install the updated {{master}} branch to production Korp (or ask someone with the rights to do that)
# [ ] _?A_ Create an LBR record (for a RES corpus, if the corpus does not yet have one)
# [ ] _+A_ Move the corpus from the list of upcoming resources to the list of published resources (add status beta to the name!)
# [ ] _+A_ Update META-SHARE record; add location PID
# [ ] _+A_ Add beta status to META-SHARE record and resource group page
# [ ] _+A_ Publish news about this new corpus in the portal
# [ ] _?A_ Inform corpus owner and possibly interested researchers on the corpus in Korp and ask them to test it
# [ ] _?D_ Fix corpus data based on feedback and re-publish (if needed)
## [ ] _?D_ Upload a fixed Korp corpus package to IDA
# [ ] _?K_ Fix corpus configuration in Korp and re-publish (if needed)
# [ ] _+A_ Remove beta status after two weeks, if no requests for corrections or changes appear during this period
## [ ] _+K_ Remove beta status from Korp configuration ({{master}}), push and install the updated {{master}}
## [ ] _+A_ Remove beta status from the META-SHARE record and resource group page
# [ ] _+A_ Freeze the IDA package
```

## Publish VRT data in Download

```
# [ ] _+D_ Get the data from IDA or extract it from Korp
# [ ] _+A_ Create a META-SHARE record
# [ ] _+A_ Request URNs (for META-SHARE, download, license pages)
# [ ] _+A_ Add the corpus to list of upcoming resources
# [ ] _+A_ Create license pages
# [ ] _+A_ Add citing information to the META-SHARE record
# [ ] _+D_ Create a download package
## [ ] _+D_ Create and add readme and license files
## [ ] _+D_ Zip the data and the readme and license files
## [ ] _+D_ Compute MD5 checksum for the zip package
# [ ] _+D_ Add the download package, MD5 checksum file and readme and license files to the directory {{/scratch/clarin/download_preview}} on Puhti
# [ ] _+T_ Have the package tested
# [ ] _+D_ Upload the package to the download service (or ask someone with the rights to do that)
# [ ] _?A_ Create an LBR record (for a RES corpus, if the corpus does not yet have one)
# [ ] _+T_ Have it tested again (access rights!)
# [ ] _+A_ Move the corpus from the list of upcoming resources to the list of published resources
# [ ] _+A_ Update the META-SHARE record; add location PID
# [ ] _+A_ Create or update the resource group page
# [ ] _+A_ Publish news about the new corpus on the Portal
# [ ] _?A_ If the package was published as beta (during the beta stage of the corresponding Korp corpus), remove the beta status after removing the beta status from Korp
## [ ] _?D_ Create a new download package with the beta status removed from the readme file and file names
## [ ] _?D_ Compute MD5 checksum for the zip package
## [ ] _?D_ Upload the package to the download service (or ask someone with the rights to do that)
## [ ] _?A_ Remove beta status from the META-SHARE record and resource group page
# [ ] _+D_ Upload the VRT package to IDA
## [ ] _+A_ Freeze the IDA package
# [ ] _?D_ Ask Martin (or Tero) to add the data to Kielipankki directory {{/appl/data/kielipankki}} on Puhti (if the corpus is PUB or ACA)
```
