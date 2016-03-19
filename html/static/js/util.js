function revisarLetras(e) {
    var allow = ' a\u00E1bcde\u00E9fghi\u00EDjklmn\u00F1o\u00F3pqrstu\u00FAvwxyzA\u00C1BCDE\u00C9FGHI\u00CDJKLMN\u00D1O\u00D3PQRSTU\u00DAVWXYZ';
    var key = e.charCode || e.keyCode || e.which || 0;
    
    return allow.indexOf(String.fromCharCode(key)) != -1;
}

function revisarLetrasNumeros(e) {
    var allow = ' a\u00E1bcde\u00E9fghi\u00EDjklmn\u00F1o\u00F3pqrstu\u00FAvwxyzA\u00C1BCDE\u00C9FGHI\u00CDJKLMN\u00D1O\u00D3PQRSTU\u00DAVWXYZ0123456789';
    var key = e.charCode || e.keyCode || e.which || 0;
    
    return allow.indexOf(String.fromCharCode(key)) != -1;
}

function revisarNumeros(e) {
    var allow = '0123456789';
    var key = e.charCode || e.keyCode || e.which || 0;
    
    return allow.indexOf(String.fromCharCode(key)) != -1;
}

function revisarTelefono(e) {
    var allow = '0123456789';
    var key = e.charCode || e.keyCode || e.which || 0;
    
    return allow.indexOf(String.fromCharCode(key)) != -1;
}

function obtenerCampo(forma, campoNombre, campoValor) {
  var indice, campo, lista;

  lista = forma.elements;  
  for (indice = 0; indice < lista.length; indice++) {    
    campo = lista[indice];
	if ((campo.constructor != null) && campo.constructor.name == 'HTMLCollection') {
	  lista = campo;
	  for (indice = 0; indice < lista.length; indice++) {  
	    campo = lista[indice];
		if (campo && (campoNombre == campo.name) && ((campoValor == null) || (campoValor == campo.value))) {
		  return campo;
		}
	  }
	} else {
      if (campo && (campoNombre == campo.name) && ((campoValor == null) || (campoValor == campo.value))) {
	    return campo;
	  }
	}
  }
}

function limpiarSelect(select) {
  while (select.childNodes.length > 0) {
    select.removeChild(select.childNodes[0]);
  }
}
