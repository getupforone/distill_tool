#!/bin/bash
#for d in */;do
#   tar -cvJf "${d%/}.tar.xz" "$d";
#done

for d in "*.tar.xz";do
	for dd in $d; do
		echo dd $dd
   		tar -xvJf ${dd};
	done
done
#for d in "*.tar";do echo $d;echo $d; xz -9e --threads=16 -c -> "${d}.xz"; done
