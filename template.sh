#!/bin/bash

# written by Riccardo Bertossa, 2020
# to compile the CSS code you need a sass compiler
# on ubuntu:
#    sudo apt install sass 
# put the text of the top and the urls of the images of the buttons 
# in the arrays BUTTON_TXT and BUTTON_IMG. in BUTTON_LINKS you put the target
# put the html code and the title of the longer sections in the arrays
# CONTENT and CONTENT_TITLE

#area buttons
#see button.sh for button style

BUTTON_TXT=(
"Astroparticle Physics"
"Astrophysics and Cosmology"
"Condensed Matter"
"Biological Systems"
"Statistical Physics"
"Teoretical Particle"
)
BUTTON_IMG=(
"img/bannerAPP_2.png"
"img/bannerAPC.jpg"
"img/bannerCM.jpg"
"img/logo_SBP.jpg"
"img/cropped-cropped-bannerOfficial3.png"
"img/cloudchamber.png"
)
BUTTON_IMG_POS=(
"center center"
"center center"
"center center"
"center center"
"center center"
"center center"
)

#remove after second " in vim:      s:\("[a-z.:/]*"\).*:\1:g
BUTTON_LINKS=(
"http://www.sissa.it/app/"
"http://www.sissa.it/ap/index.php"
"http://cm.sissa.it/"
"https://www.sissa.it/sbp/"
"http://www.statphys.sissa.it/wordpress/"
"http://www.sissa.it/tpp/index.php"
)



#various sections
#see content.sh for content style

CONTENT=(
"$(cat intro)"
"$(cat representative)"
"$(cat alumni)"
"$(cat grants)"
"$(cat convenzione)"
"$(cat excellence_coll)"
"$(cat colloquia)"
)
CONTENT_TITLE=(
"General info"
"Representatives"
"Alumni"
"Grants"
"Visiting students"
"Excellence collaborations"
"Colloquia and seminars"
)


#call routines that generates the html code
#every routine can add stuff to CSS and JS variables
#CSS variable is passed through sass


source button.sh #output in CONTENT_BUTTONS
source content.sh #output in CONTENT_HTML
source grants_css.sh #add more css for grants section in CSS


cat > out.html << EOF
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
$( echo "${CSS}" | sass --scss )
</style>
</head>
<body>
${CONTENT_BUTTONS}
${CONTENT_HTML}

<script>
${JS}
</script>

</body>
</html>
EOF
