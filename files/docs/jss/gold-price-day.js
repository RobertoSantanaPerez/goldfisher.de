function gold_price_present_text(json) {
    document.querySelector("#gold-price").value = 
        json["data"]["amount"] + " " + json["data"]["currency"];
    document.querySelector("#gold-price-min").value = 
        json["data"]["min"] + " " + json["data"]["currency"];
    document.querySelector("#gold-price-max").value = 
        json["data"]["max"] + " " + json["data"]["currency"];
    let diff = parseInt( (json["data"]["max"]-json["data"]["min"]) * 100 + 0.5 )/100;
    diff = diff.toFixed(2);
    document.querySelector("#gold-price-diff").value =     
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
function gold_price_present_dia(json) {    
    const list_c = json["data"]["list_price"];
    let labels = [];    
    let price = [];    
    let average = [];
    let minimum = [];
    let maximum = [];
    document.querySelector("#gold-price").textContent = parseFloat(json["data"]["amount"]).toFixed(2);
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
            color: '#CCFF00',
            width: 1 }
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
    Plotly.newPlot('goldprice', [ current, average, minimum, maximum ], 
    {
        showlegend: true,
        paper_bgcolor: '#333333',
        plot_bgcolor:'#333333',
        margin: { l: 45, r: 15, t: 40, b: 55 },
        title: {
            text : 'gold $/1min', 
            font: { color: '#ffd700', size: 24 }
        },
        xaxis: {
        title: { text: 'time', font: { color: '#efefef' } },
        tickfont: { color: '#efefef' }      // Achsen-Ticks
    },
    yaxis: {
        title: { text: 'price', font: { color: '#efefef' } },
        tickfont: { color: '#efefef' }
    },
    });
}