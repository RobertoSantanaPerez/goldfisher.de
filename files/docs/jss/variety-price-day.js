function variety_price_present_text(json) {
    document.querySelector("#variety-price").value = 
        json["data"]["amount"] + " " + json["data"]["currency"];
    document.querySelector("#variety-price-min").value = 
        json["data"]["min"] + " " + json["data"]["currency"];
    document.querySelector("#variety-price-max").value = 
        json["data"]["max"] + " " + json["data"]["currency"];
    let diff = parseInt( (json["data"]["max"]-json["data"]["min"]) * 100 + 0.5 )/100;
    diff = diff.toFixed(2);
    document.querySelector("#variety-price-diff").value =     
        diff + " " + json["data"]["currency"];
    document.querySelector("#date-time").value =
        json["data"]["date"] + ", " + json["data"]["time"].substr(0, 5);
    document.querySelector("#exchange-rate").value =
        json["data"]["rate"];
    document.querySelector("#info").value =
        ( json["data"]["info"] === undefined
            || json["data"]["info"] == null 
            || json["data"]["info"].length <= 0)                
        ? ""
        : json["data"]["info"];

    let suggestedMin = json["data"]["min"] * 0.998;
    suggestedMin = suggestedMin/10;
    suggestedMin = suggestedMin*10;
}

function get_colors(name) {
    colors = {
        "gold"      : "#CCFF00",        
        "silver"    : "#c0c0c0",
        "copper"    : "#FF5F1F",
        "platinum"  : "#00E5FF",
        "palladium" : "#B026FF"
    };
    if (Object.hasOwn(colors, name)) {
        return colors[name];
    }    
    return("#00FFD5");
}1

function variety_price_present_dia(json, material) {       
    let  material_kurz = material.replace(/treasury_(\d+)y/g, "UST $1y");
    material_kurz = material_kurz.replace(/fed_funds/g, "F-F");
    material_kurz = material_kurz.replace(/copper/g, "Cu");
    material_kurz = material_kurz.replace(/silver/g, "Ag");
    material_kurz = material_kurz.replace(/gold/g, "Au");
    material_kurz = material_kurz.replace(/platinum/g, "Pt");
    material_kurz = material_kurz.replace(/palladium/g, "Pd");
    const list_c = json["data"]["list_price"];
    let labels = [];    
    let price = [];    
    let average = [];
    let minimum = [];
    let maximum = [];
    document.querySelector("#variety_"+material+"_current").textContent = parseFloat(json["data"]["amount"]).toFixed(2);
    for (l in list_c) {    
      labels.push(l);
      price.push(list_c[l]);
      average.push(json["data"]["average"]);
      minimum.push(json["data"]["min"]);
      maximum.push(json["data"]["max"]);            
    }
    
    current = {
        x: labels,
        y: price,
        type: 'scatter',
        mode: 'lines',             
        line: { 
            color: get_colors(material), 
            width: 3 }
    };
    average = {
        x: labels,
        y: average,
        type: 'scatter',
        mode: 'lines',             
        line: {             
            color: '#efefef', 
            dash: 'dash',
            width: 1 }
    };
    minimum = {
        x: labels,
        y: minimum,
        type: 'scatter',
        mode: 'lines',             
        line: { 
            color: '#efefef', 
            dash: 'dash',
            width: 1 }
    };
    maximum = {
        x: labels,
        y: maximum,
        type: 'scatter',
        mode: 'lines',             
        line: { 
            color: '#efefef', 
            dash: 'dash',
            width: 1 }
    };
    Plotly.newPlot('price_'+material, [ current, average, minimum, maximum ], 
    {
        showlegend: true,
        paper_bgcolor: '#333333',
        plot_bgcolor:'#333333',
        margin: { l: 45, r: 15, t: 40, b: 55 },
        title: {
            text : material_kurz+' $/5min', 
            font: { color: get_colors(material), size: 24 }
        },
        xaxis: {
        title: { text: 'time', font: { color: '#efefef' } },
        tickfont: { color: '#efefef' }
    },
    yaxis: {
        title: { text: 'price', font: { color: '#efefef' } },
        tickfont: { color: '#efefef' }
    },
    });
}