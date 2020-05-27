CSS="${CSS}

\$bg: #3c3c3c;
\$white: #ffffff;
\$black: #202121;
\$button-color: #ffaaaa;

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
  justify-content: center;
  margin: 0;
  min-height: 10vh;
  background: \$bg;
}

.area-button {
  position: relative;
  float: left;
  min-height: 10vh;
  min-width: 10vw;
  display: inline-block;
  cursor: pointer;
  outline: none;
  border: 0;
  vertical-align: middle;
  text-decoration: none;
  font-size: inherit;
  font-family: inherit;
  & {
    @include transition(all, 0.5s, cubic-bezier(0.65,-0.25,0.25,1.95));
    font-weight: 900;
    color: \$button-color;
    padding: 1.25rem 2rem;
    background: \$white;
    text-transform: uppercase;
    &:hover, &:focus, &:active {
      letter-spacing: 0.125rem;
    }
  }
}

/*
@supports (display: grid) {
  .button-div {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 0.625rem;
    grid-template-areas: \". main main .\" \". main main .\";
  }
  
  #container {
    grid-area: main;
    align-self: center;
    justify-self: center;
  }
}
*/
"

function button() {
TEXT=$1
IMG=$2
LINK=$3
echo "
<div id=\"container\">
  <a href='${LINK}' target='_blank'><button class=\"area-button\" style=\"background: url('${IMG}') no-repeat center center;\">${TEXT}</button></a>
</div>
"

}

CONTENT_BUTTONS="<div class='button-div'>"
for idx in "${!BUTTON_TXT[@]}"; do
CONTENT_BUTTONS="${CONTENT_BUTTONS}
$(button "${BUTTON_TXT[$idx]}" "${BUTTON_IMG[$idx]}" "${BUTTON_LINKS[$idx]}")
"
done
CONTENT_BUTTONS="${CONTENT_BUTTONS}
</div>
"

