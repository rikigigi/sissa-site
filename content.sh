CONTENT_HTML=""
for idx in "${!CONTENT[@]}"; do
CONTENT_HTML="${CONTENT_HTML}
<button class='collapsible'>${CONTENT_TITLE[$idx]}</button>
<div class='content'>
${CONTENT[$idx]}
</div>
"
done

CSS="${CSS}
\$pale-red:#ffdddd;
\$pale-yellow:#ffffcc;
\$pale-blue:#ddffff;
\$pale-green:#ddffdd;
\$sand:#fdf5e6;
\$collapsible-color: rgba(101, 128, 180, 1.0);
\$collapsible-color-bright: rgba(101, 128, 180, 0.75);


\$content_bkg: #f1f1f1;
\$grad_height: 75px;
\$grant_height: 150px;

.collapsible {
  background-color: \$collapsible-color;
  color: white;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.active, .collapsible:hover {
  background-color: \$collapsible-color-bright;
}

.content {
  width: 100%;
  padding: 0 18px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
  background-color: \$content_bkg;
}
div .block {
  border: 1px solid black;
  padding: 5px;
  margin: 5px;
}
/*
div .sp {
  background-color: \$pale-red;
}

div .tpp {
  background-color: \$pale-yellow;
}
div .app {
  background-color: \$pale-blue;
}

div .cm {
  background-color: \$pale-green;
}
div .ap {
  background-color: \$sand;
}
*/

.grant_m{
height: \$grant_height;
padding-bottom: 30px;
}
.grant_f{
position: relative;
top: -\$grad_height;
background: linear-gradient(0deg, \$content_bkg, transparent);
height: \$grad_height;
}
.grant_c{
/*height: \$grant_height;*/
overflow: hidden;
}
.grant_title{
text-align: center;
font-weight: 900;
}

a.grant_title_link {
    text-decoration: none;
    color: inherit;
    background: inherit;
}
"

JS="${JS}

function collapsible() {
var coll = document.getElementsByClassName('collapsible');
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener('click', function() {
    this.classList.toggle('active');
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + 'px';
    } 
  });
}
}
document.addEventListener('DOMContentLoaded', collapsible);


function grant_layout(){
  var coll = document.getElementsByClassName('grant_m');
  var i;
  for (i=0;i<coll.length;i++) {
    all=coll[i];
    content=all.getElementsByClassName('grant_c')[0]
    hider=all.getElementsByClassName('grant_f')[0]
    if (content.scrollHeight < 150 ) {
       all.style.height = content.scrollHeight + 'px';
       hider.style.display = 'none';
    } else {
       content.style.height = '150px';
    }

  }
}

document.addEventListener('DOMContentLoaded', grant_layout);



"


