/**
 * Módulo de Gerenciamento da Página de Produtos
 * Responsável por: filtros, scroll, inicialização
 */

(function() {
    'use strict';

    // ============================================
    // CONFIGURAÇÕES
    // ============================================
    const CONFIG = {
        SCROLL_OFFSET: 300,
        SCROLL_DELAY: 100,
        PRODUCTS_SECTION_ID: 'products-cards-section',
        HEADER_SELECTOR: '.header',
        PRODUCT_CARD_SELECTOR: '.product-card-link',
        CATEGORY_TITLE_SELECTOR: '.filter-category-title',
        FILTER_ITEM_SELECTOR: '.filter-item',
        SEARCH_INPUT_ID: 'product-search',
        ALL_PRODUCTS_BUTTON_SELECTOR: '.filter-all-products'
    };

    // ============================================
    // ESTADO GLOBAL
    // ============================================
    const state = {
        activeFilter: null,
        isInitialized: false
    };

    // ============================================
    // UTILITÁRIOS
    // ============================================
    const utils = {
        /**
         * Calcula a posição absoluta de um elemento
         */
        getElementOffsetTop(element) {
            if (!element) return 0;
            
            let offsetTop = 0;
            let currentElement = element;
            
            while (currentElement) {
                offsetTop += currentElement.offsetTop;
                currentElement = currentElement.offsetParent;
            }
            
            return offsetTop;
        },

        /**
         * Normaliza string para comparação
         */
        normalizeString(str) {
            return (str || '').toLowerCase().trim().replace(/\s+/g, ' ');
        },

        /**
         * Compara duas strings de forma flexível
         */
        stringsMatch(str1, str2) {
            const n1 = this.normalizeString(str1);
            const n2 = this.normalizeString(str2);
            
            return n1 === n2 || 
                   n1.includes(n2) || 
                   n2.includes(n1);
        },

        /**
         * Log apenas em modo debug
         */
        log(...args) {
            if (window.DEBUG) {
                console.log('[ProductsPage]', ...args);
            }
        }
    };

    // ============================================
    // GERENCIADOR DE FILTROS
    // ============================================
    const FilterManager = {
        /**
         * Filtra produtos por categoria ou termo de busca
         */
        filter(filterValue, filterByCategory = false) {
            utils.log('Filtrando produtos:', filterValue, filterByCategory);
            
            const cards = document.querySelectorAll(CONFIG.PRODUCT_CARD_SELECTOR);
            utils.log('Total de produtos encontrados:', cards.length);
            
            if (cards.length === 0) {
                utils.log('Nenhum produto encontrado no DOM');
                return 0;
            }
            
            let visibleCount = 0;
            
            cards.forEach(card => {
                const categoriaPrincipal = card.getAttribute('data-categoria-principal') || '';
                let shouldShow = false;
                
                if (filterByCategory && filterValue) {
                    shouldShow = utils.stringsMatch(categoriaPrincipal, filterValue);
                } else if (filterValue) {
                    shouldShow = utils.stringsMatch(categoriaPrincipal, filterValue);
                } else {
                    shouldShow = true;
                }
                
                if (shouldShow) {
                    card.style.display = 'flex';
                    card.style.pointerEvents = 'auto';
                    card.style.visibility = 'visible';
                    card.style.opacity = '1';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                    card.style.pointerEvents = 'none';
                }
            });
            
            utils.log('Produtos visíveis após filtro:', visibleCount, 'de', cards.length);
            return visibleCount;
        },

        /**
         * Mostra todos os produtos
         */
        showAll() {
            utils.log('Mostrando todos os produtos');
            
            const cards = document.querySelectorAll(CONFIG.PRODUCT_CARD_SELECTOR);
            const filterItems = document.querySelectorAll(CONFIG.FILTER_ITEM_SELECTOR);
            const categoryTitles = document.querySelectorAll(CONFIG.CATEGORY_TITLE_SELECTOR);
            const searchInput = document.getElementById(CONFIG.SEARCH_INPUT_ID);
            
            // Remove classes active
            filterItems.forEach(item => item.classList.remove('active'));
            categoryTitles.forEach(title => title.classList.remove('active'));
            
            // Limpa busca
            if (searchInput) {
                searchInput.value = '';
            }
            
            // Remove filtro ativo
            state.activeFilter = null;
            
            // Mostra todos os produtos
            cards.forEach(card => {
                card.style.removeProperty('display');
                card.style.removeProperty('visibility');
                card.style.removeProperty('opacity');
                card.style.removeProperty('pointer-events');
                
                card.style.display = 'flex';
                card.style.pointerEvents = 'auto';
                card.style.visibility = 'visible';
                card.style.opacity = '1';
            });
            
            // Limpa parâmetro da URL
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('categoria')) {
                urlParams.delete('categoria');
                const newUrl = window.location.pathname + 
                    (urlParams.toString() ? '?' + urlParams.toString() : '');
                window.history.replaceState({}, '', newUrl);
            }
            
            utils.log('Todos os produtos visíveis:', cards.length);
        },

        /**
         * Aplica filtro por categoria da URL
         */
        applyCategoryFromURL() {
            const urlParams = new URLSearchParams(window.location.search);
            const categoriaParam = urlParams.get('categoria');
            
            if (!categoriaParam) {
                return false;
            }
            
            utils.log('Aplicando filtro da URL:', categoriaParam);
            
            const categoryTitles = document.querySelectorAll(CONFIG.CATEGORY_TITLE_SELECTOR);
            let found = false;
            
            categoryTitles.forEach(title => {
                const categoriaPrincipal = title.getAttribute('data-categoria-principal');
                
                if (utils.stringsMatch(categoriaPrincipal, categoriaParam)) {
                    utils.log('Categoria encontrada:', categoriaPrincipal);
                    
                    // Remove active de todos
                    document.querySelectorAll(CONFIG.FILTER_ITEM_SELECTOR).forEach(item => {
                        item.classList.remove('active');
                    });
                    categoryTitles.forEach(t => t.classList.remove('active'));
                    
                    // Adiciona active ao título encontrado
                    title.classList.add('active');
                    state.activeFilter = title;
                    
                    // Limpa busca
                    const searchInput = document.getElementById(CONFIG.SEARCH_INPUT_ID);
                    if (searchInput) {
                        searchInput.value = '';
                    }
                    
                    // Aplica filtro
                    this.filter(categoriaPrincipal, true);
                    found = true;
                }
            });
            
            return found;
        }
    };

    // ============================================
    // GERENCIADOR DE SCROLL
    // ============================================
    const ScrollManager = {
        /**
         * Faz scroll para a seção de produtos
         */
        scrollToProducts() {
            utils.log('Fazendo scroll para produtos');
            
            return new Promise((resolve) => {
                requestAnimationFrame(() => {
                    const section = document.getElementById(CONFIG.PRODUCTS_SECTION_ID);
                    
                    if (!section) {
                        utils.log('Seção de produtos não encontrada');
                        resolve(false);
                        return;
                    }
                    
                    // Calcula posição usando getBoundingClientRect
                    const rect = section.getBoundingClientRect();
                    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                    let elementTop = rect.top + scrollTop;
                    
                    // Fallback para offsetTop
                    if (elementTop === 0 || elementTop < 100) {
                        elementTop = utils.getElementOffsetTop(section);
                    }
                    
                    const header = document.querySelector(CONFIG.HEADER_SELECTOR);
                    const headerHeight = header ? header.offsetHeight : 80;
                    const targetPosition = Math.max(0, elementTop - headerHeight - CONFIG.SCROLL_OFFSET);
                    
                    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
                    
                    // Se já estiver próximo, não faz scroll
                    if (Math.abs(targetPosition - currentScroll) < 50) {
                        utils.log('Já está próximo da posição');
                        resolve(true);
                        return;
                    }
                    
                    utils.log('Scroll para:', targetPosition, 'Atual:', currentScroll);
                    
                    // Scroll instantâneo
                    window.scrollTo({ top: targetPosition, behavior: 'auto' });
                    
                    // Scroll suave após delay
                    setTimeout(() => {
                        const rect2 = section.getBoundingClientRect();
                        const scrollTop2 = window.pageYOffset || document.documentElement.scrollTop;
                        let elementTop2 = rect2.top + scrollTop2;
                        
                        if (elementTop2 === 0 || elementTop2 < 100) {
                            elementTop2 = utils.getElementOffsetTop(section);
                        }
                        
                        const targetPosition2 = Math.max(0, elementTop2 - headerHeight - CONFIG.SCROLL_OFFSET);
                        window.scrollTo({ top: targetPosition2, behavior: 'smooth' });
                        resolve(true);
                    }, CONFIG.SCROLL_DELAY);
                });
            });
        },

        /**
         * Faz scroll múltiplas vezes com delays crescentes
         */
        scrollToProductsMultiple(times = 3) {
            const delays = [100, 300, 600, 1000, 1500, 2000];
            
            delays.slice(0, times).forEach((delay, index) => {
                setTimeout(() => {
                    this.scrollToProducts();
                }, delay);
            });
        }
    };

    // ============================================
    // GERENCIADOR DE EVENTOS
    // ============================================
    const EventManager = {
        /**
         * Inicializa todos os event listeners
         */
        init() {
            this.attachSearchInput();
            this.attachCategoryTitles();
            this.attachAllProductsButton();
        },

        /**
         * Anexa evento ao campo de busca
         */
        attachSearchInput() {
            const searchInput = document.getElementById(CONFIG.SEARCH_INPUT_ID);
            if (!searchInput) return;
            
            // Remove listener anterior clonando o elemento
            const newInput = searchInput.cloneNode(true);
            searchInput.parentNode.replaceChild(newInput, searchInput);
            
            newInput.addEventListener('input', (e) => {
                const searchTerm = e.target.value.trim();
                
                if (state.activeFilter) {
                    state.activeFilter.classList.remove('active');
                    state.activeFilter = null;
                }
                
                FilterManager.filter(searchTerm);
            });
        },

        /**
         * Anexa eventos aos títulos de categoria
         */
        attachCategoryTitles() {
            const categoryTitles = document.querySelectorAll(CONFIG.CATEGORY_TITLE_SELECTOR);
            
            categoryTitles.forEach(title => {
                // Remove listener anterior clonando
                const newTitle = title.cloneNode(true);
                title.parentNode.replaceChild(newTitle, title);
                
                newTitle.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Remove active de todos
                    document.querySelectorAll(CONFIG.FILTER_ITEM_SELECTOR).forEach(item => {
                        item.classList.remove('active');
                    });
                    document.querySelectorAll(CONFIG.CATEGORY_TITLE_SELECTOR).forEach(t => {
                        t.classList.remove('active');
                    });
                    
                    // Adiciona active ao clicado
                    newTitle.classList.add('active');
                    state.activeFilter = newTitle;
                    
                    // Limpa busca
                    const searchInput = document.getElementById(CONFIG.SEARCH_INPUT_ID);
                    if (searchInput) {
                        searchInput.value = '';
                    }
                    
                    // Aplica filtro
                    const categoriaPrincipal = newTitle.getAttribute('data-categoria-principal');
                    FilterManager.filter(categoriaPrincipal, true);
                });
            });
        },

        /**
         * Anexa evento ao botão "Todos os Produtos"
         */
        attachAllProductsButton() {
            const buttons = document.querySelectorAll(CONFIG.ALL_PRODUCTS_BUTTON_SELECTOR);
            
            buttons.forEach(button => {
                // Remove listener anterior clonando
                const newButton = button.cloneNode(true);
                button.parentNode.replaceChild(newButton, button);
                
                newButton.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    FilterManager.showAll();
                });
            });
        }
    };

    // ============================================
    // INICIALIZADOR PRINCIPAL
    // ============================================
    const ProductsPage = {
        /**
         * Inicializa a página de produtos
         */
        init() {
            if (state.isInitialized) {
                utils.log('Já inicializado, reinicializando...');
            }
            
            utils.log('Inicializando página de produtos');
            
            // Garante que todos os produtos estejam visíveis
            this.makeAllProductsVisible();
            
            // Inicializa eventos
            EventManager.init();
            
            // Aplica filtro da URL se houver
            const hasCategoryFilter = FilterManager.applyCategoryFromURL();
            
            // Se houver filtro de categoria, faz scroll
            if (hasCategoryFilter) {
                setTimeout(() => {
                    ScrollManager.scrollToProducts();
                }, CONFIG.SCROLL_DELAY);
            }
            
            state.isInitialized = true;
            utils.log('Página de produtos inicializada');
        },

        /**
         * Garante que todos os produtos estejam visíveis
         */
        makeAllProductsVisible() {
            const cards = document.querySelectorAll(CONFIG.PRODUCT_CARD_SELECTOR);
            utils.log('Tornando', cards.length, 'produtos visíveis');
            
            cards.forEach(card => {
                card.style.display = 'flex';
                card.style.visibility = 'visible';
                card.style.opacity = '1';
                card.style.pointerEvents = 'auto';
            });
        },

        /**
         * Reinicializa após HTMX swap
         */
        reinit() {
            state.isInitialized = false;
            this.init();
            
            // Faz scroll múltiplas vezes para garantir
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('categoria')) {
                ScrollManager.scrollToProductsMultiple(6);
            }
        }
    };

    // ============================================
    // EXPOSIÇÃO PÚBLICA
    // ============================================
    window.ProductsPage = {
        init: () => ProductsPage.init(),
        reinit: () => ProductsPage.reinit(),
        scrollToProducts: () => ScrollManager.scrollToProducts(),
        filter: (value, byCategory) => FilterManager.filter(value, byCategory),
        showAll: () => FilterManager.showAll()
    };

    // ============================================
    // AUTO-INICIALIZAÇÃO
    // ============================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            if (window.location.pathname.includes('/produtos')) {
                ProductsPage.init();
            }
        });
    } else {
        if (window.location.pathname.includes('/produtos')) {
            ProductsPage.init();
        }
    }

    // ============================================
    // INTEGRAÇÃO COM HTMX
    // ============================================
    if (typeof htmx !== 'undefined') {
        document.body.addEventListener('htmx:afterSwap', (event) => {
            if (event.detail.target === document.body && 
                window.location.pathname.includes('/produtos')) {
                utils.log('HTMX swap detectado, reinicializando...');
                
                setTimeout(() => {
                    ProductsPage.reinit();
                }, 100);
            }
        });
    }

})();

