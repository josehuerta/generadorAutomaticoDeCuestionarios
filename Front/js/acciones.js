class visualizarArchivoPDF{

    constructor(){
        this.contenidoDeInteres=""
        this.lnPDF=0
    }


    visualizarArchivo=(url, canvasContainer)=>{
        const renderPage = (page) => {
            let viewport = page.getViewport(1.2);
            let canvas = document.createElement("canvas");
            let ctx = canvas.getContext("2d");
            let renderContext = {
            canvasContext: ctx,
            viewport: viewport,
            };
    
            canvas.height = viewport.height;
            canvas.width = viewport.width;
    
            canvasContainer.appendChild(canvas);
    
            page.render(renderContext);
        };

        const renderPages = (pdfDoc) => {
            
            for (let num = 1; num <= pdfDoc.numPages; num++){
                pdfDoc.getPage(num).then(renderPage);
            }
            this.lnPDF=pdfDoc.numPages
        };
    
        pdfjsLib.disableWorker = true;
        pdfjsLib.getDocument(url).then(renderPages);
        
    }

    obtenerContenido = (pdfUrl, pagInicial, pagFinal) => {
        let pdf = pdfjsLib.getDocument(pdfUrl);
        let texto=""
        texto=pdf.then(pdf => {
                // obtenemos todas las paginas del pdf
                let countPromises = []; // collecting all page promises
                for (let j = pagInicial; j <= pagFinal; j++) {
                    let page = pdf.getPage(j);
                    let txt = "";
                    countPromises.push(
                        page.then(function (page) {
                        // agregamos una pagina
                        let textContent = page.getTextContent()
                            return textContent.then(text=> {
                                // retornamos el contenido
                                return text.items
                                .map(function (s) {
                                    return s.str;
                                })
                                .join(" "); // unimos el contenido
                            })
                        })
                    )
                }
                // esperamos el contenido de todas las paginas
                return Promise.all(countPromises).then(texts =>{
                    let text=texts.join("");
                    let nText=text.replaceAll("- ","")
                    nText=nText.replaceAll("+","")
                    nText=nText.replaceAll("%","")
                    nText=nText.replaceAll(">","")
                    nText=nText.replaceAll("|","")
                    nText=nText.replaceAll("/Fig.[1-9]/","")
                    
                    return nText
                })
        })
        this.setContenido(texto)
        
    }
    setContenido(contenidoDeInteres){
        this.contenidoDeInteres=contenidoDeInteres
    }
    getContenido(){
        return this.contenidoDeInteres
    }
}

class Cuestionario{

    crearPDF=()=>{
        const pdf = new jsPDF();  
        const contenedorCuestionario=document.getElementById('cuestionario')
        if (contenedorCuestionario.hasChildNodes()){
            pdf.setFontSize(16)
            pdf.text(20,20,'Cuestionario')
            pdf.setFontSize(12)
            let preguntas=contenedorCuestionario.childNodes
            for (let i=0;i<preguntas.length;i++){
                console.log(preguntas[i])
                let pregunta=`${preguntas[i].textContent}`
                let x=20
                let y=(i+1)*8+20
                pdf.text(x,y, pregunta);
                // if (y>300){
                //     pdf.addPage()
                //     y=30
                // }
            }
            // https://es.stackoverflow.com/questions/193716/jspdf-salto-de-p%C3%A1gina
            // const container=$("#cuestionario").get(0) 
            // pdf.fromHTML(contenedorCuestionario, 15, 15, {
            //     width: 170,
            // }) 
        } 
    return pdf 
    }
    descargarCuestionario=()=>{
        const pdf=this.crearPDF()
        pdf.save("Cuestionario.pdf");
    }
}

objeto=new visualizarArchivoPDF()


const inFile = document.getElementById("inFile");

const rangePages = (totalPages) => {
    const pInicial = document.getElementById("pagInicial");
    const pFinal = document.getElementById("pagFinal");
    const valorMinimo = 1;    
    pInicial.setAttribute("value", valorMinimo);
    pInicial.setAttribute("min", valorMinimo);
    pInicial.setAttribute("max", totalPages);

    pFinal.setAttribute("min", valorMinimo);
    pFinal.setAttribute("max", totalPages);
};

