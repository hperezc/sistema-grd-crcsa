function exportarPDF(evaluacionId) {
    // Mostrar spinner
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border text-danger';
    spinner.setAttribute('role', 'status');
    
    const button = document.querySelector('#exportar-btn');
    button.disabled = true;
    button.innerHTML = '';
    button.appendChild(spinner);
    button.appendChild(document.createTextNode(' Generando PDF...'));

    // Iniciar descarga
    window.location.href = `/exportar_pdf/${evaluacionId}`;

    // Restaurar botón después de un tiempo razonable
    setTimeout(() => {
        button.disabled = false;
        button.innerHTML = 'Exportar PDF';
    }, 5000);
} 