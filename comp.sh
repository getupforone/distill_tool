#!/bin/bash
for d in */;do
   for dd in $d;do
	echo dd is $dd
   	tar -cvf - "${dd%/}" | xz -9e -T8 -c > "${dd%/}.tar.xz" ;
   done
done

#for d in "*.tar";do echo $d;echo $d; xz -9e --threads=16 -c -> "${d}.xz"; done
