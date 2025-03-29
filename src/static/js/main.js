/**
 * Script principal para o sistema de cálculo de desperdício
 */
document.addEventListener('DOMContentLoaded', function () {
    // Elementos do DOM
    const form = document.getElementById('wasteCalculationForm');
    const resultCard = document.getElementById('resultCard');
    const specialCaseAlert = document.getElementById('specialCaseAlert');
    const submitSpinner = document.getElementById('submitSpinner');
    const printTypeSelect = document.getElementById('printType');
    const printRunInput = document.getElementById('printRun');

    // Carregar tipos de impressão da API
    loadPrintTypes();

    // Configurar envio do formulário
    setupFormSubmission();

    /**
     * Carrega os tipos de impressão disponíveis da API
     */
    function loadPrintTypes() {
        fetch('/api/print-types')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar tipos de impressão');
                }
                return response.json();
            })
            .then(printTypes => {
                populatePrintTypeOptions(printTypes);
            })
            .catch(error => {
                console.error('Erro:', error);
                // Fallback para desenvolvimento/demonstração
                const sampleTypes = ['4/0', '4/4', '2/2', '2/0', '1/1', '1/0'];
                populatePrintTypeOptions(sampleTypes);
            });
    }

    /**
     * Preenche o select com as opções de tipos de impressão
     */
    function populatePrintTypeOptions(types) {
        // Limpar opções existentes (exceto a primeira)
        while (printTypeSelect.options.length > 1) {
            printTypeSelect.remove(1);
        }

        // Adicionar novas opções
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            printTypeSelect.appendChild(option);
        });
    }

    /**
     * Configura o evento de envio do formulário
     */
    function setupFormSubmission() {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            // Mostrar spinner de carregamento
            submitSpinner.style.display = 'inline-block';

            // Obter valores do formulário
            const printType = printTypeSelect.value;
            const printRun = printRunInput.value;

            // Chamar API para cálculo de desperdício
            calculateWaste(printType, printRun);
        });
    }

    /**
     * Realiza a chamada à API para cálculo de desperdício
     */
    function calculateWaste(printType, printRun) {
        const url = `/api/waste-calculation?print_type=${encodeURIComponent(printType)}&print_run=${printRun}`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na requisição');
                }
                return response.json();
            })
            .then(data => {
                // Ocultar spinner
                submitSpinner.style.display = 'none';

                // Exibir resultados
                displayResults(data);
            })
            .catch(error => {
                // Ocultar spinner
                submitSpinner.style.display = 'none';

                console.error('Erro ao calcular desperdício:', error);

                // Para desenvolvimento/demonstração, usar dados simulados
                const mockData = generateMockData(printType, printRun);
                displayResults(mockData);
            });
    }

    /**
     * Gera dados simulados para desenvolvimento/demonstração
     */
    function generateMockData(printType, printRun) {
        const run = parseInt(printRun);
        return {
            print_type: printType,
            print_run: run,
            waste_amount: Math.floor(run * 0.05), // 5% de desperdício como exemplo
            adjustment: run > 1000 ? 'Auto' : 'Manual',
            is_special_case: run > 5000 // Caso especial para tiragens grandes
        };
    }

    /**
     * Exibe os resultados na interface
     */
    function displayResults(data) {
        // Preencher dados
        document.getElementById('resultPrintType').textContent = data.print_type;
        document.getElementById('resultPrintRun').textContent = data.print_run;
        document.getElementById('resultWaste').textContent = data.waste_amount;
        document.getElementById('resultAdjustment').textContent = data.adjustment || 'N/A';

        // Verificar caso especial
        if (data.is_special_case) {
            specialCaseAlert.style.display = 'flex';
            resultCard.classList.add('special-case');
        } else {
            specialCaseAlert.style.display = 'none';
            resultCard.classList.remove('special-case');
        }

        // Mostrar card de resultado com animação
        resultCard.style.display = 'block';
        resultCard.classList.add('fade-in');

        // Remover classe de animação após a conclusão
        setTimeout(() => {
            resultCard.classList.remove('fade-in');
        }, 500);
    }
});