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

.collapsible {
  background-color: #777;
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
  background-color: #555;
}

.content {
  padding: 0 18px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
  background-color: #f1f1f1;
}
div .block {
  border: 1px solid black;
  padding: 20px;
  margin: 20px;
}
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
"

JS="
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
"

