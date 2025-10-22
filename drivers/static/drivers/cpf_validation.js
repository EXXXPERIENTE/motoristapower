// C:\APPY\MotoristaPower\drivers\static\drivers\cpf_validation.js

function cleanCPF(cpf) {
    // Remove tudo que não for número (pontos, traços, espaços)
    return cpf.replace(/\D/g, '');
}

function validateCPFStructure(cpf) {
    const cleanedCpf = cleanCPF(cpf);

    if (cleanedCpf.length === 0) {
        // Se estiver vazio, não mostra erro (apenas limpa)
        return 'limpar';
    }

    if (cleanedCpf.length < 11) {
        return 'incompleto';
    }

    // Para esta validação front-end, 11 dígitos já é considerado "válido" estruturalmente.
    // A validação completa (dígitos verificadores) será feita pelo back-end (validate_cpf em Python).
    return 'valido';
}


document.addEventListener('DOMContentLoaded', function() {
    // Tenta encontrar o campo CPF pelo atributo name
    const cpfField = document.querySelector('input[name="cpf"]');

    if (cpfField) {
        // Adiciona um listener para quando o campo perder o foco (blur)
        cpfField.addEventListener('blur', function() {
            const result = validateCPFStructure(cpfField.value);

            // Remove as classes de validação anteriores
            cpfField.classList.remove('is-invalid', 'is-valid');

            // Encontra a div de feedback de erro
            const feedbackDiv = cpfField.nextElementSibling;
            if (feedbackDiv && feedbackDiv.classList.contains('invalid-feedback')) {
                 feedbackDiv.textContent = ''; // Limpa o texto de erro anterior
            }

            if (result === 'incompleto') {
                cpfField.classList.add('is-invalid');
                if (feedbackDiv) {
                    feedbackDiv.textContent = 'CPF deve ter 11 dígitos.';
                }
            } else if (result === 'valido') {
                cpfField.classList.add('is-valid');
            } else if (result === 'limpar') {
                 // Limpa apenas o visual sem adicionar erro
            }
        });

        // Adiciona um listener para formatar o campo enquanto o usuário digita (só permite números)
        cpfField.addEventListener('input', function(e) {
            e.target.value = cleanCPF(e.target.value);
        });
    }
});