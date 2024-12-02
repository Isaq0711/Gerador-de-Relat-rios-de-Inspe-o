let concessionaria = "";
let tipoLocalPlural = "";
let tipoLocalSingular = "";
let tipoLocal = ""
let estacoesSelecionadas = [];
let imagens = []; 
let legendas = [];

// Função para atualizar o tipo de local (Estação, Terminal ou Rodovia)
function updateTipoLocal() {
    concessionaria = document.getElementById("concessionaria").value;
    //plural
    tipoLocalPlural = concessionaria === "CCR Barcas" ? "Terminais" :
                concessionaria === "Rota 116" || concessionaria === "CCR Via Lagos" ? "Rodovias" : "Estações";
    //singular
    tipoLocalSingular = concessionaria === "CCR Barcas" ? "Terminal" :
    concessionaria === "Rota 116" || concessionaria === "CCR Via Lagos" ? "Rodovia" : "Estação"               
    const tipoLocalLabel = document.getElementById("tipoLocalLabel");
    tipoLocalLabel.textContent = tipoLocal === "Rodovia" ? "" : `Número de ${tipoLocalPlural}:`;

    if (concessionaria !== "Selecionar estações") {
        carregarEstacoes();  // Carrega as estações quando a concessionária é selecionada
    }
}

function carregarEstacoes() {
    const concessionariasEstacoes = {
        "Supervia": [
            "Agostinho Porto", "Anchieta", "Augusto Vasconcelos", "Austin", "Bangu", "Barros Filho", "Belford Roxo",
            "Benjamim do Monte", "Bento Ribeiro", "Bonsucesso", "Brás de Pina", "Campo Grande", "Campos Elíseos",
            "Cascadura", "Cavalcanti", "Central do Brasil", "Citrolândia", "Coelho da Rocha", "Comendador Soares",
            "Cordovil", "Corte Oito", "Cosmos", "Costa Barros", "Del Castilho", "Deodoro", "Duque de Caxias", "Edson Passos",
            "Engenheiro Pedreira", "Engenho de Dentro", "Engenho Novo", "Fragoso", "Gramacho", "Guapimirim",
            "Guilherme da Silveira", "Honório Gurgel", "Imbariê", "Inhoaíba", "Iriri", "Jacarezinho", "Japeri",
            "Jardim Guapimirim", "Jardim Nova Marília", "Jardim Primavera", "Jororó", "Lages", "Madureira", "Magalhães Bastos",
            "Magé", "Mangueira", "Manguinhos", "Maracanã", "Marechal Hermes", "Méier", "Mercadão de Madureira", "Mesquita",
            "Mocidade/Padre Miguel", "Monoel Belo", "Morabi", "Nilópolis", "Nova Iguaçu", "Olaria", "Olinda", "Oswaldo Cruz",
            "Paciência", "Paracambi", "Parada Angélica", "Parada Bananal", "Parada de Lucas", "Parada Ideal", "Parada Modelo",
            "Parque Estrela", "Pavuna", "Penha", "Penha Circular", "Piabetá", "Piedade", "Pilares", "Praça da Bandeira",
            "Presidente Juscelino", "Queimados", "Quintino", "Ramos", "Realengo", "Riachuelo", "Ricardo de Albuquerque",
            "Rocha Miranda", "Sampaio", "Santa Cruz", "Santa Dalila", "Santa Guilhermina", "Santíssimo", "São Cristóvão",
            "São Francisco Xavier", "Saracuruna", "Senador Camará", "Silva Freire", "Suruí", "Tancredo Neves", "Tomás Coelho",
            "Triagem", "Vigário Geral", "Vila Inhomirim", "Vila Militar", "Vila Rosali"
        ],
        "CCR Barcas": [
            "Angra dos Reis", "Charitas", "Cocotá", "Ilha Grande", "Mangaratiba", "Paquetá", "Praça Arariboia", "Praça XV"
        ],
        "MetrôRio": [
            "Acari/Fazenda Botafogo", "Afonso Pena", "Antero de Quental", "Botafogo", "Cantagalo", "Cardeal Arcoverde",
            "Carioca", "Catete", "Central", "Cidade Nova", "Cinelândia", "Coelho Neto", "Colégio", "Engenheiro Rubens Paiva",
            "Engenho da Rainha", "Estácio", "Flamengo", "General Osório", "Glória", "Ihaúma", "Irajá", "Jardim de Alah",
            "Jardim Oceânico", "Largo do Machado", "Maracanã", "Maria da Graça", "Nossa Senhora da Paz", "Nova América/Del Castilho",
            "Pavuna", "Praça Onze", "Presidente Vargas", "Saens Peña", "São Conrado", "São Cristóvão", "São Francisco Xavier",
            "Siqueira Campos", "Thomaz Coelho", "Triagem", "Uruguai", "Uruguaiana", "Vicente de Carvalho"
        ],
        "CCR Via Lagos": [], // Sem estações
        "Rota 116": [] // Sem estações
    };

    // Recupera as estações baseadas na concessionária selecionada
    estacoes = concessionariasEstacoes[concessionaria] || [];
    
    // Agora, geramos os campos com base no número de estações selecionadas
    gerarComponentesEstacoes();
}

