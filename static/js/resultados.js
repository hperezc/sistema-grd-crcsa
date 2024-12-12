function exportToPDF() {
    const evaluacionId = window.location.pathname.split('/').pop();
    if (!evaluacionId) {
        alert('No se pudo determinar la evaluación actual');
        return;
    }
    
    window.location.href = `/exportar-pdf/${evaluacionId}`;
} 