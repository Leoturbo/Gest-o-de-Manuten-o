// Funções globais para todo o sistema
document.addEventListener('DOMContentLoaded', function() {
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Ativar tabs ao clicar em links com hash
    if (window.location.hash) {
        const tab = new bootstrap.Tab(document.querySelector(window.location.hash));
        tab.show();
    }
    
    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Máscaras para campos de formulário
    if (typeof IMask !== 'undefined') {
        // Máscara para telefone
        const telefoneFields = document.querySelectorAll('input[type="tel"]');
        telefoneFields.forEach(function(field) {
            IMask(field, {
                mask: '(00) 00000-0000'
            });
        });
        
        // Máscara para CPF/CNPJ
        const cpfCnpjFields = document.querySelectorAll('input[data-mask="cpf_cnpj"]');
        cpfCnpjFields.forEach(function(field) {
            IMask(field, {
                mask: [
                    { mask: '000.000.000-00', maxLength: 11 },
                    { mask: '00.000.000/0000-00' }
                ],
                dispatch: function(appended, dynamicMasked) {
                    const value = dynamicMasked.value + appended;
                    return value.length > 14 ? dynamicMasked.masks[1] : dynamicMasked.masks[0];
                }
            });
        });
    }
});

// Função para confirmar exclusões
function confirmarExclusao(event) {
    event.preventDefault();
    const form = event.target.closest('form');
    
    Swal.fire({
        title: 'Tem certeza?',
        text: "Esta ação não pode ser desfeita!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sim, excluir!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit();
        }
    });
}

// Função para exibir toast de notificação
function mostrarToast(tipo, mensagem) {
    const toastContainer = document.getElementById('toastContainer');
    
    if (!toastContainer) {
        console.error('Container de toasts não encontrado');
        return;
    }
    
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${tipo} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${mensagem}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
    
    // Remove o toast após ser escondido
    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}

// Função para carregar dados via AJAX
function carregarDados(url, callback) {
    fetch(url)
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => console.error('Erro ao carregar dados:', error));
}