var vetorCandidatos = [];

function sendPostData(inputJson, url)
{
    // Sending and receiving data in JSON format using POST method
    //
    var xhr = new XMLHttpRequest();
    //var url = "url";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          var outputJson = JSON.parse(xhr.responseText);
          console.log("saida: "+JSON.stringify(outputJson));
          //console.log(json.email + ", " + json.password);
      }else
      {
        console.log("readyState"+xhr.readyState);
        console.log("status"+xhr.status)
      }
    };
    //var data = JSON.stringify({"email": "hey@mail.com", "password": "101010"});
    console.log("send post");
    xhr.send(JSON.stringify(inputJson));
}

function runBRKGA()
{
  var inputJson = {};
  inputJson.n = document.getElementById("txtN").value; //20;
  inputJson.m = document.getElementById("txtM").value; //8;
  inputJson.p = document.getElementById("txtP").value; //20;
  inputJson.elite = document.getElementById("txtElite").value;//4;
  inputJson.mutant = document.getElementById("txtMutant").value;//2;
  inputJson.k = document.getElementById("txtK").value;//10;
  inputJson.S = document.getElementById("txtS").value; //1;
  inputJson.cover = document.getElementById("txtType").checked;//false;
  inputJson.locals = vetorCandidatos;
  
  console.log(JSON.stringify(inputJson));
  var URL = "https://sad-covid-19.herokuapp.com/brkga";
  sendPostData(inputJson, URL); 
}

function preencherTabela()
{
    var candidato = new Object();  
    candidato.nome         = document.getElementById("name").value;
    candidato.custo        = document.getElementById("custo").value;
    candidato.municipio    = document.getElementById("municipio").value;

    vetorCandidatos.push(candidato);

    showData();
    
}

function remover (i)
{
    vetorCandidatos.splice(i,1);
    showData();
}

function showData()
{
    var divCad = document.getElementById("cadastrados");
    var code= "<table class=\"w3-table-all\" >";
    
    code += "<tr class=\"w3-red\" ><th> ID </th><th> Nome </th> <th> Custo (R$) </th> <th> Municipio </th> <th> Remover </th> </tr>";
    var i;
    for(i = 0; i < vetorCandidatos.length; i++)
    {
        code += "<tr><td>"+ i +" </td><td>" +vetorCandidatos[i].nome +"</td> <td>"+ vetorCandidatos[i].custo +"</td> <td>"+ vetorCandidatos[i].municipio+"</td> <td><input class=\"w3-btn w3-blue\" type=\"button\" id= \"btRemover\" value=\"Remover\" onclick=\"remover("+i+")\"/> </td></tr>";
    }
    code += "</table>"
    console.log(code);
    divCad.innerHTML = code;
    //adicionar o titulo da tabela
    var titulo = document.getElementById("titulo");
    titulo.innerHTML = "Lista de locais candidatos: "+i;
}

function configurar() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}
