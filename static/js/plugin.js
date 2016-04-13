//we define global variables
var obj = "";
var str = "";

function success(result) {
    document.getElementById("warnings").innerHTLM="";
    //to be changed ; see with Simon (Pierre)
    result2= "{\"disamb\" : " + result + "}";
    obj = JSON.parse(result2);
    obj.disamb.sort(function(a,b){return a.begin-b.begin;});
    str = $("#ambiguous_text").val();
    var nhtml = "";
    var prec=0;
    for(i=0; i<obj.disamb.length; i++){
        nhtml += str.substring(prec,obj.disamb[i].begin);
        nhtml += "<a href=\"" + obj.disamb[i].url + "\" target=\"_blank\">";
        nhtml += str.substring(obj.disamb[i].begin, obj.disamb[i].end);
        nhtml += "</a>";
        prec = obj.disamb[i].end;
    }
    nhtml += str.slice(prec);
    document.getElementById("disambiguated_text").innerHTML = nhtml;
    document.getElementById("checkButton").style.display="block";
    document.getElementById("checkmodeButton").style.display="block";
}


function submit_success(result) {
    alert("Thank you for your support!");
}
function disambiguate() {
    var str = $("#ambiguous_text").val();
    var request = $.post("/disambiguate.json", {"text" : str});
    request.success(success);
    request.fail(function(){document.getElementById("warnings").innerHTML="Error"});
}
function erase(){
    document.getElementById("ambiguous_text").value="";
    document.getElementById("disambiguated_text").innerHTML="";
}

function checkmode(){
    // var request = $.post("/check-disambiguate.json", JSON.stringify(obj));
    // request.success(check_success);
    // request.fail(function(){document.getElementById("warnings").innerHTML="Checkmode Error"});
    document.getElementById("checkButton").innerHTML = "Now everything is OK!"
    document.getElementById("checkmodeButton").style="display:none;"
    
    var possible_senses = [];
    for(i=0; i<obj.disamb.length; i++) {
        possible_senses.push(obj.disamb[i].all_senses);
    }
    var nhtml = "";
    var prec=0;
    for(i=0; i<obj.disamb.length; i++){
        nhtml += str.substring(prec, obj.disamb[i].begin, obj.disamb[i].end);
        nhtml += "<select id=\"selection" + i + "\">";
        for(j=0; j < possible_senses[i].length; j++){
            nhtml += "<option";
            if(j == obj.disamb[i].sense_index){
                nhtml += " selected";
            }
            nhtml += ">" + possible_senses[i][j] + "</option>";
        }
        nhtml += "</select>";
        prec= obj.disamb[i].end;
    }
    nhtml += str.slice(prec);
    document.getElementById("disambiguated_text").innerHTML = nhtml;
}
function checked(){
    // Text to add to the corpus in case of 
    var str = $("#ambiguous_text").val();
    // Send to server
    if (document.getElementById("checkButton").innerHTML=="Everything is OK!"){
        //Send the fact that the given senses were right
        alert("TODO : send this information to server");
    }
    else{
        //Send the corrections
        var corrections = [];
        for(i=0; i<obj.disamb.length; i++){
            corrections.push(document.getElementById("selection" + i).selectedIndex);
        }
        console.log(corrections);
        if (obj) {
            var disambiguation = JSON.stringify(obj);
        } else {
            var disambiguation = "";
        }
        var request = 
            $.post("/submit-corrections.json",
                   {"text" : str,
                    "disambiguation" : disambiguation,
                    "sense_indices" : JSON.stringify(corrections)});
        request.success(submit_success);
        request.fail(function(){document.getElementById("warnings").innerHTML="Submission Error"});
    }
}
