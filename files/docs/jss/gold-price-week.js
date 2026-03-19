function gold_price_present_init(json) {
    gold_price_present_dia_2d(json);
    document.querySelector("#btn-3d").disabled = false;
    document.querySelector("#btn-2d").addEventListener("click", function() {            
        document.querySelector("#btn-2d").disabled = true;
        document.querySelector("#goldprice-2d").hidden = false;
        document.querySelector("#btn-3d").disabled = false;
        document.querySelector("#goldprice-3d").hidden = true;
        gold_price_present_dia_2d(json);
    });

    document.querySelector("#btn-3d").addEventListener("click", function() {
        document.querySelector("#btn-2d").disabled = false;
        document.querySelector("#goldprice-2d").hidden = true;
        document.querySelector("#btn-3d").disabled = true;
        document.querySelector("#goldprice-3d").hidden = false;
        gold_price_present_dia_3d(json);
    });        
}    

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

function gold_price_present_dia_3d(json) {
    /*
    const x = [0,1,2,3,4,5,6,7,8,9];
    const y = ["Mo", "Di", "Mi", "Do", "Fr"];
    const z = [
    [12, 11, 10,  9,  8,  9, 10, 11, 12, 13],
    [11, 10,  9,  7,  6,  7,  9, 10, 11, 12],
    [10,  9,  7,  5,  4,  5,  7,  9, 10, 11],
    [11, 10,  9,  7,  6,  7,  9, 10, 11, 12],
    [12, 11, 10,  9,  8,  9, 10, 11, 12, 13]
    ];
    */

    const x = [];
    const y = [];
    const z = [];

    for( let first in json["data"]["list"] ) {
        y.push(json["data"]["list"][first]["day"]);
        let t = [];
        for( let second in json["data"]["list"][first]["list"] ) {
            x.push(second);
            t.push( json["data"]["list"][first]["list"][second] );            
        }
        z.push( t );
    }

    const surface = {
        x: x, y: y, z: z,
        type: 'surface',
        colorscale: 'Viridis',
    };

    const layout = {
    title: 'Preisentwuicklung über eine Woche',
    paper_bgcolor: '#333333',
    plot_bgcolor:'#333333',
    scene: {
        xaxis: { title: 'Zeit', color: '#efefef' },
        yaxis: { title: 'Tag', color: '#efefef' },
        zaxis: { title: 'Preis', color: '#efefef' }
    }
    };

    Plotly.newPlot('goldprice-3d', [surface], layout);

}

function gold_price_present_dia_2d(json) {
    const colors = ["#00E5FF", "#39FF14", "#000000", "#FFFFFF", "#FFFF00", "#FF5F1F", "#FF073A"];

    const list = json["data"]["list"];
    let days = [];
    let data = [];
    let labels = [];
    
    for( let d in list ){
        let day = list[d]["day"];
        let data = [];
        let labels = [];
        console.log( list );
        for( c in list[d]["list"] ){        
            labels.push( c.substr(0,5) );            
            data.push( list[d]["list"][c] );
        }
        
        days.push({
            x: labels,
            y: data,
            type: 'scatter',
            mode: 'lines',             
            name: day,
            line: { 
                color: colors.shift(), 
                width: 1
            }

        });
    }
    Plotly.newPlot('goldprice-2d', days, 
        {
            paper_bgcolor: '#333333',
            plot_bgcolor:'#333333',
            margin: { l: 45, r: 15, t: 40, b: 55 },
            title: {
                text : 'gold price', 
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
            legend: { font: { color: "white" } }
        }
    );
}
