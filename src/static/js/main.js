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
                showToast('Não foi possível carregar os tipos de impressão. Por favor, tente novamente mais tarde.');
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

                // Exibir sugestão de otimização
                showOptimizationSuggestion(data);
            })
            .catch(error => {
                console.error('Erro ao calcular desperdício:', error);
                submitSpinner.style.display = 'none';
                showToast('Erro ao calcular desperdício. Por favor, tente novamente.');
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
     * Exibe os resultados do cálculo
     */
    function displayResults(data) {
        // Preencher valores
        document.getElementById('resultPrintType').textContent = data.print_type;
        document.getElementById('resultPrintRun').textContent = formatNumber(data.print_run);
        document.getElementById('resultWaste').textContent = formatNumber(data.waste_amount);
        document.getElementById('resultAdjustment').textContent = data.adjustment || 'N/A';

        // Calcular e exibir porcentagem de desperdício
        const wastePercent = ((data.waste_amount / data.print_run) * 100).toFixed(2);
        wastePercentage.textContent = `${wastePercent}%`;

        // Mostrar/ocultar alerta de caso especial
        if (data.is_special_case) {
            specialCaseAlert.style.display = 'flex';
        } else {
            specialCaseAlert.style.display = 'none';
        }

        // Exibir card de resultado
        resultCard.style.display = 'block';

        // Rolar para o card de resultado
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Exibe sugestões de otimização com base nos resultados
     */
    function showOptimizationSuggestion(data) {
        let suggestion = '';
        let canOptimize = false;

        // Verificar possibilidades de otimização
        if (data.print_run < 1000) {
            // Sugerir aumento para 1000 unidades
            const nextTier = 1000;
            
            // Simular cálculo para próximo tier
            fetch(`/api/waste-calculation?print_type=${encodeURIComponent(data.print_type)}&print_run=${nextTier}`)
                .then(handleResponse)
                .then(optimizedData => {
                    const currentWastePerUnit = data.waste_amount / data.print_run;
                    const optimizedWastePerUnit = optimizedData.waste_amount / optimizedData.print_run;
                    
                    if (optimizedWastePerUnit < currentWastePerUnit) {
                        canOptimize = true;
                        
                        suggestion = `
                            <p>Aumentar a tiragem para <strong>${formatNumber(nextTier)}</strong> unidades 
                            pode reduzir o desperdício por unidade de <strong>${(currentWastePerUnit * 100).toFixed(2)}%</strong> 
                            para <strong>${(optimizedWastePerUnit * 100).toFixed(2)}%</strong>.</p>
                            <p class="text-success">Economia total: <strong>${
                                ((currentWastePerUnit - optimizedWastePerUnit) * nextTier).toFixed(0)
                            }</strong> folhas comparado com proporção atual.</p>
                        `;
                        
                        // Exibir card de sugestão
                        document.getElementById('optimizationSuggestion').innerHTML = suggestion;
                        suggestionCard.style.display = 'block';
                    } else {
                        suggestionCard.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Erro ao calcular otimização:', error);
                    suggestionCard.style.display = 'none';
                });
        } else {
            suggestionCard.style.display = 'none';
        }
    }

    /**
     * Aplica a sugestão de otimização
     */
    function applySuggestion() {
        // Sugestão fixa para tiragens menores que 1000
        if (currentCalculation.print_run < 1000) {
            printRunInput.value = '1000';
            
            // Acionar envio do formulário
            form.dispatchEvent(new Event('submit'));
        }
    }

    /**
     * Formata números com separadores de milhar
     */
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    /**
     * Adiciona um cálculo ao histórico
     */
    function addToHistory(data) {
        // Obter histórico atual
        const history = getHistoryFromStorage();
        
        // Adicionar timestamp
        const historyItem = {
            ...data,
            timestamp: new Date().toISOString()
        };
        
        // Adicionar no início (mais recente primeiro)
        history.unshift(historyItem);
        
        // Limitar a 10 itens
        if (history.length > 10) {
            history.pop();
        }
        
        // Salvar no localStorage
        localStorage.setItem('wasteCalculationHistory', JSON.stringify(history));
        
        // Atualizar exibição
        renderHistoryItems(history);
    }

    /**
     * Remove um item do histórico
     */
    function removeHistoryItem(index) {
        // Obter histórico atual
        const history = getHistoryFromStorage();
        
        // Remover item no índice especificado
        history.splice(index, 1);
        
        // Salvar no localStorage
        localStorage.setItem('wasteCalculationHistory', JSON.stringify(history));
        
        // Atualizar exibição
        renderHistoryItems(history);
    }

    /**
     * Obtém o histórico do localStorage
     */
    function getHistoryFromStorage() {
        const history = localStorage.getItem('wasteCalculationHistory');
        return history ? JSON.parse(history) : [];
    }

    /**
     * Carrega o histórico do localStorage
     */
    function loadHistoryFromStorage() {
        const history = getHistoryFromStorage();
        renderHistoryItems(history);
    }

    /**
     * Renderiza os itens do histórico
     */
    function renderHistoryItems(history) {
        // Atualizar contador
        historyCount.textContent = history.length;
        
        // Limpar conteúdo atual
        historyItems.innerHTML = '';
        
        // Mostrar mensagem se vazio
        if (history.length === 0) {
            emptyHistoryMessage.style.display = 'block';
            return;
        }
        
        // Ocultar mensagem se não vazio
        emptyHistoryMessage.style.display = 'none';
        
        // Criar elementos para cada item do histórico
        history.forEach((item, index) => {
            // Converter timestamp para formato legível
            const date = new Date(item.timestamp);
            const formattedDate = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
            
            // Calcular e formatar porcentagem de desperdício
            const wastePercent = ((item.waste_amount / item.print_run) * 100).toFixed(2);
            
            // Criar elemento de histórico
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            if (item.is_special_case) {
                historyItem.classList.add('special-case');
            }
            
            historyItem.innerHTML = `
                <div class="history-item-header">
                    <div class="history-item-title">
                        <span class="badge ${item.is_special_case ? 'bg-warning' : 'bg-primary'}">
                            ${item.print_type}
                        </span>
                        <span class="history-item-quantity">${formatNumber(item.print_run)} unidades</span>
                    </div>
                    <div class="history-item-actions">
                        <button class="btn btn-sm btn-outline-primary view-btn" data-index="${index}">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger delete-btn" data-index="${index}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="history-item-details">
                    <div class="history-detail">
                        <i class="bi bi-exclamation-triangle text-warning"></i>
                        <span>Desperdício: <strong>${formatNumber(item.waste_amount)} folhas</strong> (${wastePercent}%)</span>
                    </div>
                    <div class="history-detail">
                        <i class="bi bi-calendar"></i>
                        <span>Calculado em: <strong>${formattedDate}</strong></span>
                    </div>
                </div>
            `;
            
            // Adicionar ao contêiner
            historyItems.appendChild(historyItem);
            
            // Configurar botões
            const viewBtn = historyItem.querySelector('.view-btn');
            const deleteBtn = historyItem.querySelector('.delete-btn');
            
            viewBtn.addEventListener('click', function() {
                // Preencher formulário com valores deste item
                printTypeSelect.value = item.print_type;
                printRunInput.value = item.print_run;
                
                // Exibir resultados
                displayResults(item);
                
                // Reexibir sugestões de otimização
                showOptimizationSuggestion(item);
                
                // Fechar o histórico
                new bootstrap.Collapse(historyCollapse, {
                    toggle: true
                });
                
                // Trocar ícone
                const icon = historyToggle.querySelector('.bi');
                icon.classList.replace('bi-chevron-up', 'bi-chevron-down');
            });
            
            deleteBtn.addEventListener('click', function() {
                removeHistoryItem(index);
            });
        });
    }

    /**
     * Limpa todo o histórico
     */
    function clearHistory() {
        localStorage.removeItem('wasteCalculationHistory');
        renderHistoryItems([]);
        showToast('Histórico de cálculos limpo com sucesso.');
    }

    /**
     * Exibe uma mensagem toast
     */
    function showToast(message) {
        // Se a aplicação tiver um sistema de toast, chamar aqui
        alert(message);
    }
});