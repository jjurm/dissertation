cloc --include-lang="Kotlin,Gradle,Python,CSS,YAML,SQL,Bourne Again Shell" --exclude-d=.idea --quiet --hide-rate --csv graffs partii | tail -n 1 | awk -F, '{print $3+$4+$5}'
