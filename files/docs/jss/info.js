/*
document.body.addEventListener("htmx:beforeRequest", function(event) {
    // Prüfen, ob das Formular das Event ausgelöst hat
    const form = event.target.closest("form");
    if (!form) return;

    // FormData in Objekt
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value,key) => {
      data[key] = key === "age" ? Number(value) : value;
    });

    // Browser-Validierung mit Ajv
    const valid = validate(data);
    if (!valid) {
      event.preventDefault(); // verhindert den Request
      alert("Fehler:\n" + validate.errors.map(e => e.instancePath.replace("/","") || e.params.missingProperty + " – " + e.message).join("\n"));
    }
  });


function checkform(form_name, schema_url) {
    document.body.addEventListener("htmx:beforeRequest", function(event) {
        const form = event.target.closest("form[name="+form_name+"]");
        if ( !form ) { return }
        fetch( schema_url, { 
            method: "GET", 
            headers: { 
                "Accept": "application/json",
                "Content-Type": "application/json"} 
        })
        .then( (response) => response.json() )
        .then( function(json) {     
            if( json["success"] == true ){            
                const form_name = "infomask";
                const ajv = new Ajv();
                const validate = ajv.compile(json["data"]);
                let data = {};
                for (let k in json["data"]["properties"]){
                    let selector = 
                        "form[name='"+form_name+"'] textarea[name='"+k+"'],"
                        + " form[name='"+form_name+"'] input[name='"+k+"']";
                    data[k] = document.querySelector(selector).value;
                }
                const valid = validate(data);                         
                if ( !valid ) {
                    event.preventDefault();
                    alert("Fehler:\n" + validate.errors.map(e => e.instancePath.replace("/","") || e.params.missingProperty + " – " + e.message).join("\n"));
                    console.log(validate.errors);
                } else {
                    console.log("Form data is valid");
                }  
            } 
            else {
                
            }
        })
        .catch(error => console.error("Fehler 'info' beim Laden:", error));        
    })
}

checkform("infomask", "/schema/info/form/");


function checkform() {
    fetch( "/schema/info/form/", { 
        method: "GET", 
        headers: { 
            "Accept": "application/json",
            "Content-Type": "application/json"} 
    })
        .then( (response) => response.json() )
        .then( function(json) { 
            if( json["error"] == false ){
                const form_name = "infomask";
                const ajv = new Ajv();
                const validate = ajv.compile(json["data"]);
                let data = {};
                for (let k in json["data"]["properties"]){
                    let selector = 
                        "form[name='"+form_name+"'] textarea[name='"+k+"'],"
                        + " form[name='"+form_name+"'] input[name='"+k+"']";
                    data[k] = document.querySelector(selector).value;
                }         
                // const valid = validate(formdata);   
                if ( !valid ) {
                    console.log(validate.errors);
                } else {
                    console.log("Form data is valid");
                }  
            } 
            else {
                
            }
        } )
        .catch(error => console.error("Fehler 'info' beim Laden:", error));        
}

checkform()

*/




function checkform(form_name, schema) {
alert(JSON.stringify(eingabe_schema))
  

}


