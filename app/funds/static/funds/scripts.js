document.addEventListener('DOMContentLoaded', (event) => {
    const rows = document.querySelectorAll('.clickable-row');
    rows.forEach(row => {
        row.addEventListener('click', () => {
            window.open(row.dataset.href, '_blank');
        });
    });
});