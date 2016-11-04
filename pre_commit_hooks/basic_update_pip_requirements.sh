#!/bin/sh
# A hook to commit the updated python dependencies list at each commit

pip3 freeze > requirements.txt 
exec git add requirements.txt