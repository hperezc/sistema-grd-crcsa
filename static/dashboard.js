document.addEventListener('DOMContentLoaded', function() {
    const tooltipContainers = document.querySelectorAll('.tooltip-container');
    
    tooltipContainers.forEach(container => {
        const tooltip = container.querySelector('.custom-tooltip');
        
        container.addEventListener('mouseenter', (e) => {
            // Obtener las dimensiones y posición del contenedor
            const containerRect = container.getBoundingClientRect();
            const tooltipRect = tooltip.getBoundingClientRect();
            
            // Calcular la posición óptima
            let left = containerRect.left;
            let top = containerRect.top - tooltipRect.height - 10;
            
            // Ajustar si se sale por la derecha
            if (left + tooltipRect.width > window.innerWidth) {
                left = window.innerWidth - tooltipRect.width - 20;
            }
            
            // Ajustar si se sale por arriba
            if (top < 0) {
                top = containerRect.bottom + 10;
                tooltip.style.bottom = 'auto';
                tooltip.style.top = top + 'px';
            } else {
                tooltip.style.top = top + 'px';
            }
            
            tooltip.style.left = left + 'px';
        });
    });
}); 