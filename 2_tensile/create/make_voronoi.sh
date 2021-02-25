# reference: https://atomsk.univ-lille.fr/tutorial_polycrystal.php
atomsk --create fcc 4.046 Al al_fcc_unit.lmp
atomsk --polycrystal al_fcc_unit.lmp settings.txt Al_polycrystal.lmp -wrap
