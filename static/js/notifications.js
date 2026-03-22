document.addEventListener('DOMContentLoaded', () => {
    const data = document.getElementById('django-messages');
    if (!data) return;

    const messages = JSON.parse(data.textContent);

    messages.forEach(msg => {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center border-0 bg-${msg.level} text-white`;
        toast.role = 'alert';
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${msg.text}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        document.getElementById('toast-container').appendChild(toast);

        new bootstrap.Toast(toast, { autohide: true, delay: 4000 }).show();
    });
});