//visualizacion del archivo PDF
inFile.addEventListener("change", (e) => {
    //creamos una url para el libro dentro de la app
    const path = URL.createObjectURL(inFile.files[0]); 
    //obtenemos el contenedor del libro
    const book = document.getElementById("book");
    if (book != null) {
        //si existe un libro que actualmente se visualiza y 
        //queremos ver otro eliminamos el existente
        book.remove();
    }
    //creamos contenedor para el nuevo libro a visualizar
    const newBook = document.createElement("div");
    newBook.setAttribute("id", "book");

    const bookContainer = document.getElementById("visualizarLibro");
    bookContainer.appendChild(newBook);
    

    
    //renderPDF(path, newBook);
    objeto.visualizarArchivo(path,newBook)
    //se abre la ventana modal con el libro dentro de ella
    rangePages(100);
    $("#modalLibro").modal('show')
});

//seleccion de las paginas de interes
//y obtencion del texto de las paginas de interes
const btnSeleccionarPaginas = document.getElementById(
    "seleccionarPaginas"
  );

btnSeleccionarPaginas.addEventListener("click", () => {
    let paginaInicial = parseInt(document.getElementById("pagInicial").value)
    let paginaFinal = parseInt(document.getElementById("pagFinal").value)
    let path = URL.createObjectURL(inFile.files[0])

    if (paginaInicial>100 || paginaFinal>100){
        alert("El numero de página es mayor al que contiene el libro")
    }
    else if(paginaInicial<1 || paginaFinal<1){
        alert("No hay numeros de página negativos")
    }
    else{
        objeto.obtenerContenido(path, paginaInicial, paginaFinal)
        objeto.getContenido().then((text) => {
            const contenedorTexto = document.getElementById(
            "contenidoSeleccionado"
            );
            contenedorTexto.innerText = text;
        });
        
        document.getElementById("close").click();
    }
    

});


const URLAPI="http://127.0.0.1:8000/api/generador/"

const btnCrearCuestionario=document.getElementById('crearCuestionario')
//obtenemos el texto seleccionado por el usuario
//objeto con especificaciones para llevar a cabo la peticion POST

btnCrearCuestionario.onclick=(e)=>{
    const URLAPI="http://127.0.0.1:8000/api/generador/"
    e.preventDefault()

    const textoLibro=document.getElementById('contenidoSeleccionado').value
    const peticionPOST={
        method:'POST',
        body:JSON.stringify({
            texto:textoLibro
        }),
        headers:{
            "Content-Type":"application/json"
            // las cabeceras ayudan a darle a la api una descripcion
            // de lo que se esta enviando
        }
        
    }
    fetch(URLAPI,peticionPOST)
    .then(response=>response.json())
    .then(preguntas=>{
        llenarCuestionario(preguntas.cuestionario)
        $("#btnVerCuestionario").show()
    })
    .catch(error=>{
        console.log(error)
        alert("¡ERROR AL CREAR CUESTIONARIO!")
    })
}

//Editar y descargar cuestionario
btnDescargarCuestionario=document.getElementById('descargarCuestionario')
cuestionario=new Cuestionario()
btnDescargarCuestionario.onclick=()=>{
    cuestionario.descargarCuestionario()
}


const llenarCuestionario=(cuestionario)=>{
    console.log(cuestionario)
    const contenedorCuestionario=document.getElementById('cuestionario')
    let lnPreguntas=cuestionario.length

    for(let i = contenedorCuestionario.childNodes.length - 1; i >= 0; --i) {
        contenedorCuestionario.removeChild(contenedorCuestionario.childNodes[i]);
      }

    console.log(contenedorCuestionario)
    for (let i=0;i<lnPreguntas;i++){
        // change the input to editable label
        // label with contenteditable=true
        const pregunta=document.createElement('label')
        pregunta.contentEditable=true
        pregunta.textContent=`${i+1}.-${cuestionario[i]}`
        // le agregamos una clase para el estilo de css
        pregunta.classList.add('pregunta')
        contenedorCuestionario.appendChild(pregunta)
    }
    $("#cuestionarioModal").modal('show')

}









