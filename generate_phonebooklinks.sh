function link() {
    #echo $1
    #echo $2
    wget --quiet -O - "https://services.sissa.it/phonebook/?query=$1+$2&yt0=Submit&type=person" | sed 's:.*href="/phonebook/person/\([0-9]*\).*:\1:;t;d'
    sleep 1

}

LIST=( 

  "Alessandro Silva (CM)"
  "Marco Serone (TPP)"
  "Annalisa Celotti ()"
  "Sergio Cecotti ()"
  "Cristian Micheletti ()" 
  "Roberto Trotta ()"
  )

for name_ in "${LIST[@]}"
do
    name_=($name_)
    name=${name_[@]:0:2}
    sector=${name_[@]:2:3}
    
    echo "<p><a href=\"https://services.sissa.it/phonebook/person/$(link $name)\" target=\"_blank\">${name}</a> ${sector}</p>"
done

