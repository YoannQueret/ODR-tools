#!/bin/bash
# run all what you need based on ODR dab-scripts in one screen session
# see : https://github.com/Opendigitalradio/dab-scripts/
# 
# Installation :
# copy this script into dab-scripts/ directory
#
# Usage :
# ./run.sh

echo "Create screen session ODR"
screen -d -m -S ODR

# window 0 is created by default, don't need to create it

echo "In ODR screen session, create window 0 for jackd"
screen -S ODR -p 0 -X title jackd
screen -S ODR -p 0 -X exec jackd -d dummy -r 48000

echo "In ODR screen session, create window 1 for odr-mux & odr-mod"
screen -S ODR -X screen 1
screen -S ODR -p 1 -X title mux
screen -S ODR -p 1 -X exec ./start-mux-mod.sh


if [ -f site/configuration.sh ]
then

    source site/configuration.sh

    n=2
    for radio in ${all_radios[*]}
    do
	echo "In ODR screen session, create window $n for $radio encoder"
	screen -S ODR -X screen $n
	screen -S ODR -p $n -X title encoder-$radio
	screen -S ODR -p $n -X exec ./radio.sh $radio
        sleep 0.4
	n=$(($n+1))
    done
fi

echo "To enter the ODR screen use :"
echo "  screen -rS ODR"