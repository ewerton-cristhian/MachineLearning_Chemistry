async function getKetcherSmiles() {
    // Obtém o elemento do iframe
    let ketcherFrame = document.getElementById('ifKetcher');
    let ketcher = null;

    // Verifica a disponibilidade do contentDocument no iframe
    if ('contentDocument' in ketcherFrame)
        ketcher = ketcherFrame.contentWindow.ketcher;
    else // IE7 fallback
        ketcher = document.frames['ifKetcher'].window.ketcher;

    // Se o ketcher não estiver disponível, lance um erro
    if (!ketcher) {
        throw new Error('Ketcher não está disponível no iframe');
    }

    try {
        // Aguarda a resolução da promessa de obtenção do SMILES da molécula
        const moleculeSmiles = await ketcher.getSmiles();
        return moleculeSmiles;
    } catch (error) {
        console.error('Erro ao obter SMILES da molécula:', error);
    }
}


document.getElementById('sendDataButton').addEventListener('click', async () => {
    
    const smiles = await getKetcherSmiles();

    fetch('/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ variavel: smiles  })
    })
    .then(response => response.json())
    .then(data => {document.getElementById('predictionResult').innerText = data.response;})
    .catch(error => console.log('Erro:', error));
    });

    //console.log('Resposta do servidor:', data)