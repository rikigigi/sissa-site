CSS="${CSS}

\$bg: transparent;
\$button-color: rgba(101, 128, 180, 0.0);
\$button-text-color: rgba(255, 255, 255, 1.0);

@mixin transition(\$property: all, \$duration: 0.5s, \$ease: cubic-bezier(0.65,-0.25,0.25, 1.95)) {
  transition: \$property \$duration \$ease;
}

/*
.button-div > * {
  box-sizing: border-box;
  &::before, &::after {
    box-sizing: border-box;
  }
}
*/
.button-div {
  font-family: 'Roboto', sans-serif;
  font-size: 1rem;
  line-height: 1.5;
  display: block;
  align-items: center;
  text-align: center;
  justify-content: center;
  margin: 0;
  min-height: 10vh;
  background: \$bg;
}

.area-button-a{
  background-color: transparent;
  vertical-align: middle;
}

.area-button {
  background: \$button-color;
  position: relative;
  /*height: 10ch;
  width: 30ch;*/
  display: inline-block;
  cursor: pointer;
  outline: none;
  border: 0px solid \$button-color;
  vertical-align: middle;
  text-decoration: none;
  font-size: inherit;
  font-family: inherit;
  & {
    /*@include transition(all, 0.5s, cubic-bezier(0.65,-0.25,0.25,1.95));*/
    font-weight: 900;
    /*color: \$button-color;*/
    color: \$button-text-color;
    padding: 0.625rem 1rem;
    margin: 0.5rem;
    text-transform: uppercase;
    &:hover, &:focus {
      font-weight: 1500; 
      /*letter-spacing: 0.125rem;*/
    }
  }
}
  .container-btn {
  float: left;
  display: inline-block;
  /*
    grid-area: main;
    align-self: center;
    justify-self: center;*/
  }
.container-btn2 {
  height: 10ch;
  width: 30ch;
  text-align: center;
  display: table;
}

.inside-btn {
  display: table-cell;
  text-align: center;
  vertical-align: middle;
}
span.clear {
  clear:both;
  display:block;
}

/*
@supports (display: grid) {
  .button-div {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 0.625rem;
    grid-template-areas: \". main main .\" \". main main .\";
  }
  
}
*/
"

function button() {
TEXT=$1
IMG=$2
LINK=$3
POS=$4
echo "
<div class=\"container-btn\" style=\"background: url('${IMG}') no-repeat ${POS};background-size: cover;\"><div class='container-btn2'> 
<div class='inside-btn'><a class='area-button-a' href='${LINK}' target='_blank' ><button class=\"area-button\" >${TEXT}</button></a>
</div></div></div>
"

}

CONTENT_BUTTONS="<div class='button-div'>"
for idx in "${!BUTTON_TXT[@]}"; do
CONTENT_BUTTONS="${CONTENT_BUTTONS}
$(button "${BUTTON_TXT[$idx]}" "${BUTTON_IMG[$idx]}" "${BUTTON_LINKS[$idx]}" "${BUTTON_IMG_POS[$idx]}")
"
done
CONTENT_BUTTONS="${CONTENT_BUTTONS}
<span class=\"clear\"></span></div>
"

JS="${JS}
function update_buttons_width(){
   var btn_div=document.getElementsByClassName('button-div');
   var i;
   for (i=0;i<btn_div.length;i++) {
      var btns=btn_div[i];
      var width=btns.clientWidth;
      var n_btn_line=(width/275.0)|0;
      if (n_btn_line==0) return;
      var btn_width=width/n_btn_line;
      var btn_inner_width=btn_width-5;
      var btn_all=btns.getElementsByClassName('container-btn');
      var j
      for (j=0;j<btn_all.length;j++) {
         var btn=btn_all[j];
         btn.style.width=(btn_inner_width|0) + 'px';
      }
   }
}
window.addEventListener('resize',update_buttons_width);
document.addEventListener('DOMContentLoaded', update_buttons_width);
//update_buttons_width();
"
