var fs = require("fs");
var csv = fs.readFileSync("pokemon.csv", "utf8");

var head = csv.split("\n")[0];
var pokes = csv.split("\n").slice(1).map(function(line){
  vars = line.split(",");
  var weight = Number(vars[16].slice(0,vars[16].indexOf(" ")));
  var ft_in = vars[17].replace(/[^\d']/g,'').split("'").map(Number);
  var height = (ft_in[0] + ft_in[1]/12)*0.3048;
  return {
    name: vars[3],
    type: vars[4],
    hp: Number(vars[9]),
    atk: Number(vars[10]),
    def: Number(vars[11]),
    spa: Number(vars[12]),
    spd: Number(vars[13]),
    spe: Number(vars[14]),
    weight: weight*0.453592,
    height: height
  };
});
fs.writeFileSync("dataset.csv", 
  "name,type,hp,atk,def,spa,spd,spe\n"
  + pokes.map(function(poke){
    return [poke.name, poke.type, poke.hp, poke.atk,
      poke.def, poke.spa, poke.spd, poke.spe].join(",");
  }).join("\n"))
