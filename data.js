// Datos iniciales de ejemplo — discografía principal de The Rolling Stones.
// Esto es una primera aproximación: se puede completar/corregir con la lista definitiva
// (ediciones UK/US, EPs, singles, directos, recopilatorios, etc.)
const ALBUMS_SEED = [
  { id: "1964-trs", year: 1964, title: "The Rolling Stones", type: "Estudio" },
  { id: "1965-no2", year: 1965, title: "The Rolling Stones No. 2", type: "Estudio" },
  { id: "1965-ooh", year: 1965, title: "Out of Our Heads", type: "Estudio" },
  { id: "1966-aftermath", year: 1966, title: "Aftermath", type: "Estudio" },
  { id: "1967-btb", year: 1967, title: "Between the Buttons", type: "Estudio" },
  { id: "1967-satanic", year: 1967, title: "Their Satanic Majesties Request", type: "Estudio" },
  { id: "1968-beggars", year: 1968, title: "Beggars Banquet", type: "Estudio" },
  { id: "1969-letitbleed", year: 1969, title: "Let It Bleed", type: "Estudio" },
  { id: "1970-getyerya", year: 1970, title: "Get Yer Ya-Ya's Out!", type: "Vivo" },
  { id: "1971-stickyfingers", year: 1971, title: "Sticky Fingers", type: "Estudio" },
  { id: "1972-exile", year: 1972, title: "Exile on Main St.", type: "Estudio" },
  { id: "1973-goatshead", year: 1973, title: "Goats Head Soup", type: "Estudio" },
  { id: "1974-itsonlyrocknroll", year: 1974, title: "It's Only Rock 'n Roll", type: "Estudio" },
  { id: "1976-blackandblue", year: 1976, title: "Black and Blue", type: "Estudio" },
  { id: "1977-loveyoulive", year: 1977, title: "Love You Live", type: "Vivo" },
  { id: "1978-somegirls", year: 1978, title: "Some Girls", type: "Estudio" },
  { id: "1980-emotionalrescue", year: 1980, title: "Emotional Rescue", type: "Estudio" },
  { id: "1981-tattooyou", year: 1981, title: "Tattoo You", type: "Estudio" },
  { id: "1982-stillife", year: 1982, title: "Still Life", type: "Vivo" },
  { id: "1983-undercover", year: 1983, title: "Undercover", type: "Estudio" },
  { id: "1986-dirtywork", year: 1986, title: "Dirty Work", type: "Estudio" },
  { id: "1989-steelwheels", year: 1989, title: "Steel Wheels", type: "Estudio" },
  { id: "1991-flashpoint", year: 1991, title: "Flashpoint", type: "Vivo" },
  { id: "1994-voodoolounge", year: 1994, title: "Voodoo Lounge", type: "Estudio" },
  { id: "1997-bridgestobabylon", year: 1997, title: "Bridges to Babylon", type: "Estudio" },
  { id: "1998-noisecure", year: 1998, title: "No Security", type: "Vivo" },
  { id: "2005-abiggerbang", year: 2005, title: "A Bigger Bang", type: "Estudio" },
  { id: "2008-shineliight", year: 2008, title: "Shine a Light", type: "Vivo" },
  { id: "2016-bluelonesome", year: 2016, title: "Blue & Lonesome", type: "Estudio" },
  { id: "2023-hackneydiamonds", year: 2023, title: "Hackney Diamonds", type: "Estudio" },
  { id: "1966-bigshits", year: 1966, title: "Big Hits (High Tide and Green Grass)", type: "Recopilatorio" },
  { id: "1971-hotrocks", year: 1971, title: "Hot Rocks 1964–1971", type: "Recopilatorio" },
  { id: "1975-madeinshade", year: 1975, title: "Made in the Shade", type: "Recopilatorio" },
  { id: "1993-jumpback", year: 1993, title: "Jump Back", type: "Recopilatorio" },
  { id: "2002-forty licks", year: 2002, title: "Forty Licks", type: "Recopilatorio" },
  { id: "2012-grrr", year: 2012, title: "GRRR!", type: "Recopilatorio" },
];

// Cada álbum puede tener: owned (bool), format (string), notes (string).
// Ese estado se guarda aparte (localStorage) para no pisar los datos base.
