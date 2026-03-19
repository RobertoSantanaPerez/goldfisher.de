function title() {
    fetch( "/srv/title/", { 
        method: "GET", 
        headers: { 
            "Accept": "application/json",
            "Content-Type": "application/json"} 
    })
        .then( (response) => response.json() )
        .then( function(json) { 
            document.title = json["data"]["current"] + " " + json["data"]["trend"];
            document.querySelector("#now").value = 
                json["data"]["local-date"] + ", " +
                    json["data"]["local-time"].substr(0, 5);            
        } )
        .catch(error => console.error("Fehler 'day_prices' beim Laden:", error));        
        window.setTimeout( title, config()["timeout_refresh"] )
    }//title

stash["onload_subs"].push(function () { title(); });

window.onload = function () {
    stash["onload_subs"].forEach(fn => {
        if (typeof fn === "function") { fn(); }
    });
};