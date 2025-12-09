# M6

# Compte-rendus

## 2025_12_01

Je rencontre de nombreux problèmes pour faire fonctionner l'écran de la "tablette" de M6.6 - Obsolescence Programmée.
Côté hardware, c'est cet écran : https://www.gotronic.fr/art-ecran-tactile-7-27-27-hdmi-46521.htm

- Ma première solution était d'utiliser un player vidéo. Mais il ne reconnait pas bien l'écran, et il n'est pas possible de forcer la bonne résolution (1024x600).

- J'essaye donc d'utiliser une raspi4 connectée à l'écran et lançant une simple vidéo au démarrage. J'en profite pour essayer Pipresents. Mais l'écran ne marche pas non plus, avec un bug particulièrement surpreprenant :
	- Il est possible de faire fonctionner l'écran en suivant cette démarche TRES PRECISEMENT :
		1 - Debrancher tous les cables
		2 - Allumer la pi4
		3 - Brancher le cable mini-HDMI à HDMI 0
		4 - Seulement après, brancher l'alim USB sur un posrt USB 3.0 (très important !) de la raspi 
		Là, l'écran s'allume et affiche le bureau de la pi. Mais un simple reboot ne fonctionne plus.