function gerarComponentesEstacoes() {
    const numEstacoes = parseInt(document.getElementById("numEstacoes").value);
    const estacoesContainer = document.getElementById("estacoesContainer");
    estacoesContainer.innerHTML = "";  // Limpa o conteúdo atual

    estacoesSelecionadas = [];
    imagensPorEstacao = {};  

    for (let i = 0; i < numEstacoes; i++) {
        // Criação do select para a estação
        const estacaoSelect = document.createElement("select");
        estacaoSelect.id = `estacao${i}`;
        estacoesSelecionadas.push(estacaoSelect);

        // Opção de selecionar o local
        const optionSelecionar = document.createElement("option");
        optionSelecionar.textContent = "Selecione o nome do local";
        optionSelecionar.value = "";
        estacaoSelect.appendChild(optionSelecionar);

        // Adicionando opções de estações
        estacoes.forEach(estacao => {
            const option = document.createElement("option");
            option.textContent = estacao;
            option.value = estacao;
            estacaoSelect.appendChild(option);
        });

        // Label da estação
        const estacaoLabel = document.createElement("label");
        estacaoLabel.textContent = `${tipoLocalSingular} ${i + 1}:`;

        // Contêiner único para armazenar a estação e suas imagens
        const estacaoContainer = document.createElement("div");
        estacaoContainer.id = `estacaoContainer${i}`;
        estacaoContainer.classList.add("estacaoContainer");

        // Botão para selecionar imagens
        const botaoImagem = document.createElement("button");
        botaoImagem.textContent = "Selecionar Imagens";
        botaoImagem.onclick = () => selecionarImagensPorEstacao(i);  // Função de seleção de imagens

        // Contêiner para armazenar as imagens dessa estação (único por estação)
        const imagensContainer = document.createElement("div");
        imagensContainer.id = `imagensEstacao${i}`;
        imagensContainer.classList.add("imagensEstacaoContainer");

        // Adiciona o label, select, botão e o contêiner de imagens ao container principal
        estacaoContainer.appendChild(estacaoLabel);
        estacaoContainer.appendChild(estacaoSelect);
        estacaoContainer.appendChild(botaoImagem);
        estacaoContainer.appendChild(imagensContainer);

        // Adiciona o contêiner da estação ao contêiner geral
        estacoesContainer.appendChild(estacaoContainer);

        // Inicializa o array de imagens para a estação
        imagensPorEstacao[`estacao${i}`] = [];
    }
}

// Função para selecionar imagens
function selecionarImagensPorEstacao(index) {
    const inputImagens = document.createElement("input");
    inputImagens.type = "file";
    inputImagens.accept = "image/*";
    inputImagens.multiple = true;

    inputImagens.onchange = () => {
        const files = inputImagens.files;
        if (files.length > 0) {
            const urls = Array.from(files).map(file => ({
                url: URL.createObjectURL(file),
                legenda: ""
            }));
            imagensPorEstacao[`estacao${index}`].push(...urls); 
            atualizarImagensEstacao(index);  // Atualiza as imagens da estação
        }
    };

    inputImagens.click();
}

function atualizarImagensEstacao(index) {
    const imagensContainer = document.getElementById(`imagensEstacao${index}`);
    imagensContainer.innerHTML = "";  // Limpa o conteúdo existente do contêiner da estação

    // Adiciona as imagens e legendas dentro do contêiner único da estação
    imagensPorEstacao[`estacao${index}`].forEach((imgObj, imgIndex) => {
        const divContainer = document.createElement("div");
        divContainer.classList.add("imagemContainer");

        const imgElement = document.createElement("img");
        imgElement.src = imgObj.url;
        imgElement.alt = `Imagem ${imgIndex + 1}`;

        const legendInput = document.createElement("input");
        legendInput.type = 'text';
        legendInput.placeholder = `Legenda da imagem ${imgIndex + 1}`;
        imgElement.onclick = () => abrirModal(imgObj.url); 
        legendInput.value = imgObj.legenda;
        legendInput.oninput = () => {
            imagensPorEstacao[`estacao${index}`][imgIndex].legenda = legendInput.value;
        };

        const apagarButton = document.createElement("button");
        apagarButton.textContent = "X";
        apagarButton.onclick = () => apagarImagem(index, imgIndex);

        divContainer.appendChild(imgElement);
        divContainer.appendChild(legendInput);
        divContainer.appendChild(apagarButton);

        imagensContainer.appendChild(divContainer);
    });
}


function abrirModal(imagemUrl) {
    const modal = document.getElementById("modal");
    const modalImage = document.getElementById("imagemModal");
    

    // Definindo a imagem e legenda no modal
    modalImage.src = imagemUrl;

    // Exibe o modal
    modal.style.display = "flex";
}

function fecharModal() {
    const modal = document.getElementById("modal");
    modal.style.display = "none";  // Esconde o modal ao clicar no botão de fechar
}

function apagarImagem(estacaoIndex, imgIndex) {
    imagensPorEstacao[`estacao${estacaoIndex}`].splice(imgIndex, 1);
    atualizarImagensEstacao(estacaoIndex);
}
// Função para gerar o relatório
function onGenerate() {
    const dataVistoria = document.getElementById("dataVistoria").value;
    const horarioVistoria = document.getElementById("horarioVistoria").value;
    const numEstacoes = parseInt(document.getElementById("numEstacoes").value);
    const estacoes = estacoesSelecionadas.map(estacao => estacao.value);

    if (!concessionaria || !dataVistoria || !horarioVistoria || !numEstacoes) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    // Gerar o relatório (exemplo de saída no console)
    console.log({
        concessionaria,
        tipoLocal: numEstacoes > 1 ? tipoLocalPlural : tipoLocalSingular,
        dataVistoria,
        horarioVistoria,
        estacoes,
        imagens
    });
    
    alert("Relatório gerado no console!");
}
