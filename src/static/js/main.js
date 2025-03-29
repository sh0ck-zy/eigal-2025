/**
 * Script principal para o sistema de cálculo de desperdício
 * Versão: 1.0.0
 */
document.addEventListener('DOMContentLoaded', function () {
    // Elementos do DOM
    const form = document.getElementById('wasteCalculationForm');
    const resultCard = document.getElementById('resultCard');
    const suggestionCard = document.getElementById('suggestionCard');
    const specialCaseAlert = document.getElementById('specialCaseAlert');
    const submitSpinner = document.querySelector('.spinner-border');
    const printTypeSelect = document.getElementById('printType');
    const printRunInput = document.getElementById('printRun');
    const wastePercentage = document.getElementById('wastePercentage');

    // Elementos de histórico
    const historyToggle = document.getElementById('historyToggle');
    const historyCollapse = document.getElementById('historyCollapse');
    const historyItems = document.getElementById('historyItems');
    const historyCount = document.getElementById('historyCount');
    const clearHistoryBtn = document.getElementById('clearHistory');
    const emptyHistoryMessage = document.getElementById('emptyHistoryMessage');

    // Botão de sugestão de otimização
    const applySuggestionBtn = document.getElementById('applySuggestion');

    // Rastreamento do cálculo atual
    let currentCalculation = {
        print_type: '',
        print_run: 0,
        waste_amount: 0,
        adjustment: '',
        is_special_case: false
    };

    // Inicialização
    initTooltips();
    loadPrintTypes();
    loadHistoryFromStorage();
    setupEventListeners();

    /**
     * Inicializa os tooltips do Bootstrap
     */
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    /**
     * Configura todos os listeners de eventos
     */
    function setupEventListeners() {
        // Form submit
        form.addEventListener('submit', handleFormSubmit);

        // Toggle do histórico
        historyToggle.addEventListener('click', function () {
            const bsCollapse = new bootstrap.Collapse(historyCollapse, {
                toggle: true
            });

            // Alternar ícone
            const icon = historyToggle.querySelector('.bi');
            if (icon.classList.contains('bi-chevron-down')) {
                icon.classList.replace('bi-chevron-down', 'bi-chevron-up');
            } else {
                icon.classList.replace('bi-chevron-up', 'bi-chevron-down');
            }
        });

        // Botão limpar histórico
        clearHistoryBtn.addEventListener('click', clearHistory);

        // Botão aplicar sugestão
        applySuggestionBtn.addEventListener('click', applySuggestion);

        // Validação de entrada
        printRunInput.addEventListener('input', function () {
            // Remover caracteres não numéricos
            this.value = this.value.replace(/[^0-9]/g, '');

            // Limitar a um valor razoável
            if (parseInt(this.value) > 1000000) {
                this.value = '1000000';
            }
        });

        // Tecla Enter para enviar formulário
        printRunInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                form.dispatchEvent(new Event('submit'));
            }
        });
    }

    /**
     * Manipula o envio do formulário
     */
    function handleFormSubmit(event) {
        event.preventDefault();

        // Validar formulário
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        // Mostrar spinner
        submitSpinner.style.display = 'inline-block';

        // Obter valores
        const printType = printTypeSelect.value;
        const printRun = parseInt(printRunInput.value);

        // Chamar API
        calculateWaste(printType, printRun);
    }

    /**
     * Carrega os tipos de impressão da API
     */
    function loadPrintTypes() {
        fetch('/api/print-types')
            .then(handleResponse)
            .then(printTypes => {
                populatePrintTypeOptions(printTypes);
            })
            .catch(error => {
                console.error('Erro ao carregar tipos de impressão:', error);

                // Dados de exemplo para desenvolvimento
                const sampleTypes = ['4/0', '4/4', '2/2', '2/0', '1/1', '1/0', '5/5', '5/0'];
                populatePrintTypeOptions(sampleTypes);
            });
    }

    /**
     * Processa a resposta da API
     */
    function handleResponse(response) {
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        return response.json();
    }

    /**
     * Preenche o select com opções de tipos de impressão
     */
    function populatePrintTypeOptions(types) {
        // Limpar opções existentes, exceto a primeira
        while (printTypeSelect.options.length > 1) {
            printTypeSelect.remove(1);
        }

        // Ordenar tipos para melhor visualização
        types.sort();

        // Adicionar opções
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            printTypeSelect.appendChild(option);
        });
    }

    /**
     * Calcula o desperdício chamando a API
     */
    function calculateWaste(printType, printRun) {
        const url = `/api/waste-calculation?print_type=${encodeURIComponent(printType)}&print_run=${printRun}`;

        fetch(url)
            .then(handleResponse)
            .then(data => {
                // Ocultar spinner
                submitSpinner.style.display = 'none';

                // Salvar cálculo atual
                currentCalculation = {
                    print_type: data.print_type,
                    print_run: data.print_run,
                    waste_amount: data.waste_amount,
                    adjustment: data.adjustment || 'N/A',
                    is_special_case: data.is_special_case
                };

                // Exibir resultados
                displayResults(data);

                // Adicionar ao histórico (apenas se não for uma visualização de item existente)
                if (!isCalculationInHistory(data)) {
                    addToHistory(data);
                }

                // Exibir sugestões de otimização
                showOptimizationSuggestion(data);
            })
            .catch(error => {
                // Ocultar spinner
                submitSpinner.style.display = 'none';

                console.error('Erro ao calcular desperdício:', error);

                // Para desenvolvimento, exibir resultado simulado
                const mockData = generateMockData(printType, printRun);

                // Salvar cálculo atual
                currentCalculation = {
                    print_type: mockData.print_type,
                    print_run: mockData.print_run,
                    waste_amount: mockData.waste_amount,
                    adjustment: mockData.adjustment || 'N/A',
                    is_special_case: mockData.is_special_case
                };

                displayResults(mockData);

                // Adicionar ao histórico (apenas se não for uma visualização de item existente)
                if (!isCalculationInHistory(mockData)) {
                    addToHistory(mockData);
                }

                showOptimizationSuggestion(mockData);
            });
    }

    /**
     * Verifica se um cálculo já existe no histórico
     */
    function isCalculationInHistory(data) {
        const history = getHistoryFromStorage();
        return history.some(item =>
            item.print_type === data.print_type &&
            item.print_run === data.print_run
        );
    }

    /**
     * Exibe os resultados na interface
     */
    function displayResults(data) {
        // Preencher campos
        document.getElementById('resultPrintType').textContent = data.print_type;
        document.getElementById('resultPrintRun').textContent = formatNumber(data.print_run);
        document.getElementById('resultWaste').textContent = formatNumber(data.waste_amount);
        document.getElementById('resultAdjustment').textContent = data.adjustment || 'N/A';

        // Calcular e exibir percentual de desperdício
        const wastePct = (data.waste_amount / data.print_run) * 100;
        wastePercentage.textContent = `${wastePct.toFixed(1)}%`;

        // Definir cor do badge baseado no percentual
        if (wastePct < 5) {
            wastePercentage.className = 'badge bg-success';
        } else if (wastePct < 10) {
            wastePercentage.className = 'badge bg-info';
        } else if (wastePct < 15) {
            wastePercentage.className = 'badge bg-warning';
        } else {
            wastePercentage.className = 'badge bg-danger';
        }

        // Tratar caso especial
        if (data.is_special_case) {
            specialCaseAlert.style.display = 'flex';
            resultCard.classList.add('special-case');
        } else {
            specialCaseAlert.style.display = 'none';
            resultCard.classList.remove('special-case');
        }

        // Exibir o card de resultado com animação
        resultCard.style.display = 'block';
        resultCard.classList.add('fade-in');

        // Remover classe após animação
        setTimeout(() => {
            resultCard.classList.remove('fade-in');
        }, 500);
    }

    /**
     * Gera uma sugestão de otimização com base nos dados
     */
    function showOptimizationSuggestion(data) {
        // Verificar se a sugestão é relevante
        if (data.print_run < 2000) {
            // Calcular a sugestão (exemplo simplificado)
            const suggestedRun = Math.ceil(data.print_run / 500) * 500;

            // Se a sugestão for igual à tiragem atual, aumentar
            if (suggestedRun <= data.print_run) {
                suggestedRun += 500;
            }

            // Calcular a redução relativa de desperdício (lógica fictícia para demonstração)
            const currentWastePct = (data.waste_amount / data.print_run) * 100;
            const estimatedNewWaste = data.waste_amount * 1.2; // Assumindo que aumenta 20%
            const newWastePct = (estimatedNewWaste / suggestedRun) * 100;
            const reduction = Math.round(currentWastePct - newWastePct);

            // Mostrar a sugestão apenas se houver redução
            if (reduction > 0) {
                document.getElementById('optimizationSuggestion').innerHTML = `
                    <p>Aumentando a tiragem para <strong>${formatNumber(suggestedRun)}</strong> unidades, 
                    você teria uma redução de aproximadamente <strong>${reduction}%</strong> 
                    no desperdício relativo por unidade.</p>
                    <p class="text-muted small">O desperdício total em folhas pode ser maior, mas o custo por unidade será menor.</p>
                `;

                // Definir valor a ser aplicado na sugestão
                applySuggestionBtn.dataset.suggestedRun = suggestedRun;

                // Mostrar card de sugestão
                suggestionCard.style.display = 'block';
                suggestionCard.classList.add('fade-in');

                // Remover classe após animação
                setTimeout(() => {
                    suggestionCard.classList.remove('fade-in');
                }, 500);
            } else {
                suggestionCard.style.display = 'none';
            }
        } else {
            suggestionCard.style.display = 'none';
        }
    }

    /**
     * Aplica a sugestão de otimização
     */
    function applySuggestion() {
        const suggestedRun = applySuggestionBtn.dataset.suggestedRun;
        if (suggestedRun) {
            printRunInput.value = suggestedRun;
            suggestionCard.style.display = 'none';
            form.dispatchEvent(new Event('submit'));
        }
    }

    /**
     * Formata números com separador de milhares
     */
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    /**
     * Gera dados simulados para desenvolvimento
     */
    function generateMockData(printType, printRun) {
        const wasteRate = 0.05; // 5% de taxa de desperdício base

        // Ajuste da taxa com base no tipo de impressão
        let adjustedRate = wasteRate;
        if (printType.includes('4/4')) {
            adjustedRate = 0.07; // Tipos com mais cores têm mais desperdício
        } else if (printType.includes('2/2')) {
            adjustedRate = 0.06;
        }

        // Ajuste baseado na tiragem (tiragens maiores têm menor % de desperdício)
        if (printRun > 5000) {
            adjustedRate *= 0.8;
        } else if (printRun < 1000) {
            adjustedRate *= 1.2;
        }

        const wasteAmount = Math.round(printRun * adjustedRate);

        return {
            print_type: printType,
            print_run: printRun,
            waste_amount: wasteAmount,
            adjustment: printRun > 1000 ? 'Auto' : 'Manual',
            is_special_case: printRun > 5000 && printType.includes('5/')
        };
    }

    /**
     * Adiciona um cálculo ao histórico
     */
    function addToHistory(data) {
        // Criar objeto de histórico
        const historyItem = {
            timestamp: new Date().toISOString(),
            print_type: data.print_type,
            print_run: data.print_run,
            waste_amount: data.waste_amount,
            is_special_case: data.is_special_case
        };

        // Obter histórico existente
        let history = getHistoryFromStorage();

        // Adicionar novo item no início
        history.unshift(historyItem);

        // Limitar a 5 itens
        if (history.length > 5) {
            history = history.slice(0, 5);
        }

        // Salvar no localStorage
        localStorage.setItem('wasteCalculationHistory', JSON.stringify(history));

        // Atualizar UI
        renderHistoryItems(history);

        // Verificar se o histórico está colapsado e tem itens
        if (history.length > 0 && !historyCollapse.classList.contains('show')) {
            // Destacar o cabeçalho para indicar novos itens
            historyToggle.classList.add('highlight-history');
            setTimeout(() => {
                historyToggle.classList.remove('highlight-history');
            }, 2000);
        }
    }

    /**
     * Remove um item específico do histórico
     */
    function removeHistoryItem(index) {
        let history = getHistoryFromStorage();

        // Remover o item no índice especificado
        history.splice(index, 1);

        // Salvar no localStorage
        localStorage.setItem('wasteCalculationHistory', JSON.stringify(history));

        // Atualizar UI
        renderHistoryItems(history);

        showToast('Item removido do histórico.');
    }

    /**
     * Obtém o histórico do localStorage
     */
    function getHistoryFromStorage() {
        const historyString = localStorage.getItem('wasteCalculationHistory');
        return historyString ? JSON.parse(historyString) : [];
    }

    /**
     * Carrega o histórico do localStorage na inicialização
     */
    function loadHistoryFromStorage() {
        const history = getHistoryFromStorage();
        renderHistoryItems(history);
    }

    /**
     * Renderiza os itens de histórico na UI
     */
    function renderHistoryItems(history) {
        // Limpar conteúdo atual
        historyItems.innerHTML = '';

        // Atualizar contador
        historyCount.textContent = history.length;

        // Se não houver histórico, mostrar mensagem
        if (history.length === 0) {
            emptyHistoryMessage.style.display = 'block';
            return;
        }

        // Ocultar mensagem de vazio
        emptyHistoryMessage.style.display = 'none';

        // Criar tabela para os itens de histórico
        const table = document.createElement('table');
        table.className = 'table table-hover';

        // Cabeçalho da tabela
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Tipo</th>
                <th>Tiragem</th>
                <th>Desperdício</th>
                <th>Data/Hora</th>
                <th>Ações</th>
            </tr>
        `;
        table.appendChild(thead);

        // Corpo da tabela
        const tbody = document.createElement('tbody');

        // Adicionar itens
        history.forEach((item, index) => {
            const row = document.createElement('tr');
            if (item.is_special_case) {
                row.classList.add('table-warning');
            }

            // Formatar data
            const date = new Date(item.timestamp);
            const formattedDate = date.toLocaleDateString('pt-BR') + ' ' +
                date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

            // Conteúdo da linha
            row.innerHTML = `
                <td>${item.print_type}</td>
                <td>${formatNumber(item.print_run)}</td>
                <td>${formatNumber(item.waste_amount)} folhas</td>
                <td>${formattedDate}</td>
                <td>
                    <div class="d-flex">
                        <button class="btn btn-sm view-history-item me-1" title="Visualizar este cálculo">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm delete-history-item" title="Remover do histórico">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            `;

            // Adicionar evento para visualizar este cálculo
            const viewBtn = row.querySelector('.view-history-item');
            viewBtn.addEventListener('click', () => {
                printTypeSelect.value = item.print_type;
                printRunInput.value = item.print_run;

                // Mostrar os dados mas sem recalcular (simulando um clique no botão Calcular)
                const data = {
                    print_type: item.print_type,
                    print_run: item.print_run,
                    waste_amount: item.waste_amount,
                    adjustment: 'Auto', // Valor de exemplo, pode ser ajustado
                    is_special_case: item.is_special_case
                };

                displayResults(data);
                showOptimizationSuggestion(data);
            });

            // Adicionar evento para excluir este item
            const deleteBtn = row.querySelector('.delete-history-item');
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation(); // Evitar que o evento de clique da linha seja disparado
                removeHistoryItem(index);
            });

            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        historyItems.appendChild(table);
    }

    /**
     * Limpa o histórico de cálculos
     */
    function clearHistory() {
        localStorage.removeItem('wasteCalculationHistory');
        renderHistoryItems([]);
        showToast('Histórico limpo com sucesso!');
    }

    /**
     * Exibe um toast de notificação
     */
    function showToast(message) {
        // Criar elemento de toast
        const toastElement = document.createElement('div');
        toastElement.className = 'toast align-items-center bg-success text-white position-fixed bottom-0 end-0 m-3';
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');

        toastElement.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Fechar"></button>
            </div>
        `;

        // Adicionar ao documento
        document.body.appendChild(toastElement);

        // Inicializar e mostrar o toast
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 3000
        });
        toast.show();

        // Remover elemento após esconder
        toastElement.addEventListener('hidden.bs.toast', () => {
            document.body.removeChild(toastElement);
        });
    }